#!/usr/bin/env bash
# Reproduction sweep: repro/run_backtest.sh  (debate ON)
# Modification sweep:  DEBATE=0 repro/run_backtest.sh  (debate OFF)
set -euo pipefail

cd "$(dirname "$0")/.."

DEBATE="${DEBATE:-1}"       # the modification switch
TICKERS="${TICKERS:-AAPL,GOOGL,AMZN}"

export TRADINGAGENTS_LLM_PROVIDER=deepseek
export TRADINGAGENTS_QUICK_THINK_LLM=deepseek-flash
export TRADINGAGENTS_DEEP_THINK_LLM=deepseek-v4-pro
export TRADINGAGENTS_OUTPUT_LANGUAGE=English
export TRADINGAGENTS_MAX_DEBATE_ROUNDS="$DEBATE"
export TRADINGAGENTS_MAX_RISK_ROUNDS=1
export TRADINGAGENTS_TEMPERATURE=0.0
export TRADINGAGENTS_NO_UPDATE_CHECK=1
export TRADINGAGENTS_RESULTS_DIR="$PWD/repro_results"
export SSL_CERT_FILE="$PWD/.venv/lib/python3.14/site-packages/certifi/cacert.pem"  # macOS TLS fix

.venv/bin/tradingagents backtest "$TICKERS" \
  --start 2024-01-02 --end 2024-03-26 --every 14 \
  --analysts market,sentiment,news,fundamentals \
  "$@"
