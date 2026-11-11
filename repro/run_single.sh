#!/usr/bin/env bash
# One full analysis: repro/run_single.sh <TICKER> <DATE> [analysts]
set -euo pipefail

cd "$(dirname "$0")/.."

TICKER="${1:?ticker required}"
DATE="${2:?date required (YYYY-MM-DD)}"
ANALYSTS="${3:-market,news,fundamentals}"

export TRADINGAGENTS_LLM_PROVIDER=deepseek
export TRADINGAGENTS_QUICK_THINK_LLM=deepseek-flash
export TRADINGAGENTS_DEEP_THINK_LLM=deepseek-v4-pro
export TRADINGAGENTS_OUTPUT_LANGUAGE=English
export TRADINGAGENTS_MAX_DEBATE_ROUNDS=1
export TRADINGAGENTS_MAX_RISK_ROUNDS=1
export TRADINGAGENTS_TEMPERATURE=0.0
export TRADINGAGENTS_NO_UPDATE_CHECK=1
export TRADINGAGENTS_RESULTS_DIR="$PWD/repro_results"
export SSL_CERT_FILE="$PWD/.venv/lib/python3.14/site-packages/certifi/cacert.pem"  # macOS TLS fix

.venv/bin/tradingagents \
  --ticker "$TICKER" \
  --date "$DATE" \
  --analysts "$ANALYSTS" \
  --save --no-show --no-html
