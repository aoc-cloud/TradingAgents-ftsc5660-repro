# 录屏操作流程 + 逐字讲稿（≤15 分钟）

---

# 第一部分：操作流程（录制前看，按顺序做）

## 开录前准备（约 10 分钟）

1. 关闭所有无关应用（微信、音乐等），开勿扰模式，避免弹通知
2. 打开 VSCode，打开这三个文件（`Cmd+O` 依次打开）：
   - `repro/report.md` → 按 `Cmd+Shift+V` 打开预览（这个预览就是你的「幻灯片」）
   - `repro_results/backtest/20261110_184102/trading_memory.md`（复现结果表）
   - `repro_results/backtest/20261111_001111/trading_memory.md`（消融结果表）
3. 打开 VSCode 终端（`Ctrl + `` `），**先试跑一遍**基线（确认有网、能出结果）：
   ```bash
   .venv/bin/python repro/baseline.py
   ```
   看到最后一行 `mean alpha per cell = +0.17%` 就说明环境就绪。（录制时再跑一遍，跑两次没关系，不花钱）
4. 插好耳机麦克风，试录 10 秒确认声音清晰
5. 把本讲稿放在手机/平板/第二屏幕上看，电脑屏幕留给录制

## 录制流程（打开 Zoom：新建会议 → 共享屏幕 → 选 VSCode 窗口 → 点「录制」→ 选「录制到本机」）

按下面顺序走，每个环节照着讲稿念：

| 环节 | 屏幕操作 | 时间 |
|---|---|---|
| ① 开场 | 切到 report.md 预览，滚到最上方 | 0:00–1:30 |
| ② 怎么做的 | 预览滚到第 2 节 Setup notes | 1:30–4:00 |
| ③ 基线演示 | 切到终端，再跑一次 baseline.py，指着结果讲 | 4:00–5:30 |
| ④ 复现结果 | 切回预览，滚到第 4 节表格 | 5:30–8:00 |
| ⑤ 修改（重头戏） | 滚到第 5 节辩论对比表格 | 8:00–10:30 |
| ⑥ 证据展示 | 切到 trading_memory.md，滚动展示结果表 | 10:30–11:30 |
| ⑦ 踩坑+结论 | 滚到第 6、7 节 | 11:30–13:30 |
| ⑧ 收尾 | 终端敲 git diff 命令展示零改动 | 13:30–14:30 |

录完：停止共享 → 结束会议 → Zoom 自动导出 mp4（一般在 `~/Documents/Zoom/`）→ 检查一遍 → 上传 Zoom 云盘/Google Drive 拿链接。

**备注**：任何环节卡壳了不用慌，停两秒重新念那句就行；实在不想要这段可以整段重录（多录几遍挑最好的）。

---

# 第二部分：逐字讲稿（英文，照着读，约 13 分钟）

## ① 开场（report.md 顶部）

Hello, I'm CHEN WEIWEN, student ID 1155269941. Today I will present my
reproducibility work on TradingAgents, a multi-agent LLM financial trading
framework.

TradingAgents mimics a real trading firm. Four analyst agents — market,
sentiment, news, and fundamentals — collect data in parallel. Then bull and
bear researchers debate the reports. A trader proposes a trade. A risk team
reviews it. Finally, a portfolio manager issues the final rating.

The paper reports a three-month backtest, from January to March 2024, on
Apple, Google and Amazon. Powered by GPT-4o, the system earned twenty-six
point six percent on Apple, while buy-and-hold lost five point two percent.

My target claim is paper Table 1: the system beats buy-and-hold on all three
tickers.

## ② 怎么做的（Setup notes）

Here is what I did. Because the original GPT-4o model is not available to
me, I followed the assignment's edge case A and switched the model to
DeepSeek. I kept the same window, the same tickers, and the same scoring
concept. So my results are not directly comparable to the paper, but the
comparison is as fair as possible.

