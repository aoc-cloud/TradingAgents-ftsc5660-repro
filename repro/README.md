# FTEC5660 Reproducibility Work — TradingAgents

Reproducing one reported result of **TradingAgents: Multi-Agents LLM Financial
Trading Framework** (arXiv:2412.20138), plus one well-scoped modification.

Student ID: 1155269941 CHEN WEIWEN

## What I tried to reproduce

Paper Table 1 reports a 3-month backtest (2024-01-01 to 2024-03-29) of the
TradingAgents framework (GPT-4o) against buy-and-hold and rule-based baselines
on AAPL, GOOGL and AMZN:

| Metric                          | AAPL   | GOOGL  | AMZN   |
| ------------------------------- | ------ | ------ | ------ |
| TradingAgents cumulative return | 26.62% | 24.36% | 23.21% |
| Buy-and-hold cumulative return  | -5.23% | 7.78%  | 17.1%  |

**Target claim:** TradingAgents outperforms buy-and-hold on all three tickers
over the paper's window.

## Setup

```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
uv venv --python 3.14 && source .venv/bin/activate
uv pip install .
cp .env.example .env     
```

Optional but recommended on macOS (fixes TLS for the social-data fetchers):

```bash
export SSL_CERT_FILE="$PWD/.venv/lib/python3.14/site-packages/certifi/cacert.pem"
```

## Runs

Single analysis (smoke test):

```bash
repro/run_single.sh AAPL 2024-01-02
```

Reproduction sweep — the paper's window, sampled every 14 days
(7 dates × 3 tickers = 21 cells):

```bash
repro/run_backtest.sh                  # DEBATE=1 (default)
```

Modification sweep — research debate disabled (ablation):

```bash
DEBATE=0 repro/run_backtest.sh
```

Buy-and-hold baseline over the same cells and window:

```bash
.venv/bin/python repro/baseline.py
```

All outputs land in `repro_results/backtest/<run_id>/` — the decision log
(`trading_memory.md`) is the results table, with per-run reports under
`reports/`.

## Metric definitions

- **Rating**: each cell's final decision (Buy / Overweight / Hold /
  Underweight / Sell) from the Portfolio Manager.
- **Hit rate**: fraction of directional cells whose 5-trading-day forward
  return (first close after the analysis date) matched the direction of the
  rating, computed against the regional benchmark (SPY).
- **Mean alpha**: mean of (ticker 5-day forward return − SPY 5-day forward
  return) per rating.
- **Baseline**: buy-and-hold 5-day forward return over the same cells,
  computed from the same yfinance data in `repro/baseline.py`.

## Settings recorded

- Provider: `deepseek`, base URL `https://api.deepseek.com`
- Quick tier (analysts/researchers/trader): `deepseek-flash`
- Deep tier (managers): `deepseek-v4-pro`
- temperature 0.0, debate rounds 1, risk rounds 1, holding period 5 days
- Analysts: market, sentiment, news, fundamentals
- Data vendors: yfinance (prices/news/technical), SEC EDGAR (fundamentals),
  FRED (macro — unavailable, no key), Polymarket (prediction markets)

## Modification

**Ablation: research debate disabled** (`max_debate_rounds` 1 → 0). The paper
claims the bull/bear researcher debate "significantly enhances trading
performance" — I remove exactly that step and measure the change in hit rate
and mean alpha on the identical AAPL cells.

## Debug diary (highlights)

- `SSL: CERTIFICATE_VERIFY_FAILED` on StockTwits/Reddit fetches (macOS
  python.org build): fixed with `SSL_CERT_FILE` pointing at certifi's bundle.
- `FRED_API_KEY` not set: macro tools degrade gracefully to unavailable.
- Trader structured-output invocation retried once as free text on the smoke
  run (transient, self-recovered).
- Paper's B&H baseline for AAPL (-5.23%) does not match yfinance adj-close
  B&H for the same window (-10.8%): GOOGL/AMZN match within ~1.5pp, so the
  paper's AAPL figure likely used a different start convention or data vendor.

## Results (summary)

Reproduction, 21 cells (7 dates × AAPL/GOOGL/AMZN, DeepSeek):

| Rating      | n   | direction hit rate | mean alpha vs SPY |
| ----------- | --- | ------------------ | ----------------- |
| Overweight  | 5   | 80%                | +0.92%            |
| Underweight | 13  | 54%                | +0.60%            |
| Hold        | 3   | —                  | -0.80%            |

Weighted mean alpha **+0.48%/cell** vs buy-and-hold **+0.17%/cell**
(≈2.8×). Modification (debate OFF, same 7 AAPL cells): ratings flipped to
Overweight 7/7, hit rate fell 80% → 29%. Full write-up in `repro/report.md`;
per-run details in `repro_results/backtest/<run_id>/trading_memory.md`.
