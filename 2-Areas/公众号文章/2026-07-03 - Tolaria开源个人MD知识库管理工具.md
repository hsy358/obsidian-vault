---
title: "Tolaria：开源的个人 MD 知识库管理工具"
author: "Ranger Ramblings"
publish_date: "2026-06-11 18:48:03"
saved_date: "2026-07-03"
source: "wechat"
url: "https://mp.weixin.qq.com/s/ZsyZfOlqop2BFtiZhf_7Pg"
---
# Tolaria：开源的个人 MD 知识库管理工具
![](https://mmbiz.qpic.cn/sz_mmbiz_png/icK8n7FWvkD8ZI2wAN7ia9vTNMAk0GvGibcm5JibXFlyRag6WYibVP3u3Q1DMJaQ2FtaGibyAN4RpXYKooCqEsk359zOjQfqDUMErdfUPcNO62OTY/640?wx_fmt=png&from=appmsg)

## 一、项目简介

**Tolaria** 是一款跨平台（macOS / Windows / Linux）桌面应用，专为管理 **Markdown 知识库**（Knowledge Base / Second Brain）而设计。

它由 Luca Rosini[1] 开发，作者本人用它管理一个超过 10,000 条笔记的个人知识库，并每天使用它"运营自己的人生"。

## 二、核心设计理念

原则

说明

**文件优先**笔记是纯 Markdown 文件，可用任何编辑器打开，无需导出步骤，数据属于你

**Git 优先**每个知识库都是 Git 仓库，自带完整版本历史，支持任意 Git 远端

**离线优先，零锁定**无需账号、无订阅、无云端依赖，完全离线工作，随时可离开

**开源**完全开源，AGPL-3.0 授权

**标准格式**笔记使用标准 Markdown + YAML frontmatter，无私有格式

**类型即导航**类型是查找笔记的辅助分类，不是强制 Schema，无必填字段

**AI 优先，但不强依赖 AI**支持 Claude Code、Codex CLI、Gemini CLI 等主流 AI 代理

⌨ **键盘优先**

为注重效率的用户设计，Command Palette 覆盖所有操作

**源自真实使用**所有功能都来自真实痛点

## 三、解决了什么问题

### 传统笔记工具的痛点

- 1. **数据锁定**：Notion、Roam Research 等工具将数据存在云端，导出困难，格式私有
- 2. **无版本控制**：修改后无法回溯，协作冲突难以处理
- 3. **依赖云服务**：断网无法使用，服务商关闭则数据风险极高
- 4. **AI 集成不自然**：传统工具对 AI 代理不友好，知识库结构无法被 AI 有效理解

### Tolaria 的解决方案

- • **Markdown + Git** = 完全可移植的知识库，配合任意远端（GitHub、GitLab、Gitea 等）
- • **结构化 frontmatter** = AI 可理解的知识图谱节点
- • **本地优先** = 无账号、无服务商、无断网恐惧
- • **MCP Server** = 让 AI 代理（Claude、Gemini 等）可以直接读写你的知识库

## 四、主要功能

### 界面概览（四面板布局）

```
┌────────┬─────────────┬─────────────────────────┬────────────┐│Sidebar │ Note List   │ Editor                  │ Right Panel││        │             │                         │            ││ All    │ Note 1      │ # My Note               │ Properties ││ Changes│ Note 2      │                         │ Backlinks  ││ Pulse  │ Note 3      │ Content here...         │ TOC        ││ Inbox  │ ...         │ (BlockNote or Raw)      │ History    ││        │             │                         │            ││Projects│             │                         │            ││People  │             │                         │            ││Events  │             │                         │            │├────────┴─────────────┴─────────────────────────┴────────────┤│ StatusBar: v2026.6.1 │ main │ Synced 2m ago │ Vault: ~/Notes│└──────────────────────────────────────────────────────────────┘
```

- • **Sidebar**：类型导航、保存的视图（Saved Views）、文件夹树
- • **Note List**：按类型/视图过滤的笔记列表，支持搜索
- • **Editor**：富文本（BlockNote）或原始 Markdown（CodeMirror），支持 Wikilink、数学公式、Mermaid 图表、tldraw 白板
- • **Right Panel**：属性面板、反向链接、目录、Git 历史

### 编辑器功能

- • 富文本编辑（BlockNote）+ 原始 Markdown（CodeMirror）自由切换
- • `[[Wikilink]]` 内联链接，支持补全
- • 数学公式（KaTeX：`$...$`、`$$...$$`）
- • Mermaid 图表（`/mermaid` 命令）
- • tldraw 白板（`/whiteboard` 命令）
- • 代码块语法高亮（Shiki）
- • 文件/图片附件
- • 多窗口：`Cmd+Shift+O` 在新窗口中打开笔记

### Git 功能

- • 自动保存 + 自动 Git 提交（AutoGit，可配置空闲阈值）
- • 手动提交、推送、拉取
- • 冲突解决（Keep mine / Keep theirs）
- • Pulse 视图：Git 活动时间线
- • Changes 视图：未提交变更
- • 文件 Diff 视图

### AI 集成

- • 内置 AI 工作区（侧边栏或独立窗口）
- • 支持 CLI 代理：Claude Code、Codex CLI、OpenCode、Gemini CLI、Pi、Kiro
- • MCP Server：让任意 MCP 兼容客户端（Cursor、Claude 等）读写知识库
- • 权限模式：Vault Safe（只读）/ Power User（可写）

### 搜索

- • 全文关键词搜索（无需索引，直接扫描文件系统）
- • 实时过滤（标题、摘要、属性）
- • `Cmd+K` 命令面板

## 五、安装方式

### macOS（推荐：Homebrew）

```
brew install --cask tolaria
```

### 直接下载

访问 tolaria.md/download/[2] 下载最新稳定版：

平台

格式

状态

macOS Apple Silicon

`.app.tar.gz` + `.dmg`

主要开发平台

macOS Intel

`.app.tar.gz` + `.dmg`

支持

Windows x64

NSIS 安装程序 `.exe`

支持（早期）

Linux x64

`.AppImage` / `.deb` / `.rpm`

支持（早期）

## 六、快速上手

### 第一次启动

- 1. 打开 Tolaria，会出现欢迎界面，提供三个选项：
- • **Getting Started Vault**：克隆官方示例知识库（推荐初学者）
- • **Open existing folder**：打开一个已有的 Markdown 文件夹
- • **Create new empty vault**：创建一个新的空知识库
- 2. 选择 Getting Started Vault，Tolaria 会自动从 GitHub 克隆并断开远端连接，让你可以自由编辑练习。

### 基本操作

快捷键

功能

`Cmd+K` / `Ctrl+K`

打开 Command Palette（命令面板，核心入口）

`Cmd+N`新建笔记

`Cmd+P` / `Cmd+O`

快速打开笔记

`Cmd+S`保存笔记

`Cmd+F`在当前笔记中查找

`Cmd+Shift+F`在全库搜索

`Cmd+[` / `Cmd+]`

前进/后退导航

`Cmd+Shift+O`在新窗口中打开笔记

`[[`触发 Wikilink 补全菜单

## 七、核心概念详解

### 7.1 Vault（知识库）

Vault 就是一个文件夹，包含若干 `.md` 文件。Tolaria 不拥有数据，只是读写这些文件。

```
~/MyVault/├── AGENTS.md           ← AI 代理的指引文件（Tolaria 自动维护）├── CLAUDE.md           ← Claude Code 兼容 shim├── project.md          ← type: Type（类型定义文档）├── person.md           ← type: Type├── my-project.md       ← type: Project（普通笔记）├── john-doe.md         ← type: Person├── views/              ← 保存的自定义视图│   └── active-projects.yml└── attachments/        ← 图片、PDF 等附件    └── screenshot.png
```

所有笔记都扁平存放在根目录（或子文件夹），类型由 frontmatter 的 `type:` 字段决定，与文件夹无关。

### 7.2 YAML Frontmatter

每个笔记的元数据通过标准 YAML frontmatter 存储：

```
---type: Projectstatus: Activebelongs_to:  - "[[q2-2026]]"related_to:  - "[[team-alpha]]"start_date: 2026-04-01end_date: 2026-06-30url: https://example.com---# My Project Title正文内容...
```

**常用的语义字段：**

字段

说明

UI 行为

`type:`实体类型（Project、Person、Event…）

侧边栏分组 + 类型标签

`status:`生命周期状态（Active、Done、Blocked…）

彩色状态徽章

`url:`外部链接

可点击的链接按钮

`date:`单个日期

格式化日期徽章

`start_date:` / `end_date:`

时间段

日期区间徽章

`belongs_to:`父级关系

Relationships 面板

`related_to:`关联关系

Relationships 面板

`has:`包含关系

Relationships 面板

**系统字段（以 _ 开头，不在 UI 中显示）：**

```
_pinned_properties:     # 编辑器内联栏显示的属性  - key: status    icon: circle-dot_icon: shapes           # 类型图标_color: blue            # 类型颜色_order: 10              # 侧边栏排序_sidebar_label: 项目     # 侧边栏标签覆盖_width: wide            # 富文本编辑器宽度（normal/wide）
```

### 7.3 Type（类型）

类型是一种特殊的笔记（`type: Type`），它定义了其他笔记的分类规则和默认属性：

```
---type: Typeicon: folder-opencolor: blueorder: 1sidebar_label: 项目template: |  # {title}    ## Goals    ## Notes---# Project
```

点击侧边栏的某个类型名称，可以看到所有属于该类型的笔记。

### 7.4 Wikilink（双向链接）

在编辑器中输入 `[[` 触发补全，创建内部链接：

```
本周开会和 [[john-doe]] 讨论了 [[q2-2026-planning]] 的进展。
```

Tolaria 会自动检测反向链接，在 Right Panel 中显示所有引用了当前笔记的笔记。

### 7.5 Saved Views（保存的视图）

自定义视图存储为 `views/*.yml` 文件，支持复杂过滤：

```
name: Active Projectsicon: foldercolor: bluefilters:  - field: type    op: eq    value: Project  - field: status    op: eq    value: Activesort: modified:desc
```

### 7.6 Git 集成

Tolaria 使用系统 Git，无需额外配置：

```
# 初始化一个带 Git 的新知识库（Tolaria 会自动做这一步）git init ~/MyVault# 连接远端（可以在 Tolaria UI 中操作，也可以命令行）git remote add origin https://github.com/yourname/my-vault.git
```

**AutoGit**：在设置中开启后，Tolaria 会在你停止编辑一段时间后自动提交（类似自动保存的 Git 提交），提交信息为 `Updated N note(s)`。

## 八、使用场景

### 场景 1：个人第二大脑 / PKM

```
---type: Topic---# 认知心理学## 相关资源- [[thinking-fast-and-slow]]- [[kahneman-daniel]]正文笔记...
```

- • 按 `type: Book`、`type: Person`、`type: Topic` 分类所有内容
- • 用 Wikilink 建立知识网络
- • 用 Neighborhood 模式浏览一个笔记的所有关联节点

### 场景 2：项目管理 / 公司文档

```
---type: Projectstatus: Activebelongs_to:  - "[[q2-2026]]"has:  - "[[task-001]]"  - "[[task-002]]"start_date: 2026-04-01end_date: 2026-06-30---# Project Alpha## Overview...
```

- • 每个季度是一个 `type: Quarter` 笔记
- • 每个项目 `belongs_to` 某个季度
- • 每个任务 `belongs_to` 某个项目
- • 用 Saved Views 过滤"本季度 Active 的项目"

### 场景 3：为 AI 代理提供上下文

Tolaria 内置 MCP Server，让 AI 代理可以直接读写知识库：

```
# 在 Tolaria 中：Command Palette → "Setup Claude Code MCP"# 这会自动在 ~/.claude.json 中注册 Tolaria 的 MCP Server# 之后在任何地方使用 Claude Code，它就能：# - 搜索笔记# - 读取笔记内容# - 创建新笔记# - 更新 frontmatter
```

**MCP 工具列表**（AI 代理可调用）：

工具

说明

`search_notes`按标题/内容搜索笔记

`read_note`读取笔记内容

`create_note`创建新笔记

`edit_note_frontmatter`更新笔记 frontmatter

`list_notes`列出所有笔记（可按类型过滤）

`append_to_note`向笔记末尾追加内容

`link_notes`在 frontmatter 中添加 Wikilink 关联

`delete_note`删除笔记

`vault_context`获取知识库全局摘要

`ui_open_note`在 Tolaria UI 中打开某个笔记

### 场景 4：读书/资源管理

```
---type: Bookstatus: Readingurl: https://www.goodreads.com/book/show/...belongs_to:  - "[[reading-list-2026]]"---# Thinking, Fast and Slow作者：[[kahneman-daniel]]## 核心观点...
```

## 九、本地开发 & 从源码运行

### 环境要求

- • Node.js 20+
- • pnpm 8+
- • Rust（stable）
- • macOS 或 Linux（开发环境）

### Linux 系统依赖

**Debian / Ubuntu（22.04+）：**

```
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file \  libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev \  libsoup-3.0-dev patchelf
```

**Arch / Manjaro：**

```
sudo pacman -S --needed webkit2gtk-4.1 base-devel curl wget file openssl \  appmenu-gtk-module libappindicator-gtk3 librsvg
```

**Fedora 38+：**

```
sudo dnf install webkit2gtk4.1-devel openssl-devel curl wget file \  libappindicator-gtk3-devel librsvg2-devel
```

### 启动开发环境

```
# 克隆仓库git clone https://github.com/refactoringhq/tolaria.gitcd tolaria# 安装依赖pnpm install# 浏览器 mock 模式（无需 Rust，快速开发）pnpm dev# 访问 http://localhost:5173# 原生桌面模式（完整功能）pnpm tauri dev
```

## 十、常见问题与解决方法

### Q1：Windows 安装时被 SmartScreen 拦截

**现象**：Windows 弹出"Windows 已保护你的电脑"警告
**原因**：Tolaria 的 Windows 安装包目前处于早期阶段，Authenticode 代码签名正在逐步部署
**解决方法**：

- • 不要禁用 SmartScreen 或 Windows 安全中心
- • 如果是个人设备，可点击"更多信息" → "仍要运行"
- • 如果是公司设备，通过公司软件审批流程安装

### Q2：Linux 上运行 AppImage 崩溃或白屏

**现象**：AppImage 启动失败，或显示白屏
**原因**：Linux WebKitGTK 渲染器与某些 Wayland/DMA-BUF 配置不兼容
**解决方法**：Tolaria 已内置环境变量保护，如仍有问题可手动运行：

```
WEBKIT_DISABLE_DMABUF_RENDERER=1 WEBKIT_DISABLE_COMPOSITING_MODE=1 ./Tolaria.AppImage
```

### Q3：Linux AppImage 上 AI 工具不可用

**现象**：MCP Server 或 Claude Code 在 AppImage 环境下无法使用
**原因**：AppImage 隔离了宿主系统的 Node.js
**解决方法**：确保宿主系统安装了 Node.js：

```
# 例如 Ubuntusudo apt install nodejs
```

Tolaria AppImage 会在 `~/.local/share/tolaria/mcp-server/` 中提取 MCP Server 文件，使用宿主 Node.js 运行。

### Q4：AI 代理无法访问知识库

**现象**：Claude Code / Gemini 等无法读取或操作笔记
**解决方法**：在 Tolaria 中注册 MCP Server：

- 1. 按 `Cmd+K` 打开命令面板
- 2. 搜索 "Setup Claude Code MCP" 或 "Setup Gemini CLI MCP"
- 3. 按提示完成注册
或手动获取配置片段：`Cmd+K` → "Get MCP Config Snippet"，复制到对应的配置文件。

### Q5：Git 推送/拉取认证失败

**现象**：执行 git_push / git_pull 时报认证错误
**原因**：Tolaria 使用系统 Git 的认证配置，不存储任何 Token
**解决方法**：

- • **SSH**：确保 `~/.ssh/id_rsa`（或 ed25519）已添加到 Git 服务商
- • **HTTPS + GitHub**：运行 `gh auth login` 或配置 macOS Keychain
- • **HTTPS + 其他**：配置 `git credential.helper`

```
# macOS：使用 Keychaingit config --global credential.helper osxkeychain# Windows：使用 Git Credential Managergit config --global credential.helper manager# Linux：缓存凭据 1 小时git config --global credential.helper 'cache --timeout=3600'
```

### Q6：Vault 加载后数据不一致 / 缓存问题

**现象**：笔记列表与实际文件不同步
**解决方法**：执行 Vault 重载：

- • `Cmd+K` → "Reload Vault"
- • 这会清除缓存文件（`~/.laputa/cache/<hash>.json`）并重新扫描所有文件

### Q7：笔记中的 Wikilink 解析不到目标

**现象**：`[[target]]` 显示为红色（未解析）
**排查步骤**：

- 1. 确认目标笔记文件名（stem）与 wikilink 中的文本一致（大小写不敏感）
- 2. 或者在目标笔记的 frontmatter 中添加 `aliases:` 字段：

```
---aliases:  - target  - 目标笔记的别名---
```

- 3. 执行 Reload Vault 刷新索引

### Q8：富文本编辑器内容丢失格式

**现象**：从其他应用粘贴内容后格式混乱
**解决方法**：使用"无格式粘贴"：`Cmd+Shift+V`

### Q9：公司设备无法安装（MSI/策略限制）

**解决方法**：通过公司 IT 的软件审批流程请求安装，或从 Releases 页面下载特定版本的安装包。

### Q10：合并冲突（Git Conflict）

**现象**：多设备同步后，某个笔记出现合并冲突
**解决方法**：Tolaria 会在编辑器内显示 **ConflictNoteBanner**，提供：

- • **Keep mine**：保留本地版本
- • **Keep theirs**：保留远端版本
- • 也可以在 Raw 编辑器中手动解决冲突标记（`<<<<<<<` / `=======` / `>>>>>>>`）

## 十一、对比同类产品的优势

### 竞品对比总览

特性

Tolaria

Obsidian

Notion

Roam Research

Logseq

**开源**AGPL-3.0

闭源

闭源

闭源

AGPL

**本地优先**完全本地

云端为主

云端

**数据格式**纯 Markdown

Markdown

私有格式

私有格式

Markdown

**需要账号**不需要

（付费同步需要）

必须

必须

**Git 原生集成**内置

需插件

实验性

**AI 代理集成（MCP）**内置

插件

**付费订阅**免费

Sync $8/月

$8–20/月

$15/月

部分付费

**离线可用**完全离线

**跨平台**mac/Win/Linux

Web/App

Web

### 11.1 Git 原生集成，而非"插件补丁"

**对比 Obsidian**：Obsidian 的 Git 版本控制依赖第三方社区插件，不稳定、功能有限、移动端无法使用。

Tolaria 的 Git 是**一等公民**：

- • 每个 Vault 天然就是一个 Git 仓库
- • 内置 **AutoGit**：停止编辑后自动提交，相当于"带版本的自动保存"
- • 内置 **Pulse 视图**：可视化 Git 活动时间线，类似 GitHub 的 commit history
- • 内置 **Changes 视图**：实时展示未提交的修改（类似 `git status`）
- • 内置 **冲突解决 UI**：多设备同步冲突时，直接在编辑器中 Keep mine / Keep theirs
- • 支持任意 Git 远端：GitHub、GitLab、Gitea、自托管，一视同仁

> 对 Obsidian 用户的意义：你不再需要担心 Obsidian Git 插件在 iOS 上失效，也不再需要为 Obsidian Sync 每月付 $8。

### 11.2 AI 代理原生集成（MCP Server）

这是 Tolaria 最具前瞻性的差异化优势，**目前没有任何主流笔记产品可以对标**。

Tolaria 内置一个 **MCP（Model Context Protocol）Server**，让 AI 代理可以像操作代码库一样操作你的知识库：

```
Claude Code / Codex CLI / Gemini CLI           ↓ MCP 工具调用    search_notes("Q2 项目进展")    read_note("q2-2026.md")    edit_note_frontmatter("project.md", {status: "Done"})    create_note("new-idea.md", content)           ↓        你的知识库（本地 .md 文件）
```

**实际意义**：

- • 让 AI 真正成为你的"知识库助手"，而不只是聊天工具
- • AI 可以主动搜索、读取、修改、创建笔记
- • 知识库的结构化 frontmatter（type/status/belongs_to 等）让 AI 能理解知识图谱关系
- • Notion AI、Obsidian AI 都是封闭生态，无法接入任意 AI 代理

### 11.3 真正的"零锁定"

产品

数据迁出成本

Notion

高：导出 HTML/Markdown 格式丢失，数据库关系无法完全还原

Roam Research

高：EDN 格式，工具生态极小

Obsidian

低：本地 Markdown，但 Dataview 查询语法是私有的

**Tolaria****极低：纯 Markdown + YAML frontmatter，停用后什么都不丢**

Tolaria 的核心承诺：

> "If you stop using Tolaria, you lose nothing."

你的笔记是标准 Markdown 文件，任何编辑器都能打开，任何工具都能迁移。

### 11.4 真开源 vs 假开源

- • **Obsidian**：完全闭源，核心功能（Sync、Publish）付费墙，商业公司控制路线图
- • **Logseq**：开源但曾宣布转向数据库模式，社区有顾虑
- • **Tolaria**：AGPL-3.0，代码完全公开，你可以自己 fork、自己 build、自己修改
对于企业或注重数据安全的用户，开源意味着可审计、可自托管、无后门。

### 11.5 为大规模知识库设计

Tolaria 是**作者用来管理 10,000+ 笔记的工具**，性能设计从一开始就针对大 Vault：

- • **Git 增量缓存**：`~/.laputa/cache/` 使用 git diff 做增量更新，不是每次全量扫描
- • **渐进加载**：打开大 Vault 时，UI 先渲染 shell，数据异步加载，不卡顿
- • **关键字搜索直扫文件系统**：不需要预建索引，但有结果评分排序
对比 Notion：Notion 在 Workspace 有几千条数据时就开始明显变慢；Tolaria 本地处理，速度取决于你的硬盘而非网络。

### 11.6 约定优于配置，但不强迫你

Tolaria 内置一套语义字段约定（`type`、`status`、`belongs_to` 等），这些约定直接驱动 UI 行为：

```
type: Project       → 侧边栏自动分组status: Active      → 彩色状态徽章belongs_to: [[Q2]]  → 自动建立关系图
```

但这一切都是**可选的**：

- • 没有必填字段，没有 Schema 验证
- • 不用这些字段照样能用
- • 类型（Type）是导航辅助，不是数据库约束
对比 Notion Database：Notion 的数据库有强 Schema，字段类型不对就无法正常渲染。

### 11.7 键盘驱动的效率设计

这是对比 Bear、Notion、Apple Notes 等"鼠标友好"工具的优势：

- • `Cmd+K`：Command Palette，几乎所有操作一键直达
- • `[[`：即时触发 Wikilink 补全
- • `Cmd+[` / `Cmd+]`：前进后退导航（取代标签页）
- • `Cmd+Shift+O`：在新窗口中打开笔记
- • 所有快捷键跨平台一致（macOS 用 `Cmd`，Linux/Windows 用 `Ctrl`）

### 11.8 隐私与安全

产品

遥测

数据上云

Notion

强制，无法关闭

全部数据在云端

Roam

未知

云端

Obsidian

可关闭

本地（Sync 功能走云端）

**Tolaria****首次询问，可完全关闭****永不上传笔记内容**

Tolaria 的遥测仅收集匿名的崩溃报告和使用统计（且明确告知哪些字段），绝不上传笔记内容、文件路径或 AI 对话内容。

### 适合与不适合的用户

**非常适合**：

- • 重视数据主权、不想被云服务绑架的用户
- • 已有 Git 工作流习惯的开发者或技术人员
- • 想把知识库与 AI 代理（Claude、Gemini 等）深度集成的用户
- • 管理大规模个人/团队知识库（几千到几万条笔记）
- • 注重键盘效率、追求 Power User 体验的用户
**可能不适合**：

- • 需要移动端 App（iOS/Android）的用户（目前尚在开发中）
- • 习惯拖拽表格、看板等 Notion 式数据库操作的用户
- • 不熟悉 Git 概念，且不想学习的非技术用户

## 十二、技术架构简介

层

技术

桌面 Shell

Tauri v2

前端

React 19 + TypeScript 5.9

编辑器

BlockNote 0.46 + CodeMirror 6

图表

Mermaid 11

白板

tldraw 4

数学公式

KaTeX

样式

Tailwind CSS v4

构建

Vite 7

后端

Rust（Tauri IPC 命令）

Frontmatter 解析

gray_matter（Rust）

文件监听

notify（Rust）

MCP Server

Node.js（`@modelcontextprotocol/sdk`）

AI 代理

CLI 子进程（Claude Code / Codex / Gemini / Pi / Kiro）

**数据流：**

```
Filesystem (.md files)    ↓ scan_vault_cached()Cache (~/.laputa/cache/)    ↓ useVaultLoaderReact State (VaultEntry[])    ↓ Tauri IPC (保存时)Filesystem (.md files)  ← 文件系统始终是唯一真相来源
```

## 十三、补充信息

### 发布节奏

- • **Alpha**：每次推送到 `main` 分支都会自动发布 Alpha 版本（版本号格式：`YYYY.M.D-alpha.N`）
- • **Stable**：打 `stable-vYYYY.M.D` 标签后发布稳定版
在设置中可以切换 Alpha / Stable 更新频道。

### 数据存储位置

数据

路径

笔记和附件

你选择的 Vault 文件夹

类型定义和保存的视图

Vault 文件夹（跟着 Git 同步）

应用设置

`~/.config/com.tolaria.app/settings.json`Vault 列表

`~/.config/com.tolaria.app/vaults.json`缓存

`~/.laputa/cache/<hash>.json`（可重建）

窗口大小、缩放等

本地 app 设置

### 遥测与隐私

- • 首次启动时会询问是否开启匿名崩溃报告（Sentry）和使用分析（PostHog）
- • 可在设置中随时关闭
- • 绝不上传笔记内容、文件路径或 AI 对话内容

### 安全问题报告

如发现安全漏洞，请通过 GitHub Private Security Advisory 私下报告，不要公开 Issue。详见 SECURITY.md[3]。

## 十四、相关资源

资源

链接

官方网站

tolaria.md[4]

GitHub 仓库

refactoringhq/tolaria[5]

下载页面

tolaria.md/download[2]

发布记录

tolaria.md/releases[6]

Getting Started Vault

refactoringhq/tolaria-getting-started[7]

架构文档

docs/ARCHITECTURE.md[8]

作者 Twitter

@lucaronin[1]

播客/newsletter

Refactoring[9]

许可证

AGPL-3.0-or-later

#### 引用链接

`[1]` Luca Rosini: *http://x.com/lucaronin*
`[2]` tolaria.md/download/: *https://tolaria.md/download/*
`[3]` SECURITY.md: *https://github.com/refactoringhq/tolaria/blob/main/SECURITY.md*
`[4]` tolaria.md: *https://tolaria.md*
`[5]` refactoringhq/tolaria: *https://github.com/refactoringhq/tolaria*
`[6]` tolaria.md/releases: *https://tolaria.md/releases/*
`[7]` refactoringhq/tolaria-getting-started: *https://github.com/refactoringhq/tolaria-getting-started*
`[8]` docs/ARCHITECTURE.md: *https://github.com/refactoringhq/tolaria/blob/main/docs/ARCHITECTURE.md*
`[9]` Refactoring: *https://refactoring.fm*
