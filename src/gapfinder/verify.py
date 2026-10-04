"""Verificadores de la Fase 3: dado (idea, candidato), ¿el candidato ya construye la idea?

Tres preguntas por par, cada una una probabilidad en [0, 1]:
- core:      el candidato implementa el núcleo de la idea (la capacidad central que la idea dice que falta).
- partial:   implementa al menos una parte real de ese núcleo (monótona: core alto implica partial alto).
- same_user: está hecho para el mismo usuario objetivo.

Implementaciones:
- JevVerifier: TypeSafe Jev (System One) vía el SDK oficial `typesafe-sdk`. Un request por par con
  tres Nouls (una proposición por pregunta, como recomiendan los docs; state chico y solo con lo
  relevante, porque Jev rinde peor con state largo lleno de detalle irrelevante). Precio: solo tokens
  de entrada ($0.042 / Mtok, jev-1.13).
- HaikuVerifier: Claude Haiku 4.5 como baseline, salida estructurada con las tres probabilidades.
  Para corridas grandes, Message Batches API (50% del precio, asíncrona).
Los resultados se guardan en data/phase3/verdicts_<verifier>.jsonl (append) y se retoman: un par ya
verificado no se vuelve a pedir.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol

log = logging.getLogger(__name__)

OUT_DIR = Path("data/phase3")
CANDIDATE_CHARS = 1500

QUESTIONS = {
    "core": {
        "instructions": "Does `candidate` implement the core of `idea`, meaning the central capability that `idea` says is needed?",
        "true": "The candidate provides the central capability of the idea, even if details, scale or polish differ.",
        "false": "The candidate is only on a related topic, covers a side feature, or is merely a component someone could use to build it.",
    },
    "partial": {
        "instructions": "Does `candidate` implement at least a real part of the central capability that `idea` says is needed?",
        "true": "The candidate delivers a meaningful piece of the idea's central capability (possibly all of it).",
        "false": "The candidate delivers none of the central capability; it is only on a related topic or serves a different purpose.",
    },
    "same_user": {
        "instructions": "Is `candidate` built for the same target user as `idea`?",
        "true": "Same kind of user or buyer, in the same role and context.",
        "false": "A different audience.",
    },
}


@dataclass(frozen=True, slots=True)
class Pair:
    case_id: str
    idea: str
    item_id: str
    title: str
    text: str

    def state(self) -> dict:
        return {"idea": self.idea, "candidate": {"title": self.title, "description": self.text[:CANDIDATE_CHARS]}}


@dataclass(slots=True)
class Verdict:
    case_id: str
    item_id: str
    core: float
    partial: float
    same_user: float
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""
    latency_ms: float = 0.0
    cost_usd: float | None = None   # lo que cobró el proveedor por el request (OpenRouter: usage.cost); None = no informado


class Verifier(Protocol):
    name: str

    def verify(self, pairs: list[Pair]) -> list[Verdict]: ...


def load_done(name: str) -> dict[tuple[str, str], Verdict]:
    path = OUT_DIR / f"verdicts_{name}.jsonl"
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text().splitlines():
        v = Verdict(**json.loads(line))
        out[(v.case_id, v.item_id)] = v
    return out


def _append(name: str, verdicts: list[Verdict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / f"verdicts_{name}.jsonl").open("a") as f:
        for v in verdicts:
            f.write(json.dumps(asdict(v)) + "\n")


# --- Jev (TypeSafe) --------------------------------------------------------------------------------


FATAL_STATUSES = {401, 402, 403}   # key inválida / sin crédito / sin permiso: detener, no reintentar


class JevVerifier:
    """TypeSafe Jev. Requiere TYPESAFE_API_KEY. Concurrencia limitada para quedar bajo 1.200 req/min;
    el SDK reintenta 429/529 con backoff y respeta retry-after."""

    name = "jev"

    def __init__(self, model: str = "jev-1.13.0", concurrency: int = 16, name: str = "jev") -> None:
        self.name = name            # archivo de resultados: verdicts_<name>.jsonl (p. ej. "jev_pilot")
        self.model = model          # versión fija, no el alias: los umbrales se calibran contra esta versión
        self.concurrency = concurrency

    def client_kwargs(self) -> dict:
        return {"model": self.model}   # TypeSafe nativo: TYPESAFE_API_KEY del entorno

    def response_model(self):
        return None

    @staticmethod
    def cost(r) -> float | None:
        return None                     # la API nativa no informa costo; se calcula aparte con el precio de lista

    @staticmethod
    def questions() -> dict:
        from typesafe_sdk import Noul, NoulCriteria

        return {k: Noul(instructions=q["instructions"], criteria=NoulCriteria(true=q["true"], false=q["false"]))
                for k, q in QUESTIONS.items()}

    def verify(self, pairs: list[Pair]) -> list[Verdict]:
        return asyncio.run(self._verify(pairs))

    async def _verify(self, pairs: list[Pair]) -> list[Verdict]:
        from typesafe_sdk import AsyncTypeSafeClient, TypeSafeAPIError

        done = load_done(self.name)
        todo = [p for p in pairs if (p.case_id, p.item_id) not in done]
        sem = asyncio.Semaphore(self.concurrency)
        questions = self.questions()
        out: list[Verdict] = []
        fatal: list[str] = []   # error de cuenta (sin crédito, key inválida): no tiene sentido seguir pidiendo

        async with AsyncTypeSafeClient(**self.client_kwargs()) as client:
            async def one(p: Pair) -> Verdict | None:
                async with sem:
                    if fatal:
                        return None
                    t0 = time.perf_counter()
                    try:
                        r = await client.system_one(p.state(), questions, response_model=self.response_model())
                    except TypeSafeAPIError as e:
                        if e.status in FATAL_STATUSES:
                            fatal.append(f"{e.status}: {e}")
                        log.error("jev %s %s: %s", p.case_id, p.item_id, e)
                        return None
                    ms = (time.perf_counter() - t0) * 1000   # incluye reintentos del SDK si los hubo
                a = r.answers
                return Verdict(p.case_id, p.item_id, a["core"].noul, a["partial"].noul, a["same_user"].noul,
                               r.usage.input_tokens, r.usage.output_tokens, r.model, ms, self.cost(r))

            for start in range(0, len(todo), 500):
                got = [v for v in await asyncio.gather(*(one(p) for p in todo[start:start + 500])) if v]
                _append(self.name, got)
                out += got
                log.info("jev: %d/%d pares", start + len(got), len(todo))
                if fatal:
                    raise RuntimeError(f"jev: corrida detenida por error de cuenta ({fatal[0][:160]}); "
                                       f"{len(done) + len(out)} pares guardados, se retoma al relanzar")
        return list(done.values()) + out


class OpenRouterJevVerifier(JevVerifier):
    """Jev vía OpenRouter (registros de TypeSafe pausados). Según los docs de OpenRouter, su endpoint
    POST /api/v1/systemone implementa el formato de TypeSafe, así que se usa el mismo SDK oficial con
    base_url de OpenRouter y OPENROUTER_API_KEY. Modelo fijo `typesafe/jev-1.13` (no jev-router, que
    elige modelo por su cuenta). OpenRouter agrega `id`, `provider` y `usage.cost` (lo cobrado); el SDK
    los descarta por defecto, por eso se pasa un response_model que los conserva."""

    BASE_URL = "https://openrouter.ai/api"

    def __init__(self, model: str = "typesafe/jev-1.13", concurrency: int = 16, name: str = "jev_openrouter") -> None:
        super().__init__(model=model, concurrency=concurrency, name=name)

    def client_kwargs(self) -> dict:
        import os

        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("falta OPENROUTER_API_KEY en .env")
        return {"model": self.model, "api_key": key, "base_url": self.BASE_URL}

    def response_model(self):
        return openrouter_response_model()

    @staticmethod
    def cost(r) -> float | None:
        return r.usage.cost


def openrouter_response_model():
    from pydantic import BaseModel
    from typesafe_sdk import NoulAnswer

    class OpenRouterUsage(BaseModel):
        input_tokens: int
        output_tokens: int
        cost: float | None = None

    class OpenRouterSystemOneResponse(BaseModel):
        id: str | None = None
        model: str
        provider: str | None = None
        answers: dict[str, NoulAnswer]
        usage: OpenRouterUsage

    return OpenRouterSystemOneResponse


# --- Claude Haiku (baseline) --------------------------------------------------------------------------

HAIKU_MODEL = "claude-haiku-4-5"
HAIKU_SYSTEM = (
    "You judge whether an existing product or project already builds an idea. You get IDEA and CANDIDATE "
    "(title and description). Answer three questions, each as your probability from 0 to 1 that the answer "
    "is yes:\n"
    + "\n".join(f"- {k}: {q['instructions'].replace('`', '')} Yes means: {q['true']} No means: {q['false']}"
                for k, q in QUESTIONS.items())
    + "\nJudge only from the text given. Be calibrated: use values near 0.5 when the text does not settle it."
)
HAIKU_SCHEMA = {
    "type": "object",
    "properties": {k: {"type": "number"} for k in QUESTIONS},
    "required": list(QUESTIONS),
    "additionalProperties": False,
}


def haiku_params(p: Pair) -> dict:
    s = p.state()
    user = (f"IDEA:\n{s['idea']}\n\nCANDIDATE:\nTitle: {s['candidate']['title']}\n"
            f"Description: {s['candidate']['description']}")
    return {"model": HAIKU_MODEL, "max_tokens": 200, "system": HAIKU_SYSTEM,
            "output_config": {"format": {"type": "json_schema", "schema": HAIKU_SCHEMA}},
            "messages": [{"role": "user", "content": user}]}


class HaikuVerifier:
    """Claude Haiku 4.5 vía Message Batches API (50% del precio). `verify` crea el batch, espera y
    guarda; el id del batch queda en data/phase3/haiku_batches.json para retomar si se corta."""

    name = "haiku"

    def verify(self, pairs: list[Pair], poll_seconds: int = 60) -> list[Verdict]:
        import time

        import anthropic
        from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
        from anthropic.types.messages.batch_create_params import Request

        client = anthropic.Anthropic()
        done = load_done(self.name)
        todo = [p for p in pairs if (p.case_id, p.item_id) not in done]
        state_path = OUT_DIR / "haiku_batches.json"
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        batches = json.loads(state_path.read_text()) if state_path.exists() else []
        pending = {tuple(v) for e in batches if not e.get("saved") for v in e["ids"].values()}
        todo = [p for p in todo if (p.case_id, p.item_id) not in pending]  # ya enviados, sin resultados aún
        offset = sum(len(e["ids"]) for e in batches)                       # custom_ids únicos entre batches
        for start in range(0, len(todo), 50_000):   # límite: 100k requests / 256 MB por batch
            chunk = todo[start:start + 50_000]
            ids = {f"p{offset + start + n}": (p.case_id, p.item_id) for n, p in enumerate(chunk)}
            b = client.messages.batches.create(requests=[
                Request(custom_id=cid, params=MessageCreateParamsNonStreaming(**haiku_params(p)))
                for cid, p in zip(ids, chunk)])
            batches.append({"id": b.id, "ids": ids})
            state_path.write_text(json.dumps(batches))
        out = []
        for entry in batches:
            if entry.get("saved"):
                continue
            while client.messages.batches.retrieve(entry["id"]).processing_status != "ended":
                time.sleep(poll_seconds)
            got = []
            for res in client.messages.batches.results(entry["id"]):
                case_id, item_id = entry["ids"][res.custom_id]
                if res.result.type != "succeeded" or res.result.message.stop_reason == "refusal":
                    log.error("haiku %s %s: %s", case_id, item_id, res.result.type)
                    continue
                msg = res.result.message
                data = json.loads(next(b.text for b in msg.content if b.type == "text"))
                clip = lambda x: min(max(float(x), 0.0), 1.0)
                got.append(Verdict(case_id, item_id, clip(data["core"]), clip(data["partial"]), clip(data["same_user"]),
                                   msg.usage.input_tokens, msg.usage.output_tokens, msg.model))
            _append(self.name, got)
            entry["saved"] = True
            state_path.write_text(json.dumps(batches))
            out += got
        return list(done.values()) + out
