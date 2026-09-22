---
title: jianying-headless — 让 Coding Agent 用 JSON 生成可编辑视频草稿
type: project-note
tags: [jianying, capcut, video-automation, coding-agent, alpha-signal, agent-tools]
source: AlphaSignal + 视频介绍（用户提供 URL）
url: https://github.com/mcncarl/jianying-headless
fetched_date: 2026-09-22
status: archived
---

# jianying-headless — 让 Coding Agent 用 JSON 生成可编辑视频草稿

> **⚠️ 仓库路径纠错**
> 
> 用户原话：「项目地址是 github.com/mchenai/jianying-headless」
> 实际仓库：**`github.com/mcncarl/jianying-headless`**（mchenai → mcncarl，可能是 typo）

> **来源**：
> - 视频介绍（用户提供）
> - AlphaSignal 报道：https://alphasignal.ai/news/jianying-headless-lets-coding-agents-build-editable-video-drafts-from-json
> - 抓取日期：2026-09-22

## 一、项目是什么

**source-available Python controller**，通过 Python 脚本生成剪映（Jianying）原生草稿文件 + 调用桌面端本地渲染引擎导出 MP4。

## 二、核心设计

| 组件 | 行为 |
|---|---|
| Interface | Python CLI 脚本 |
| Input | JSON editing plan + 本地媒体 |
| Output | 可编辑剪映草稿 + 可选 `render.mp4` |
| Editing scope | 片段、速度、音量、多轨道、画中画、字幕、标题、背景音乐、音效 |
| License | 个人学习 + 非商业用途；商用需书面授权 |
| Platform | **Apple Silicon macOS 26.0+ + 剪映 Pro 11.4.2**（哈希校验构建，禁止自动降级） |

## 三、关键创新点

#### 1. **草稿即接口**（不是 GUI 自动化）

- 直接写 `draft_content.json` / `draft_mate_info.json`
- **不是模拟鼠标键盘**，而是用剪映原生数据结构
- 剪映打开自动补全 → 用户可在 GUI 里继续编辑

#### 2. **Repo 两天 700+ stars**

- 作者原本计划 888 RMB 卖出
- 反响超出预期后改为开源（个人/非商用）
- 社区生态：跟 Hommy-master/capcut-mate、GuanYixuan/pyJianYingDraft 是同一赛道

#### 3. **架构分离**

- `engine/` — 草稿构造、隔离 working copy、资源校验、原生导出协调
- `bridge/` — 剪映安装库的文件/管道适配器（避免硬编码）

## 四、对 Coding Agent 的价值

* **JSON editing plan** 是 Agent 的天然输入格式
* Agent → jianying-headless → 草稿 → 剪映 GUI 编辑 → MP4
* 实现"agent-first, human-in-the-loop" 视频工作流
* 适合批量视频生产（口播、混剪）

## 五、与何大人的关联

* **短视频自动化**：vault 里有 `公众号文章/` 大量视频相关研究
* **Jev 切入点**：可以加 Jev Noul 决定"本视频是否值得剪"（类似 cron 优先级思路）
* **快速试水**：Apple Silicon 是硬门槛 —— 当前服务器是 Linux x86_64，**无法直接跑**

## 六、关联项目（同赛道）

| 项目 | URL | 备注 |
|---|---|---|
| Hommy-master/capcut-mate | github.com/Hommy-master/capcut-mate | 1.8k stars · FastAPI + 扣子插件 |
| GuanYixuan/pyJianYingDraft | github.com/GuanYixuan/pyJianYingDraft | 0.3.0 · 轻量灵活 |
| xuliang2024/cutcli-cookbook | github.com/topics/jianying-draft | 193 stars · JSON 模板 + AI prompts |
| SkyNotSilent/insightcut-jianying-image-video | github.com/topics/jianying-draft | 119 stars · AI 图片视频工作台 |

## 七、待办（何大人层面）

- [ ] 不投入（Apple Silicon 限制，无法本地跑）
- [ ] 关注社区动态即可
- [ ] 若以后买 M 系列 Mac，优先试这个