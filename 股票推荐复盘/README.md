# 股票推荐复盘系统

> **目的**：让小助（OpenClaw）对自己列出的股票做长期跟踪、复盘、改进。
> **触发**：何大人 2026-06-24 明确要求，"亏了也要复盘改进策略"。

## 规则

1. **每条推荐跟踪 10 个交易日**（约 2 周），不达标不算完结
2. **每天 15:30 跑复盘**（A 股收盘 30 分钟后）
3. **亏损强制复盘**：平均亏损超过 -3% 必须写入 `改进记录/strategy_improvements.md`
4. **跟踪期满后生成最终报告**（胜率、平均盈亏、判断对错的根因）

## 文件结构

```
股票推荐复盘/
├── README.md                              ← 本文件
├── 跟踪/
│   └── recommendations.json               ← 推荐记录（结构化）
├── 复盘日志/
│   └── recap_log.md                       ← 每日复盘日志
└── 改进记录/
    └── strategy_improvements.md           ← 亏损时的策略反思
```

## 数据源

- 腾讯实时行情接口：`https://qt.gtimg.cn/q={market}{code}`
- 行情字段：`当前价~昨收~今开~成交量~涨跌额~涨跌幅~最高~最低`
- A 股节假日：当前**未处理**（脚本只过滤周末），后续可补

## 自动化

- 复盘 cron：每天 15:30（仅周一至周五）
- 跑完后自动 commit + push 到 GitHub
- 跟踪期满自动标记 `status: completed`

## 当前条目

| ID | 主题 | 推荐日 | 跟踪期 | 状态 |
|---|---|---|---|---|
| 2026-06-24-001 | MLCC 板块 5 只 | 2026-06-24 | 10 交易日 | 跟踪中 |

## 手工命令

```bash
# 看当前跟踪状态
python3 /root/.openclaw/workspace/skills/stock-recap/recap.py --report

# 手动跑一次（不写文件）
python3 /root/.openclaw/workspace/skills/stock-recap/recap.py --dry-run

# 真跑一次
python3 /root/.openclaw/workspace/skills/stock-recap/recap.py
```

## 何大人的核心要求（2026-06-24 原话）

> "你推荐的股票和板块你要自己保存两周时间，这样你自己记录保存的数据然后第二天自己去对比，看看推荐的票是否赚钱了，这样每次推荐的票亏的时候自己也要复盘改进你的策略。"

**自评起点**：今天列 MLCC 板块 5 只股票，本身就是失误（哪怕有免责声明）。这个跟踪系统是补救措施——让未来的小助有据可查。