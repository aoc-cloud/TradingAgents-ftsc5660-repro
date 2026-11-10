#!/usr/bin/env python
"""Buy-and-hold baseline for the FTEC5660 reproducibility exercise.

Computes, from the same yfinance data the framework's settlement uses:
1. Per-cell 5-trading-day forward return + alpha vs SPY, for the same
   (ticker, date) grid the backtest sweeps, and
2. Full-window B&H cumulative return for the paper's window
   (Jan 1 - Mar 29, 2024) for comparison with paper Table 1.

Usage: .venv/bin/python repro/baseline.py
"""
from __future__ import annotations

import yfinance as yf

TICKERS = ["AAPL", "GOOGL", "AMZN"]
DATES = ["2024-01-02", "2024-01-16", "2024-01-30", "2024-02-13",
         "2024-02-27", "2024-03-12", "2024-03-26"]
HOLDING_DAYS = 5  # must match holding_period_days in the config


def forward_returns(ticker: str, start: str, end: str):
    """Close-to-close returns n trading days ahead, aligned to the framework."""
    df = yf.download(ticker, start=start, end=end, progress=False,
                     auto_adjust=False)
    closes = df["Adj Close"].squeeze().dropna()
    return closes


def main() -> None:
    # Pull the price windows once per ticker: grid window + 5-day settlement
    # tail + the full paper window.
    print(f"Per-cell B&H: {HOLDING_DAYS}-trading-day forward return "
          f"(what buy-and-hold earns over each cell's holding window)\n")
    print(f"{'ticker':<8}{'date':<12}{'fwd ret':>9}{'SPY fwd':>9}{'alpha':>8}")
    per_cell = {}
    for ticker in TICKERS:
        closes = forward_returns(ticker, "2023-11-15", "2024-04-20")
        spy = forward_returns("SPY", "2023-11-15", "2024-04-20")
        for date in DATES:
            if date not in closes.index:
                print(f"{ticker:<8}{date:<12}  (no price on date, non-trading)")
                continue
            i = closes.index.get_loc(date)
            j = i + HOLDING_DAYS
            if j >= len(closes):
                print(f"{ticker:<8}{date:<12}  (holding window out of range)")
                continue
            ret = float(closes.iloc[j] / closes.iloc[i] - 1)
            i_s = spy.index.get_loc(date)
            sret = float(spy.iloc[i_s + HOLDING_DAYS] / spy.iloc[i_s] - 1)
            alpha = ret - sret
            per_cell[(ticker, date)] = (ret, alpha)
            print(f"{ticker:<8}{date:<12}{ret:>+9.2%}{sret:>+9.2%}{alpha:>+8.2%}")
    print()

    print("Full-window B&H (paper window: first close on/after 2024-01-01 "
          "to last close on/before 2024-03-29)")
    print(f"{'ticker':<8}{'B&H CR (ours)':>14}{'paper Table 1':>15}")
    paper_bh = {"AAPL": -5.23, "GOOGL": 7.78, "AMZN": 17.1}
    for ticker in TICKERS:
        closes = forward_returns(ticker, "2023-12-29", "2024-03-29")
        cr = float(closes.iloc[-1] / closes.iloc[0] - 1)
        print(f"{ticker:<8}{cr * 100:>+13.2f}%{paper_bh[ticker]:>+14.2f}%")

    # Aggregates for the report's comparison table
    alphas = [a for _, a in per_cell.values()]
    if alphas:
        mean_alpha = sum(alphas) / len(alphas)
        hits = sum(1 for a in alphas if a > 0)
        print(f"\nB&H per-cell aggregate: mean alpha {mean_alpha:+.2%}, "
              f"{hits}/{len(alphas)} cells beat SPY over their holding window")


if __name__ == "__main__":
    main()
