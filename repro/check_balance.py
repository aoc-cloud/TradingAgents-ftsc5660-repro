#!/usr/bin/env python
"""
Check the DeepSeek account balance.

Why this exists: during the reproduction sweep our balance ran out
mid-run (HTTP 402 Insufficient Balance) and 14 of 21 cells failed.
Before launching more sweeps, we check the balance with this script.

It reads the API key from .env (never prints it) and asks DeepSeek's
balance endpoint how much money is left.

Usage: .venv/bin/python repro/check_balance.py
"""

import json
import os
import urllib.request

from dotenv import load_dotenv

# Read the API key from the .env file in the repository root.
# (load_dotenv adds the .env values to the environment variables.)
load_dotenv(".env")
key = os.environ.get("DEEPSEEK_API_KEY", "")

if not key:
    print("DEEPSEEK_API_KEY not found in .env")
    raise SystemExit(1)

# Ask DeepSeek: GET https://api.deepseek.com/user/balance
request = urllib.request.Request(
    "https://api.deepseek.com/user/balance",
    headers={"Authorization": f"Bearer {key}"},
)
with urllib.request.urlopen(request) as response:
    data = json.loads(response.read())

# Example reply:
#   {"is_available": true, "balance_infos": [
#       {"currency": "CNY", "total_balance": "47.50", ...}]}
print(json.dumps(data, indent=2))
