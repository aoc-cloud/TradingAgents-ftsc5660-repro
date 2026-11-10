#!/usr/bin/env bash
# =============================================================================
# Backtest sweep for the FTEC5660 reproducibility assignment.
#
# What this does: tells the TradingAgents framework to run its full
# multi-agent analysis on every (ticker, date) cell in a grid, then score
# each decision against what the market actually did afterwards.
#
# Two modes (same grid, same models — only one setting changes):
#   repro/run_backtest.sh            -> normal run (debate ON)  = reproduction
#   DEBATE=0 repro/run_backtest.sh   -> debate OFF              = modification
#
# The env vars below are the framework's settings. They answer the CLI's
# questions in advance so the run needs no keyboard input.
# =============================================================================
set -euo pipefail

# Make sure we run from the repository root, no matter where we are called from.
cd "$(dirname "$0")/.."

# Debate rounds: 1 by default; set DEBATE=0 to remove the research debate.
DEBATE="${DEBATE:-1}"
# Which stocks to sweep: all three by default; e.g. TICKERS=AAPL for a
# cheaper single-ticker sweep (used for the AAPL-only ablation).
TICKERS="${TICKERS:-AAPL,GOOGL,AMZN}"

# --- Framework settings (documented in the report) --------------------------
export TRADINGAGENTS_LLM_PROVIDER=deepseek          # which LLM provider
export TRADINGAGENTS_QUICK_THINK_LLM=deepseek-flash # analysts/trader model
export TRADINGAGENTS_DEEP_THINK_LLM=deepseek-v4-pro # manager model
export TRADINGAGENTS_OUTPUT_LANGUAGE=English
export TRADINGAGENTS_MAX_DEBATE_ROUNDS="$DEBATE"    # <- the modification
export TRADINGAGENTS_MAX_RISK_ROUNDS=1              # risk debate stays on
export TRADINGAGENTS_TEMPERATURE=0.0                # as deterministic as possible
export TRADINGAGENTS_NO_UPDATE_CHECK=1
export TRADINGAGENTS_RESULTS_DIR="$PWD/repro_results"  # save outputs here

# macOS fix: without this, the StockTwits/Reddit fetchers fail TLS
# verification (debug diary item). Points SSL at certifi's CA bundle.
export SSL_CERT_FILE="$PWD/.venv/lib/python3.14/site-packages/certifi/cacert.pem"

# The grid: the paper's backtest window (2024 Q1), sampled every 14 days.
# 3 tickers x 7 dates = 21 cells. The framework scores each decision over
# the 5 trading days after the analysis date, against SPY.
.venv/bin/tradingagents backtest "$TICKERS" \
  --start 2024-01-02 --end 2024-03-26 --every 14 \
  --analysts market,sentiment,news,fundamentals \
  "$@"
