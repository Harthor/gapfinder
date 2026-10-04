#!/bin/zsh
# Iteración 2: prelim con MiniLM cuando está BM25; final con MiniLM + bge cuando termina bge.
cd "$(dirname "$0")/.."
while pgrep -f bm25_precompute >/dev/null; do sleep 60; done
grep -q "precompute: listo" data/bm25_precompute.log || { echo "bm25 precompute no terminó"; exit 1; }
uv run gapfinder eval2 --model minilm --out data/eval/prelim_minilm || exit 1
echo "PRELIM LISTO $(date +%T)"
while pgrep -f "gapfinder embed --model bge" >/dev/null; do sleep 120; done
uv run gapfinder embed --model bge --index corpus targeted || exit 1   # corpus: completa bloques si faltara alguno
uv run gapfinder eval2 || exit 1
echo "FINAL LISTO $(date +%T)"
