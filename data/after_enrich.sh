#!/bin/zsh
# Espera a que termine `gapfinder enrich` y corre el post-proceso acordado.
cd "$(dirname "$0")/.."
while pgrep -f "gapfinder enrich" >/dev/null; do sleep 120; done
if ! tail -1 data/enrich_full.log | grep -q "^enrich: {"; then
  echo "enrich NO terminó bien; post-proceso omitido. Última línea:"; tail -3 data/enrich_full.log; exit 1
fi
tail -1 data/enrich_full.log
uv run gapfinder reclean-readmes
if [ -e data/synthetic_worksheet_2.md ]; then echo "data/synthetic_worksheet_2.md ya existe, no la piso"; exit 0; fi
uv run gapfinder worksheet --n 20 --origins author_comment=10,author_reply=10 --out data/synthetic_worksheet_2.md
