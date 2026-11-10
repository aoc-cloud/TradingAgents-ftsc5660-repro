#!/usr/bin/env bash
# =============================================================================
# Single-analysis smoke test (one ticker, one date, one full pipeline run).
#
# Usage: repro/run_single.sh <TICKER> <DATE> [analysts]
#   e.g. repro/run_single.sh AAPL 2024-01-02
#   e.g. repro/run_single.sh NVDA 2024-01-02 market,news,fundamentals
#
# What this does: runs ONE full analysis (all agent teams, one decision,
# saved as a report). Use it to check the pipeline works before launching
# the 21-cell backtest sweep in run_backtest.sh.
# =============================================================================
set -euo pipefail

cd "$(dirname "$0")/.."

# First two arguments are required: which stock, and which analysis date.
TICKER="${1:?ticker required}"
DATE="${2:?date required (YYYY-MM-DD)}"
# Third argument is optional: which analyst teams to run (comma-separated).
ANALYSTS="${3:-market,news,fundamentals}"

# Same framework settings as run_backtest.sh (see comments there).
export TRADINGAGENTS_LLM_PROVIDER=deepseek
export TRADINGAGENTS_QUICK_THINK_LLM=deepseek-flash
export TRADINGAGENTS_DEEP_THINK_LLM=deepseek-v4-pro
export TRADINGAGENTS_OUTPUT_LANGUAGE=English
export TRADINGAGENTS_MAX_DEBATE_ROUNDS=1
export TRADINGAGENTS_MAX_RISK_ROUNDS=1
export TRADINGAGENTS_TEMPERATURE=0.0
export TRADINGAGENTS_NO_UPDATE_CHECK=1
export TRADINGAGENTS_RESULTS_DIR="$PWD/repro_results"   # save reports here
export SSL_CERT_FILE="$PWD/.venv/lib/python3.14/site-packages/certifi/cacert.pem"

# --save: write the report to disk   --no-show: don't open the live UI
# --no-html: skip the extra HTML page, the markdown report is enough
.venv/bin/tradingagents \
  --ticker "$TICKER" \
  --date "$DATE" \
  --analysts "$ANALYSTS" \
  --save --no-show --no-html