I sampled the paper's window every fourteen days: seven dates times three
tickers, twenty-one cells in total. Each cell runs the full pipeline and
produces one rating. I scored every decision over a five-trading-day holding
period, measuring alpha against SPY, the market benchmark.

I used deepseek-flash for the analyst tier and deepseek-v4-pro for the
manager tier, with temperature zero. The repository version is zero point
seven point one.

## ③ 基线演示（终端跑 baseline.py）

Let me quickly show the baseline. This script computes what buy-and-hold
would earn over the same twenty-one cells. I will run it now.

[跑 .venv/bin/python repro/baseline.py，等结果出来]

This is the same twenty-one-cell grid. The last line is the key number:
buy-and-hold earns a mean alpha of plus zero point one seven percent per
cell, and beats the market in only twelve of twenty-one cells. This is the
number my reproduction compares against.

## ④ 复现结果（第 4 节表格）

Here are my results. The system made eighteen directional calls. Five were
Overweight, with an eighty percent hit rate and plus zero point nine two
percent mean alpha. Thirteen were Underweight, fifty-four percent hit rate,
plus zero point six percent. Three were Hold.

Overall, the system's mean alpha per cell was plus zero point four eight
percent — that is roughly two point eight times the buy-and-hold baseline.
Sixty-one percent of its directional calls were correct.

So the paper's headline claim is directionally reproduced: the multi-agent
system beats buy-and-hold on these tickers in Q1 2024.

But the exact magnitude, twenty-six point six percent, is not reproducible.
There are three reasons. First, the repository has evolved far beyond the
paper version. Second, the model differs. Third, the paper simulates a daily
trading portfolio, while the current harness scores independent five-day
calls. The repository's own README warns that backtest results are not
guaranteed to match published figures.

## ⑤ 修改：关掉辩论（第 5 节表格）

My modification is an ablation. The paper claims the bull-bear debate
significantly enhances performance. So I removed the debate by changing one
setting: debate rounds from one to zero. Everything else stayed identical.

The results are striking. With the debate on, the system rated Apple as
Underweight five times and Hold twice — cautious, because Apple fell eleven
percent in that quarter. Its direction hit rate was eighty percent.

With the debate off, every single cell became Overweight. The system turned
confidently bullish, and its hit rate collapsed to twenty-nine percent.

So the debate flipped the entire direction of the system's judgement, and it
also created the Hold option. Without debate, the system never chose to do
nothing.

This is direct evidence for the paper's claim: on this ticker and window,
the debate was the difference between correctly cautious and confidently
wrong.

## ⑥ 证据展示（trading_memory.md）

These are the real decision logs. Each entry starts with the date, the
ticker, the rating, the return, and the alpha. Below each entry is the full
reasoning — the executive summary, the investment thesis, and a reflection
after the outcome. This is the explainability the paper highlights.

[滚动展示几行]

## ⑦ 踩坑 + 结论（第 6、7 节）

I kept a debug diary, and two entries are worth mentioning. First, my
DeepSeek balance ran out in the middle of the sweep, so fourteen cells
failed. I topped up the account and resumed with the run-id flag, which
skips completed cells — nothing was re-spent. Second, historical news and
social data for 2024 are mostly unavailable, because live feeds do not
archive old posts. This is a real limit of reproducibility.

My conclusions. What reproduces: the architecture and the end-to-end
pipeline work exactly as described, and decisions are explainable. The
directional performance also reproduces: the system beat buy-and-hold by a
clear margin.

What does not reproduce: the exact return numbers, for the reasons I
explained — and the authors themselves warn about this.

My recommendation to future users: pin the repository version and the model
if you need exact numbers. Otherwise, treat the framework as a research
scaffold, and compare directional performance on a fixed grid, as I did.

## ⑧ 收尾（终端敲 git diff）

One last thing. I did not modify any of the original code. My whole
contribution is additive. Let me show the diff against the upstream
repository.

[敲: git diff --stat upstream/main HEAD | tail -5]

Forty-one files added, zero modified. All my changes are new scripts,
results, and this report.

Thank you for watching. The GitHub link and the report are in the
submission.
