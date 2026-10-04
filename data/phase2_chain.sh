#!/bin/zsh
# Fase 2: espera embeddings del corpus + búsqueda dirigida, embebe lo dirigido y corre el eval.
cd "$(dirname "$0")/.."
while pgrep -f "gapfinder (embed|targeted)" >/dev/null; do sleep 60; done
grep -q "^targeted: {" data/targeted.log || { echo "targeted no terminó bien"; tail -3 data/targeted.log; exit 1; }
uv run gapfinder embed --model all --index corpus targeted || exit 1   # corpus: completa bloques faltantes si los hubiera
uv run gapfinder eval
