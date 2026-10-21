"""CLI de gapfinder."""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path

from gapfinder import db

def load_dotenv(path: Path = Path(".env")) -> None:
    """KEY=VALUE por línea; no pisa variables ya definidas en el entorno."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        key, sep, value = line.strip().partition("=")
        if sep and key and not key.startswith("#"):
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


load_dotenv()
DEFAULT_DB = Path(os.environ.get("GAPFINDER_DB", "data/corpus.db"))


def cmd_ingest(args: argparse.Namespace) -> None:
    from gapfinder.ingest import github, hn

    conn = db.connect(args.db)
    if args.source in ("hn", "all"):
        n = hn.ingest(conn, limit=args.limit)
        print(f"show_hn: +{n} nuevos, {db.count_items(conn, 'show_hn')} en total")
    if args.source in ("github", "all"):
        n = github.ingest(conn, limit=args.limit, min_stars=args.min_stars, max_stars=args.max_stars)
        print(f"github: +{n} nuevos, {db.count_items(conn, 'github')} en total")
    if args.readmes:
        n = github.fetch_readmes(conn, limit=args.readme_limit)
        print(f"github: {n} README procesados")


def cmd_enrich(args: argparse.Namespace) -> None:
    from gapfinder.ingest import enrich

    conn = db.connect(args.db)
    counts = enrich.enrich(conn, limit=args.limit, workers=args.workers, wayback_workers=args.wayback_workers,
                           wayback_rpm=args.wayback_rpm, wayback_min_points=args.wayback_min_points,
                           only=args.only, order=args.order)
    print(f"enrich: {counts}")


def cmd_probe_comments(args: argparse.Namespace) -> None:
    from gapfinder.ingest import hn_comments

    conn = db.connect(args.db)
    print(hn_comments.probe(conn, per_stratum=args.per_stratum, examples=args.examples))


def cmd_worksheet(args: argparse.Namespace) -> None:
    from gapfinder import cases

    if args.out.exists() and not args.force:
        raise SystemExit(f"{args.out} ya existe (puede tener tus respuestas). Usá --force para regenerarla.")
    origins = None
    if args.origins:
        origins = {o: int(k) for o, k in (part.split("=") for part in args.origins.split(","))}
    others = [p for p in args.out.parent.glob("synthetic_worksheet*.md") if p.resolve() != args.out.resolve()]
    conn = db.connect(args.db)
    args.out.write_text(cases.build_worksheet(conn, n=args.n, seed=args.seed, origins=origins,
                                              exclude=cases.worksheet_item_ids(others)))
    n_items = args.out.read_text().count("\n## ")
    print(f"hoja escrita en {args.out}: {n_items} items")


def cmd_worksheet_import(args: argparse.Namespace) -> None:
    from gapfinder import cases, leakage

    conn = db.connect(args.db)
    idf = leakage.load_idf(conn, Path("data/cache/idf.json"))
    parsed, _ = cases.parse_worksheet(args.worksheet.read_text(), args.worksheet.name)
    flagged = {c["id"] for c, leak in zip(parsed, cases.leakage_report(conn, parsed, idf)) if leak.flagged}
    n, empty = cases.import_worksheet(args.worksheet, args.cases, flagged)
    print(f"{n} casos sintéticos en {args.cases}" + (f"; {len(empty)} sin necesidad: {', '.join(empty)}" if empty else ""))
    if flagged:
        print(f"con leakage_flag (el filtro las marca y quedaron así): {', '.join(sorted(flagged))}")


def cmd_worksheet_check(args: argparse.Namespace) -> None:
    from gapfinder import cases, leakage

    conn = db.connect(args.db)
    idf = leakage.load_idf(conn, Path("data/cache/idf.json"), refresh=args.refresh_idf)
    parsed, empty = cases.parse_worksheet(args.worksheet.read_text(), args.worksheet.name)
    flagged = 0
    for c, leak in zip(parsed, cases.leakage_report(conn, parsed, idf)):
        flagged += leak.flagged
        mark = "REESCRIBIR" if leak.flagged else "ok"
        terms = ", ".join(f"{w}({v})" for w, v in leak.distinctive) or "-"
        print(f"{mark:<10} {c['id']:<14} {c['author']:<6} distintivos: {terms}")
    print(f"\n{flagged} de {len(parsed)} marcadas para reescribir; {len(empty)} sin necesidad (idf sobre {idf.n_docs} docs)")


CONSTELLATE_ROOT = Path(os.environ.get("CONSTELLATE_ROOT", Path.home() / "Documents/constellate-engine"))


def cmd_real_candidates(args: argparse.Namespace) -> None:
    from gapfinder import real_cases

    if args.out.exists() and not args.force:
        raise SystemExit(f"{args.out} ya existe (puede tener tus marcas). Usá --force para regenerarlo.")
    conn = db.connect(args.db)
    text, stats = real_cases.build_candidates(conn, CONSTELLATE_ROOT, Path("data/cache/real_notes.md"))
    args.out.write_text(text)
    print(f"candidatos escritos en {args.out}")
    print(json.dumps(stats, ensure_ascii=False))


def cmd_real_import(args: argparse.Namespace) -> None:
    from gapfinder import real_cases

    conn = db.connect(args.db)
    r = real_cases.import_candidates(conn, args.candidates, CONSTELLATE_ROOT, args.cases)
    print(f"{r['real']} reales, {r['partial']} parciales y {r['negative']} negativos en {args.cases}; "
          f"{len(r['discarded'])} descartados; {len(r['pending'])} sin marcar")
    if r["outside"]:
        print(f"reales/parciales sin ninguna URL esperada en el corpus (miden cobertura, no retrieval): "
              f"{', '.join(r['outside'])}")


def cmd_reclean_readmes(args: argparse.Namespace) -> None:
    from concurrent.futures import ThreadPoolExecutor

    import httpx

    from gapfinder.ingest.github import _try_readme, clean_readme, is_rst_noisy

    conn = db.connect(args.db)
    if args.refetch_rst:
        # El README se guarda limpio y truncado: el ruido .rst que se limpió tarde ocupó parte de ese
        # espacio, así que para recuperar el texto hay que volver a bajarlo con la limpieza actual.
        for table, key, repo_sql in (("enrichment", "item_id", "github_repo"), ("items", "id", "substr(id, 8)")):
            rows = [(k, repo) for k, repo, readme in conn.execute(
                f"SELECT {key}, {repo_sql}, readme FROM {table} WHERE readme IS NOT NULL AND readme != ''")
                if repo and is_rst_noisy(readme)]
            with httpx.Client(timeout=20, follow_redirects=True) as client, ThreadPoolExecutor(8) as pool:
                got = [(r, k) for (k, _), r in zip(rows, pool.map(lambda x: _try_readme(client, x[1]), rows))
                       if r]  # None = limitado, '' = ya no tiene README: se queda el guardado y se re-limpia abajo
            conn.executemany(f"UPDATE {table} SET readme=? WHERE {key}=?", got)
            conn.commit()
            print(f"{table}: {len(got)} de {len(rows)} README con restos .rst vueltos a bajar")
    for table, key in (("enrichment", "item_id"), ("items", "id")):
        rows = conn.execute(f"SELECT {key}, readme FROM {table} WHERE readme IS NOT NULL AND readme != ''").fetchall()
        changed = [(new, r[0]) for r in rows if (new := clean_readme(r[1])) != r[1]]
        conn.executemany(f"UPDATE {table} SET readme=? WHERE {key}=?", changed)
        conn.commit()
        print(f"{table}: {len(changed)} de {len(rows)} README re-limpiados")


def cmd_embed(args: argparse.Namespace) -> None:
    from gapfinder import embed

    conn = db.connect(args.db)
    for key in (embed.ACTIVE if args.model == "all" else [args.model]):
        for name in args.index:
            n = embed.build(conn, key, name)
            print(f"embed {key}/{name}: {n} vectores nuevos")


def cmd_targeted(args: argparse.Namespace) -> None:
    from gapfinder import targeted

    conn = db.connect(args.db)
    cases = json.loads(args.cases.read_text())
    llm_queries = json.loads(Path("data/llm_queries.json").read_text()) if args.llm else None
    print(f"targeted: {targeted.run(conn, cases, llm_queries=llm_queries)}")


def cmd_eval(args: argparse.Namespace) -> None:
    from gapfinder import embed, eval as ev

    conn = db.connect(args.db)
    cases = json.loads(args.cases.read_text())
    models = embed.ACTIVE if args.model == "all" else [args.model]
    print(ev.run(conn, cases, models, args.out))
    print(f"reporte en {args.out / 'phase2_recall.md'}")


def cmd_llm_queries(args: argparse.Namespace) -> None:
    from gapfinder import llm

    cases = [c for c in json.loads(args.cases.read_text()) if not args.kinds or c["kind"] in args.kinds.split(",")]
    print(f"llm-queries: {llm.generate(cases, out=args.out, version=args.prompt_version)}")
    if args.copy_rest_from:  # los casos no regenerados se copian tal cual (para evals que necesitan todos)
        out, src = json.loads(args.out.read_text()), json.loads(args.copy_rest_from.read_text())
        out.update({k: v for k, v in src.items() if k not in out})
        args.out.write_text(json.dumps(out, indent=1, ensure_ascii=False))


def cmd_bm25(args: argparse.Namespace) -> None:
    from gapfinder import bm25

    n = bm25.build(db.connect(args.db), bm25.connect())
    print(f"bm25: {n} items agregados al índice FTS5")


def cmd_eval2(args: argparse.Namespace) -> None:
    from gapfinder import embed, eval2

    conn = db.connect(args.db)
    cases = json.loads(args.cases.read_text())
    models = embed.ACTIVE if args.model == "all" else [args.model]
    print(eval2.run(conn, cases, models, args.out, targeted=args.targeted, llm_path=args.llm_queries))
    print(f"reporte en {args.out / 'iter2_recall.md'}")


def _phase3_cases(args: argparse.Namespace) -> list[dict]:
    kinds = set(args.kinds.split(","))
    return [c for c in json.loads(args.cases.read_text()) if c["kind"] in kinds and c.get("expected_item_ids")]


def cmd_phase3(args: argparse.Namespace) -> None:
    from gapfinder import phase3, verify

    conn = db.connect(args.db)
    if args.step == "review-pilot":  # revisión humana de los 50 pares del piloto
        from gapfinder import pilot
        print(pilot.interactive_review(conn, json.loads(args.cases.read_text())))
        return
    if args.step == "review-labels":  # las 4 etiquetas de positivos reales que la revisión del piloto juzgó "no"
        from gapfinder import pilot
        print(pilot.interactive_labels(conn, json.loads(args.cases.read_text())))
        return
    if args.step == "review-alarms":  # adjudicación humana de las alarmas más altas (negativos por remoción)
        from gapfinder import pilot
        print(pilot.interactive_alarms(conn, json.loads(args.cases.read_text()), per_bin=args.per_bin))
        return
    cases = _phase3_cases(args)
    cand_path = verify.OUT_DIR / f"candidates_{args.model}{args.suffix}.json"
    if args.step == "candidates":
        cand = phase3.retrieve(conn, cases, args.model, llm_path=args.llm_queries, suffix=args.suffix)
        print(f"candidatos: {len(cand)} casos en {cand_path}")
        return
    cand = json.loads(cand_path.read_text())
    if args.step == "estimate":
        print(json.dumps(phase3.estimate(conn, cases, cand), indent=1))
    elif args.step == "verify":
        cls = {"jev": verify.JevVerifier, "jev-openrouter": verify.OpenRouterJevVerifier,
               "haiku": verify.HaikuVerifier}[args.verifier]
        verifier = cls(concurrency=args.concurrency) if args.verifier != "haiku" else cls()
        if args.name:
            verifier.name = args.name
        pairs = phase3.pairs_for(conn, cases, cand, llm_path=args.llm_queries)
        if args.only_new_vs:  # solo los pares cuyo item no estaba en otro archivo de candidatos
            old = json.loads(args.only_new_vs.read_text())
            pairs = [p for p in pairs if p.item_id not in set(old.get(p.case_id, []))]
        print(f"{len(pairs)} pares a verificar ({verifier.name})")
        print(f"{args.verifier}: {len(verifier.verify(pairs))} veredictos")
    elif args.step == "report":
        default_names = {"jev": "jev", "jev-openrouter": "jev_openrouter", "haiku": "haiku"}
        name = args.name or default_names[args.verifier]   # mismo archivo que escribió `verify`
        verdicts = verify.load_done(name)
        if not verdicts:
            raise SystemExit(f"no hay veredictos en {verify.OUT_DIR / f'verdicts_{name}.jsonl'}")
        m = phase3.metrics(conn, cases, cand, verdicts)
        (verify.OUT_DIR / f"metrics_{name}.json").write_text(json.dumps(m, indent=1))
        print(json.dumps({k: v for k, v in m.items() if k != "top_alarms"}, indent=1))
        print("alarmas más altas (revisar a mano):", json.dumps(m["top_alarms"][:20], indent=1))


def cmd_pilot(args: argparse.Namespace) -> None:
    from gapfinder import pilot, verify

    conn = db.connect(args.db)
    cases = json.loads(args.cases.read_text())
    if args.step == "select":
        cand = json.loads((verify.OUT_DIR / f"candidates_{args.model}.json").read_text())
        picked = pilot.select(conn, cases, cand)
        print({s: sum(p["stratum"] == s for p in picked) for s in {p["stratum"] for p in picked}})
        return
    picked = json.loads(pilot.PAIRS_PATH.read_text())
    pairs = pilot.to_pairs(conn, cases, picked)
    if args.step == "haiku":
        print(pilot.run_haiku(pairs))
    elif args.step == "jev":
        verify.JevVerifier(name="jev_pilot", concurrency=8).verify(pairs)
    elif args.step == "jev-openrouter":
        verify.OpenRouterJevVerifier(name="jev_openrouter_pilot", concurrency=8).verify(pairs)
    pilot.review(conn, cases, picked, pairs)
    print(json.dumps({"haiku": pilot.summary("haiku_pilot", 1.0, 5.0),
                      "jev_openrouter": pilot.summary("jev_openrouter_pilot", 0.042, 0.0),
                      "jev_typesafe": pilot.summary("jev_pilot", 0.042, 0.0),
                      "acuerdo_jev_openrouter_vs_haiku": pilot.agreement(pairs, "jev_openrouter_pilot", "haiku_pilot")},
                     indent=1))
    print(f"revisión en {pilot.REVIEW_PATH}")


def cmd_holdout(args: argparse.Namespace) -> None:
    from gapfinder import holdout

    conn = db.connect(args.db)
    chosen, cases, queries = holdout.selected_cases(conn)
    if args.step == "retrieve":
        cand = holdout.retrieve(conn, cases, queries)
        print(f"holdout: top-{holdout.K} para {len(cand)} ideas en {holdout.DIR / 'candidates.json'}")
    elif args.step == "verify":
        cand = json.loads((holdout.DIR / "candidates.json").read_text())
        print(holdout.verify_with_budget(holdout.pairs(conn, cand, queries), args.budget))
    elif args.step == "review":
        from gapfinder import review
        print(review.interactive_holdout(conn))
    elif args.step == "report":
        holdout.report(conn)
        print("reporte en data/eval/holdout_temporal.md")


def cmd_askhn(args: argparse.Namespace) -> None:
    from gapfinder import askhn

    if args.step == "collect":
        print(json.dumps(askhn.collect(), indent=1, ensure_ascii=False))
    elif args.step == "extract":
        print(json.dumps(askhn.extract(db.connect(args.db), limit=args.limit), indent=1, ensure_ascii=False))
    elif args.step == "select":
        order = askhn.select()
        print(f"elegidos: {len(order)} en {askhn.SELECTED}")
    elif args.step == "run":
        print(json.dumps(askhn.run(db.connect(args.db), budget=args.budget), indent=1, ensure_ascii=False))
    elif args.step == "report":
        askhn.report(db.connect(args.db))
        print(f"reporte en {askhn.REPORT}")
    elif args.step == "remap":
        print(f"remapeados: {askhn.remap(db.connect(args.db))}")


def cmd_gaps(args: argparse.Namespace) -> None:
    from gapfinder import gaps

    if args.step == "extract":
        res = gaps.extract(limit=args.limit)
        muestra = res.pop("muestra")
        print(json.dumps(res, indent=1, ensure_ascii=False))
        print(muestra)
        return
    conn = db.connect(args.db)
    if args.step == "compare":
        print(gaps.compare(conn))
    elif args.step == "run":
        print(json.dumps(gaps.run(conn, rerun_first=args.rerun_first), indent=1, ensure_ascii=False))
    elif args.step == "report":
        gaps.report(conn)
        print(f"lista en {gaps.REPORT}")


def cmd_review(args: argparse.Namespace) -> None:
    from gapfinder import review

    review.menu(db.connect(args.db), json.loads(args.cases.read_text()), evaluar=args.evaluar)


def cmd_census(args: argparse.Namespace) -> None:
    from gapfinder.ingest import github

    table = github.census(args.stars)
    header = "año   " + "".join(f"{'>=' + str(t):>12}" for t in args.stars)
    print(header)
    for year, row in table.items():
        print(f"{year}  " + "".join(f"{row[t]:>12,}" for t in args.stars))
    print("total " + "".join(f"{sum(r[t] for r in table.values()):>12,}" for t in args.stars))


def cmd_stats(args: argparse.Namespace) -> None:
    conn = db.connect(args.db)
    rows = conn.execute(
        """SELECT source, COUNT(*), MIN(created_at), MAX(created_at),
                  SUM(description != ''), SUM(readme IS NOT NULL AND readme != ''),
                  SUM(archived = 1)
           FROM items GROUP BY source"""
    ).fetchall()
    print(f"{'fuente':<8} {'items':>8}  {'desde':<10}  {'hasta':<10}  {'con desc':>8}  {'con README':>10}  {'archivados':>10}")
    for s, n, lo, hi, desc, readme, arch in rows:
        print(f"{s:<8} {n:>8}  {lo[:10]}  {hi[:10]}  {desc:>8}  {readme or 0:>10}  {arch or 0:>10}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="gapfinder")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("ingest", help="descarga el corpus de oferta a SQLite")
    p.add_argument("--source", choices=["hn", "github", "all"], default="all")
    p.add_argument("--limit", type=int, default=50_000, help="máximo de items por fuente")
    p.add_argument("--min-stars", type=int, default=100, help="GitHub: estrellas mínimas")
    p.add_argument("--max-stars", type=int, help="GitHub: estrellas máximas (para ampliar por bandas)")
    p.add_argument("--readmes", action="store_true", help="GitHub: bajar README truncado")
    p.add_argument("--readme-limit", type=int, default=10**9, help="máximo de README a bajar en esta corrida")
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser("enrich", help="Show HN sin descripción: vincular GitHub o bajar meta description")
    p.add_argument("--limit", type=int, default=10**9)
    p.add_argument("--workers", type=int, default=32)
    p.add_argument("--wayback-workers", type=int, default=3)
    p.add_argument("--wayback-rpm", type=float, default=15, help="requests/min a archive.org (global)")
    p.add_argument("--wayback-min-points", type=int, default=None,
                   help="activa Wayback en bulk para posts con >= N puntos (default: pausado)")
    p.add_argument("--only", choices=["github", "web"], help="limitar a URLs de GitHub o al resto")
    p.add_argument("--order", choices=["points", "random"], default="points")
    p.set_defaults(func=cmd_enrich)

    p = sub.add_parser("probe-comments", help="cobertura de comentarios del autor en Show HN web sin descripción")
    p.add_argument("--per-stratum", type=int, default=100)
    p.add_argument("--examples", type=int, default=20)
    p.set_defaults(func=cmd_probe_comments)

    p = sub.add_parser("worksheet", help="hoja para escribir casos sintéticos a mano")
    p.add_argument("--n", type=int, default=40)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--origins", help="cuotas por origen de texto, p. ej. author_comment=10,author_reply=10")
    p.add_argument("--out", type=Path, default=Path("data/synthetic_worksheet.md"))
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_worksheet)

    p = sub.add_parser("worksheet-import", help="convierte la hoja completada en casos kind=synthetic")
    p.add_argument("--worksheet", type=Path, default=Path("data/synthetic_worksheet.md"))
    p.add_argument("--cases", type=Path, default=Path("data/known_cases.json"))
    p.set_defaults(func=cmd_worksheet_import)

    p = sub.add_parser("worksheet-check", help="filtro de fuga léxica entre necesidad e item esperado")
    p.add_argument("--worksheet", type=Path, default=Path("data/synthetic_worksheet.md"))
    p.add_argument("--refresh-idf", action="store_true")
    p.set_defaults(func=cmd_worksheet_check)

    p = sub.add_parser("real-candidates", help="arma data/real_candidates.md con las absences verificadas de Constellate")
    p.add_argument("--out", type=Path, default=Path("data/real_candidates.md"))
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_real_candidates)

    p = sub.add_parser("real-import", help="importa los candidatos marcados como casos real / partial / negative")
    p.add_argument("--candidates", type=Path, default=Path("data/real_candidates.md"))
    p.add_argument("--cases", type=Path, default=Path("data/known_cases.json"))
    p.set_defaults(func=cmd_real_import)

    p = sub.add_parser("reclean-readmes", help="re-aplica la limpieza actual a los README guardados")
    p.add_argument("--refetch-rst", action="store_true",
                   help="antes, vuelve a bajar los README con restos de reStructuredText (raw.githubusercontent)")
    p.set_defaults(func=cmd_reclean_readmes)

    p = sub.add_parser("embed", help="Fase 2: embeddings del corpus (retoma por bloques)")
    p.add_argument("--model", choices=["minilm", "e5", "bge", "all"], default="all")
    p.add_argument("--index", nargs="+", choices=["corpus", "targeted"], default=["corpus"])
    p.set_defaults(func=cmd_embed)

    p = sub.add_parser("targeted", help="Fase 2: búsqueda dirigida por caso (GitHub sin filtro + Show HN)")
    p.add_argument("--cases", type=Path, default=Path("data/known_cases.json"))
    p.add_argument("--llm", action="store_true", help="usar las palabras clave de data/llm_queries.json")
    p.set_defaults(func=cmd_targeted)

    p = sub.add_parser("eval", help="Fase 2: recall@50/200/1000 sobre known_cases.json")
    p.add_argument("--cases", type=Path, default=Path("data/known_cases.json"))
    p.add_argument("--model", choices=["minilm", "e5", "bge", "all"], default="all")
    p.add_argument("--out", type=Path, default=Path("data/eval"))
    p.set_defaults(func=cmd_eval)

    p = sub.add_parser("llm-queries", help="Claude: query_core, reformulaciones y palabras clave por caso")
    p.add_argument("--cases", type=Path, default=Path("data/known_cases.json"))
    p.add_argument("--out", type=Path, default=Path("data/llm_queries.json"))
    p.add_argument("--prompt-version", type=int, choices=[1, 2], default=1, help="2 = permite términos de categoría")
    p.add_argument("--kinds", default="", help="solo estos kinds (separados por coma); vacío = todos")
    p.add_argument("--copy-rest-from", type=Path, help="copiar de este archivo los casos no regenerados")
    p.set_defaults(func=cmd_llm_queries)

    p = sub.add_parser("bm25", help="índice FTS5 (BM25) sobre título + texto resuelto; incremental")
    p.set_defaults(func=cmd_bm25)

    p = sub.add_parser("eval2", help="retrieval iteración 2: RRF con N justo, BM25, híbrido, consultas de Claude")
    p.add_argument("--cases", type=Path, default=Path("data/known_cases.json"))
    p.add_argument("--model", choices=["minilm", "bge", "all"], default="all")
    p.add_argument("--out", type=Path, default=Path("data/eval"))
    p.add_argument("--targeted", action="store_true", help="agregar la variante con búsqueda dirigida (fuera por defecto)")
    p.add_argument("--llm-queries", type=Path, default=Path("data/llm_queries.json"), help="consultas de Claude (v1 o v2)")
    p.set_defaults(func=cmd_eval2)

    p = sub.add_parser("phase3", help="Fase 3: candidatos top-1000, estimación de costo, verificador y métricas")
    p.add_argument("step", choices=["candidates", "estimate", "verify", "report", "review-pilot", "review-alarms", "review-labels"])
    p.add_argument("--model", choices=["minilm", "bge"], default="minilm", help="modelo de embeddings de los candidatos")
    p.add_argument("--verifier", choices=["jev", "jev-openrouter", "haiku"], default="haiku")
    p.add_argument("--kinds", default="real,synthetic", help="kinds de casos, separados por coma")
    p.add_argument("--concurrency", type=int, default=6, help="requests en paralelo (Jev: límite ~1.200 req/min)")
    p.add_argument("--per-bin", type=int, help="review-alarms: muestra de hasta N alarmas por tramo de puntaje")
    p.add_argument("--llm-queries", type=Path, default=Path("data/llm_queries.json"), help="consultas/idea (v1 o v2)")
    p.add_argument("--suffix", default="", help="sufijo del archivo de candidatos (p. ej. _v2_real)")
    p.add_argument("--name", help="nombre del archivo de veredictos (verdicts_<name>.jsonl)")
    p.add_argument("--only-new-vs", type=Path, help="verificar solo items ausentes en este archivo de candidatos")
    p.add_argument("--cases", type=Path, default=Path("data/known_cases.json"))
    p.set_defaults(func=cmd_phase3)

    p = sub.add_parser("pilot", help="Fase 3: piloto de 50 pares (mismos pares para Jev y Haiku) + hoja de revisión")
    p.add_argument("step", choices=["select", "haiku", "jev", "jev-openrouter", "review"])
    p.add_argument("--model", choices=["minilm", "bge"], default="minilm")
    p.add_argument("--cases", type=Path, default=Path("data/known_cases.json"))
    p.set_defaults(func=cmd_pilot)

    p = sub.add_parser("holdout", help="holdout temporal: retrieval sobre el corpus anterior a T y verificación con Jev")
    p.add_argument("step", choices=["retrieve", "verify", "review", "report"])
    p.add_argument("--budget", type=float, default=1.26, help="tope de gasto de Jev en USD (usage.cost real)")
    p.set_defaults(func=cmd_holdout)

    p = sub.add_parser("askhn", help="Fase 4: Ask HN \"¿hay una herramienta para…?\" (demanda)")
    p.add_argument("step", choices=["collect", "extract", "remap", "select", "run", "report"])
    p.add_argument("--budget", type=float, default=2.40, help="run: tope de gasto total de la Fase 4 en USD (todos los proveedores)")
    p.add_argument("--limit", type=int, help="extract: solo los primeros N que faltan (validación)")
    p.set_defaults(func=cmd_askhn)

    p = sub.add_parser("gaps", help="candidatos a hueco: extracción automática de Ask HN y lista final para revisar")
    p.add_argument("step", choices=["extract", "compare", "run", "report"])
    p.add_argument("--limit", type=int, help="extract: solo los primeros N que faltan (prueba)")
    p.add_argument("--rerun-first", type=int, default=40, help="run: huecos a re-correr primero con K=1000")
    p.set_defaults(func=cmd_gaps)

    p = sub.add_parser("review", help="menú único de revisión humana: etiquetas, holdout, Ask HN, Fase 4, huecos")
    p.add_argument("--cases", type=Path, default=Path("data/known_cases.json"))
    p.add_argument("--evaluar", action="store_true", help="mostrar también la cola c) de confirmación manual de la extracción")
    p.set_defaults(func=cmd_review)

    p = sub.add_parser("census", help="GitHub: repos por año de creación y umbral de estrellas")
    p.add_argument("--stars", type=int, nargs="+", default=[20, 50, 100])
    p.set_defaults(func=cmd_census)

    p = sub.add_parser("stats", help="resumen del corpus")
    p.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    args.func(args)


if __name__ == "__main__":
    main()
