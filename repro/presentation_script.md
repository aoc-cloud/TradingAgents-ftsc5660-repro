# 录屏操作流程 + 逐字讲稿（精简版，全程约 10 分钟）

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
   cd ~/Projects/ftsc5660-repro/TradingAgents
   .venv/bin/python repro/baseline.py
   ```
   看到最后一行 `mean alpha per cell = +0.17%` 就说明环境就绪。（录制时再跑一遍，跑两次没关系，不花钱）
4. 插好耳机麦克风，试录 10 秒确认声音清晰
5. 把本讲稿放在手机/平板/第二屏幕上看，电脑屏幕留给录制

## 录制流程（打开 Zoom：新建会议 → 共享屏幕 → 选 VSCode 窗口 → 点「录制」→ 选「录制到本机」）

按下面顺序走，每个环节照着讲稿念：

| 环节 | 屏幕操作 | 时间 |
|---|---|---|
| ① 开场 | 切到 report.md 预览，滚到最上方 | 0:00–1:00 |
| ② 怎么做的 | 预览滚到第 2 节 Setup notes | 1:00–2:00 |
| ③ 基线演示 | 切到终端，再跑一次 baseline.py，指着结果讲 | 2:00–3:30 |
| ④ 复现结果 | 切回预览，滚到第 4 节表格 | 3:30–5:30 |
| ⑤ 修改（重头戏） | 滚到第 5 节辩论对比表格 | 5:30–7:30 |
| ⑥ 证据展示 | 切到 trading_memory.md，滚动展示结果表 | 7:30–8:30 |
| ⑦ 踩坑+结论 | 滚到第 6、7 节 | 8:30–9:30 |
| ⑧ 收尾 | 终端敲 git diff 命令展示零改动 | 9:30–10:30 |

录完：停止共享 → 结束会议 → Zoom 自动导出 mp4（一般在 `~/Documents/Zoom/`）→ 检查一遍 → 上传 Zoom 云盘/Google Drive 拿链接。

**备注**：任何环节卡壳了不用慌，停两秒重新念那句就行；实在不想要这段可以整段重录（多录几遍挑最好的）。

---

# 第二部分：逐字讲稿（英文，照着读，约 7 分钟念稿 + 3 分钟操作）

## ① 开场（report.md 顶部）

Hello, I'm CHEN WEIWEN, student ID 1155269941. I will present my
reproducibility work on TradingAgents, a multi-agent LLM trading framework
that mimics a real trading firm. Four analyst agents collect data in
parallel; bull and bear researchers debate; a trader proposes a trade; a
risk team reviews; a portfolio manager gives the final rating.

The paper reports a three-month backtest in early 2024, where the system
earned twenty-six point six percent on Apple while buy-and-hold lost five
point two percent. My target is that claim.

## ② 怎么做的（Setup notes）

I used the current repository with DeepSeek models instead of GPT-4o, as
the assignment's edge case A allows. Same window, same tickers, same
scoring concept. I sampled every fourteen days: seven dates times three
tickers — twenty-one cells. Each decision is scored over five trading days,
with alpha measured against SPY.

## ③ 基线演示（终端跑 baseline.py）

Let me run the buy-and-hold baseline over the same twenty-one cells.

[跑 .venv/bin/python repro/baseline.py，等结果出来，指着最后一行]

The key number: buy-and-hold earns plus zero point one seven percent alpha
per cell, beating the market in only twelve of twenty-one cells.

## ④ 复现结果（第 4 节表格）

My results: eighteen directional calls. Overweight five times, with eighty
percent hit rate. Underweight thirteen times, fifty-four percent. Overall
mean alpha: plus zero point four eight percent per cell — about two point
eight times the buy-and-hold baseline. Sixty-one percent of directional
calls were correct.

So the paper's claim — the system beats buy-and-hold — is directionally
reproduced. The exact twenty-six point six percent is not reproducible: the
repository evolved, the model differs, and the scoring design changed.

## ⑤ 修改：关掉辩论（第 5 节表格）

My modification is an ablation of the debate. The paper claims the bull-bear
debate significantly enhances performance, so I switched debate rounds from
one to zero and changed nothing else.

On the same seven Apple cells: with debate, five Underweight and two Hold —
cautious, because Apple fell eleven percent that quarter — eighty percent
hit rate. Without debate, seven Overweight — confidently bullish — hit rate
twenty-nine percent.

The debate flipped the entire direction of the system, and it created the
Hold option. This is direct evidence for the paper's claim.

## ⑥ 证据展示（trading_memory.md）

These are the real decision logs. Each entry shows the rating and the
actual outcome, plus the full reasoning and a reflection afterwards. That
explainability is exactly what the paper highlights.

[滚动展示几行头部]

## ⑦ 踩坑 + 结论（第 6、7 节）

Two lessons from my debug diary. First, my API balance ran out mid-sweep;
I topped up and resumed with the run-id flag, which skips completed cells,
so nothing was re-spent. Second, historical news for 2024 is mostly
unavailable — live feeds do not archive old posts.

What reproduces: the architecture, the explainability, and the directional
edge. What does not: the exact numbers, for the reasons above.

My advice: pin the repository version and model if you need exact numbers.
Otherwise, compare directional performance on a fixed grid, as I did.

## ⑧ 收尾（终端敲 git diff）

Finally, I did not modify any original code — my contribution is purely
additive.

[敲: git diff --stat upstream/main HEAD | tail -5]

Forty-one files added, zero modified. Thank you for watching.
