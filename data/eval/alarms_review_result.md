# Adjudicación de alarmas: negativos por remoción (Jev, phase3 report v1)

Revisión PARCIAL: 23/47 alarmas (la más alta de cada caso, P(núcleo) >= 0.85). núcleo = implementación real no listada; parcial = implementa una parte; no = error del verificador. Error = no / (núcleo + parcial + no).

| grupo | alarmas | núcleo | parcial | no | no sé | error del verificador |
|---|---|---|---|---|---|---|
| todas | 47 | 17 | 2 | 1 | 3 | 5% |
| real | 7 | 2 | 1 | 0 | 2 | 0% |
| synthetic | 40 | 15 | 1 | 1 | 1 | 6% |
| Jev 0.85-0.90 | 13 | 2 | 2 | 1 | 1 | 20% |
| Jev 0.90-0.95 | 17 | 4 | 0 | 0 | 2 | 0% |
| Jev 0.95-1.00 | 17 | 11 | 0 | 0 | 0 | 0% |

## Errores del verificador (humano: no)

| caso | candidato | Jev núcleo |
|---|---|---|
| `syn-23340711` | Probably the simplest Reddit-style site you'll ever use | 0.89 |
