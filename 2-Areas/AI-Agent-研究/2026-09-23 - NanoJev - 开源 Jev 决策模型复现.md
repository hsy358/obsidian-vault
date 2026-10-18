---
type: document-metadata
title: "NanoJev - 开源 Jev 决策模型复现"
description: "0.6B 并行决策模型，基于 Qwen3-0.6B，零 token 解码直接输出概率分布"
source: https://github.com/TianyuCodings/NanoJev
uploaded_date: 2026-09-23
tags: [AI-Agent, 决策模型, Jev, 开源, Qwen3, 强化学习, RLCD]
---

# NanoJev — 开源 Jev 决策模型复现

**仓库**: https://github.com/TianyuCodings/NanoJev
**模型**: https://huggingface.co/C-Tianyu/NanoJev
**数据**: https://huggingface.co/datasets/C-Tianyu/NanoJev-Data
**论文**: 对应 Typesafe Jev (https://typesafe.ai/blog/introducing-system-one-models-and-jev)

## 核心定位

Jev（Typesafe 闭源）的开源复现：**状态+问题 → 完整概率分布，零 token 解码**。

底座只用 Qwen3-0.6B，一次前向并行批处理多个状态、多个问题，动态候选 2–255 个，支持 Choice / Boolean / Score 三类结构化决策。

## 技术架构

- **Backbone**: Qwen3-0.6B + decision heads
- **决策类型**:
  - `Choice`: 2–255 候选的 softmax 概率分布
  - `Boolean`: 命题的 sigmoid 概率
  - `Score`: 2–10 有序等级的期望概率
- **训练**: 混合任务 SFT，权重 Maze 1/3 + Snake 1/3 + Basic 1/6 + Predict Position 1/6
- **数据集**: 每 variant 18,760 条决策问题，含 16,333 条 ViZDoom 问题

## 实测对比（274-case 测试集）

| 模型 | Maze (10) | Snake (8) | Basic (128) | Predict Position (128) |
|---|---|---|---|---|
| **NanoJev** | **4/10** | **8/8** | **128/128** | **27/128** |
| 原版 Jev (闭源) | 7/10 | 8/8 | 56/128 | 11/128 |
| 未调优 Qwen3-0.6B | 2/10 | 0/8 | 56/128 | 11/128 |

**关键发现**: NanoJev 在 Basic 和 Predict Position 上**超越**原版 Jev，Snake 全胜。闭源 Jev 的 Maze 略强（7 vs 4）。

## 快速开始

```bash
git clone https://github.com/TianyuCodings/NanoJev.git
cd NanoJev
pip install -r requirements-toy.txt huggingface_hub

# 下载模型
python -c "
from huggingface_hub import snapshot_download
snapshot_download(repo_id='C-Tianyu/NanoJev', revision='unified-games-v1',
                  local_dir='checkpoints/NanoJev-unified',
                  allow_patterns=['best.safetensors', 'config.json', 'tokenizer/*', 'backbone_config/*'])
"

# 启动推理服务（需 CUDA）
python scripts/serve_decisions.py --checkpoint-dir checkpoints/NanoJev-unified --port 8765
# POST http://127.0.0.1:8765/api/evaluate
```

## 局限与 Roadmap

- [x] 单一 checkpoint 通吃 4 个游戏
- [x] 50×50 迷宫 225 步到达终点
- [ ] RLCD post-training（更广泛的长程任务）
- [ ] 共享前缀推理 + 更大候选批次
- [ ] 更广泛射击场景

**注意**: 需要 GPU 才能跑量化推理，CPU 不可行（0.6B 模型但无 CUDA 加速）

## 与 OpenClaw 的关系

- OpenClaw 当前用的是 **Typesafe API 的闭源 Jev**（`beacon memory evaluations run` 调用 `api.typesafe.ai`）
- NanoJev 可作为**本地替代**，延迟和成本更低
- Beacon 的 Jev 引擎架构支持自定义 endpoint（`--jev-endpoint`），可对接 NanoJev 本地服务
- **整合路径**: `beacon memory evaluations run --jev-endpoint http://127.0.0.1:8765`

## 关键链接

- Demo: https://nanojev-dev.tianyuchen99.chatgpt.site/?autoplay=1
- 项目主页: GitHub 仓库内含完整文档
