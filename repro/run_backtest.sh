#!/usr/bin/env bash
# Backtest sweep for the FTEC5660 reproducibility assignment.
# Reproduction sweep: DEBATE=1 (default). Ablation sweep: DEBATE=0.
# Usage: repro/run_backtest.sh [DEBATE=0|1] [--run-id ID] [extra flags...]
set -euo pipefail

cd "$(dirname "$0")/.."

DEBATE="${DEBATE:-1}"

export TRADINGAGENTS_LLM_PROVIDER=deepseek
export TRADINGAGENTS_QUICK_THINK_LLM=deepseek-flash
export TRADINGAGENTS_DEEP_THINK_LLM=deepseek-v4-pro
export TRADINGAGENTS_OUTPUT_LANGUAGE=English
export TRADINGAGENTS_MAX_DEBATE_ROUNDS="$DEBATE"
export TRADINGAGENTS_MAX_RISK_ROUNDS=1
export TRADINGAGENTS_TEMPERATURE=0.0
export TRADINGAGENTS_NO_UPDATE_CHECK=1
export TRADINGAGENTS_RESULTS_DIR="$PWD/repro_results"
# macOS python.org builds can fail TLS verification for urllib fetchers
# (StockTwits/Reddit); point SSL at certifi's CA bundle (debug diary item).
export SSL_CERT_FILE="$PWD/.venv/lib/python3.14/site-packages/certifi/cacert.pem"

# Paper's backtest window (Jan 1 - Mar 29, 2024), sampled every 14 days.
# 7 dates x 3 tickers = 21 cells per sweep.
.venv/bin/tradingagents backtest AAPL,GOOGL,AMZN \
  --start 2024-01-02 --end 2024-03-26 --every 14 \
  --analysts market,sentiment,news,fundamentals \
  "$@"
