#!/usr/bin/env python
"""
Buy-and-hold baseline for the FTEC5660 reproducibility exercise.

What this script does:
  1. For each (ticker, date) cell in our backtest grid, it looks up the
     stock's price 5 trading days later and computes the buy-and-hold return
     ("if you just bought and did nothing, what would you earn?").
  2. It does the same for SPY (the market benchmark), and subtracts it.
     The difference is the "alpha": how much better/worse the stock did
     than the market over that holding window.
  3. It also computes the full-window buy-and-hold return (2024 Q1), to
     compare with the paper's Table 1 baseline numbers.

Why: the backtest scores TradingAgents decisions the same way (5 trading
days, compared against SPY), so this gives us the fair "what would a
buy-and-hold investor have earned" numbers to compare against.

Usage: .venv/bin/python repro/baseline.py
"""

import yfinance

# These three stocks and seven dates are the exact same grid that
# repro/run_backtest.sh runs the agents on. Keep them in sync.
TICKERS = ["AAPL", "GOOGL", "AMZN"]
DATES = ["2024-01-02", "2024-01-16", "2024-01-30", "2024-02-13",
         "2024-02-27", "2024-03-12", "2024-03-26"]

# The framework scores each decision over 5 trading days after it is made.
# This must match holding_period_days in the framework's config.
HOLDING_DAYS = 5

# The paper's Table 1 reports these buy-and-hold numbers for the full
# window (2024-01-01 to 2024-03-29).
PAPER_BUY_AND_HOLD = {"AAPL": -5.23, "GOOGL": 7.78, "AMZN": 17.1}


def download_closes(ticker: str, start: str, end: str):
    """Download daily closing prices for one ticker from Yahoo Finance.

    Returns a list of (date, price) pairs, oldest first.
    yfinance gives us a table; we keep only the adjusted close column,
    which accounts for dividends and splits (so returns are fair).
    """
    df = yfinance.download(ticker, start=start, end=end,
                           progress=False, auto_adjust=False)
    # .squeeze() turns a one-column table into a simple series of values
    # .dropna() removes any days with missing prices (holidays etc.)
    closes = df["Adj Close"].squeeze().dropna()
    return list(closes.items())  # [(date, price), (date, price), ...]


def find_index_of_date(prices, target_date):
    """Find where target_date sits in the price list, or None if missing."""
    for i, (date, _price) in enumerate(prices):
        if str(date.date()) == target_date:
            return i
    return None


def compute_cell_return(prices, spy_prices, target_date):
    """Compute one grid cell: 5-day return, 5-day SPY return, alpha.

    Returns (return, alpha) or None if the date or holding window is missing.
    """
    i = find_index_of_date(prices, target_date)
    i_spy = find_index_of_date(spy_prices, target_date)
    if i is None or i_spy is None:
        return None  # e.g. a holiday, not a trading day

    j = i + HOLDING_DAYS          # 5 trading days later
    j_spy = i_spy + HOLDING_DAYS
    if j >= len(prices) or j_spy >= len(spy_prices):
        return None  # not enough future data to score this cell

    stock_return = prices[j][1] / prices[i][1] - 1
    spy_return = spy_prices[j_spy][1] / spy_prices[i_spy][1] - 1
    alpha = stock_return - spy_return
    return stock_return, alpha


def main():
    # --- Part 1: per-cell buy-and-hold (same cells as the agent backtest) ---
    # Fetch a price window that covers the grid plus the 5-day holding tail.
    # (The grid starts 2024-01-02, so start a bit earlier for safety.)
    spy_prices = download_closes("SPY", "2023-11-15", "2024-04-20")

    print(f"Per-cell buy-and-hold over {HOLDING_DAYS} trading days")
    print("(what you earn by buying on each analysis date and doing nothing)")
    print()
    print(f"{'ticker':<8}{'date':<12}{'5d return':>10}{'SPY 5d':>9}{'alpha':>9}")

    all_alphas = []
    for ticker in TICKERS:
        prices = download_closes(ticker, "2023-11-15", "2024-04-20")
        for date in DATES:
            result = compute_cell_return(prices, spy_prices, date)
            if result is None:
                print(f"{ticker:<8}{date:<12}  (missing data, skipped)")
                continue
            stock_return, alpha = result
            all_alphas.append(alpha)
            # e.g. +4.20% means the stock beat SPY by 4.20 points over 5 days
            print(f"{ticker:<8}{date:<12}{stock_return:>+9.2%}"
                  f"{stock_return - alpha:>+9.2%}{alpha:>+9.2%}")

    # --- Part 2: full-window buy-and-hold vs the paper's Table 1 ---
    print()
    print("Full-window buy-and-hold (2024 Q1, same window as paper Table 1)")
    print(f"{'ticker':<8}{'B&H (ours)':>12}{'paper Table 1':>15}")
    for ticker in TICKERS:
        # First trading day of 2024 to last trading day of March 2024.
        prices = download_closes(ticker, "2023-12-29", "2024-03-29")
        first_price = prices[0][1]
        last_price = prices[-1][1]
        cr = last_price / first_price - 1  # cumulative return
        print(f"{ticker:<8}{cr * 100:>+11.2f}%"
              f"{PAPER_BUY_AND_HOLD[ticker]:>+14.2f}%")

    # --- Part 3: one-number summary for the report ---
    if all_alphas:
        mean_alpha = sum(all_alphas) / len(all_alphas)
        wins = sum(1 for a in all_alphas if a > 0)
        print(f"\nBuy-and-hold summary: mean alpha per cell = "
              f"{mean_alpha:+.2%}, beat SPY in {wins}/{len(all_alphas)} cells")


if __name__ == "__main__":
    main()
