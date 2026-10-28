---
title: "SolidCraft：纯 Rust 开源参数化 3D CAD + MCP"
type: document
source: video
file_type: md
file_path: /root/vault/2-Areas/AI-Agent-研究/2026-10-28 - SolidCraft - 纯 Rust 参数化 3D CAD 与 MCP Agent 接入.md
uploaded_date: 2026-10-28
title_short: "SolidCraft 研究笔记"
description: "SolidCraft 全面调研：tangency-labs/solidcraft 真实数据核实、MCP 工具集与安全模型、五层架构、几何内核 SolidCore、部署可行性，以及对德勤 Agent 执行器抽象层的借鉴点"
size_bytes: 0
tags:
  - solidcraft
  - cad
  - mcp
  - rust
  - agent-tooling
  - parametric-cad
  - ai-native
  - research
related:
  - "2-Areas/AI-Agent-研究/2026-10-28 - DeepSeek Harness + DS Bot - 架构分析与德勤项目借鉴点.md"
  - "3-Resources/AI工具/2026-09-04 - Rakazo 开源 AI 队友平台.md"
source_note: "何大人提供（视频里展示的项目页），2026-10-28"
---

# SolidCraft：纯 Rust 参数化 3D CAD + MCP

> **何大人提供**：`https://github.com/solidcraft/solidcraft`（视频里展示的项目页，9.9k Stars）
> **⚠️ 核实结果**：该地址 **404**。真实仓库是 **`tangency-labs/solidcraft`**，2026-10-28 实测 **11,462★**（何大人说的 9.9k 是视频录制时点，涨势很快）。

---

## 一、核实数据（GitHub API，2026-10-28）

| 项 | 值 |
|---|---|
| 仓库 | `tangency-labs/solidcraft` |
| 描述 | SolidCraft: an open-source parametric 3D CAD application built in pure Rust. Desktop, web, and automation through MCP. |
| Stars | **11,462** |
| Forks | 1,458 |
| Open issues | **4,028** |
| 创建 | **2026-10-07**（距今仅 3 周）|
| 最近推送 | 2026-10-28（当天）|
| 版本 | **v0.25.1**（2026-10-28 发布，前一天 v0.25.0）|
| License | Apache-2.0（另有 MIT 部分资产）|
| 主页 | https://solidcraft.io ｜ 文档 https://docs.solidcraft.io/ |
| 话题标签 | `3d-modeling` `brep` `cad` `egui` `mcp` `parametric-cad` `rust` `step` `wasm` |
| 仓库体积 | 221 MB（含 vendor）|
| 累计下载 | 18,968 次（v0.25.1 全平台）|

### 语言构成
```
Rust    32,176,594 B  96%   ← 纯 Rust，名副其实
Python     824,891 B   2%
WGSL       131,709 B   0%   ← GPU 着色器
JavaScript  117,662 B   0%
```

### 几何内核（关键）
- **`tangency-labs/solidcore`** —— 244★，Apache-2.0
- 描述：**A Rust port of NVIDIA's SMLib B-rep kernel (CAD subset): safe, deterministic, wasm-compatible**
- 原仓库 `bherbruck/solidcore` 已 301 重定向到 `tangency-labs/solidcore`

---

## 二、⚠️ 三个必须知道的信号

### 1. 项目只有 3 周大，但 issue 编号已到 #8235

| 指标 | 数值 | 解读 |
|---|---|---|
| 创建至今 | **21 天** | 极快 |
| Stars | 11,462 | 病毒式传播 |
| 总 issue 数 | **8,235+** | 约为 star 数的 72% |
| 未关闭 | **4,028** | 关闭率仅约 51% |

**未关闭 issue 抽样**（全是新手级问题）：
```
#8235 MODEL: Not able to snap points
#8233 Move surfaces
#8232 INSERT SVG: operation failed
#8229 When you save step file as mesh sometimes it does weird stuff
#8225 SHELL: operation failed
#8224 Feature request: Reverse spline direction / control-point order
```
**判读**：用户基数巨大但**以新手为主**，问题质量偏低 → 说明这是"现象级传播"但**工程成熟度远落后于 star 数**。v0.25.1 仍是 0.x，API 会破坏性变更。

### 2. 法务干净（少见）
- `CONTRIBUTING.md` 明写 **clean-room 与 licence 规则**
- `ATTRIBUTION.md` **强制每个资产登记作者/来源/许可**，`cargo xtask assets` 校验不过就 CI 失败
- **明确声明不含任何 Autodesk 图标/图片/字体/模板/帮助文本**
- 有 `NOTICE.md`、`THIRD-PARTY-LICENSES.txt`、`LICENSE-APACHE` + `LICENSE-MIT`
- **对德勤这类需要过法务的项目，这点非常关键**

### 3. 几何内核是 NVIDIA SMLib 的 Rust 移植
`SolidCore` 是 "Rust port of NVIDIA's SMLib B-rep kernel"。虽然许可证清晰（Apache-2.0），但**如果德勤客户涉及 IP 红线，需要法务确认 SMLib 移植的许可状态**。建议在正式引用前让法务过一遍 `NOTICE.md` + `THIRD-PARTY-LICENSES.txt`。

---

## 三、架构：五层 + "一切皆命令"

来源：`docs/architecture.md`

| 层 | Crates | 职责 |
|---|---|---|
| **L0** | `geom` | 向量、平面、轮廓、网格及其度量 |
| **L1** | `sketch` `kernel` `render` | 约束求解器与轮廓；**B-rep 内核边界（truck）**；视图数学与 headless 场景描述 |
| **L2** | `doc` | 参数、表达式、**特征时间线与增量求值** |
| **L3** | `io` | 设计文件、STL/OBJ/STEP/3MF 导出、STEP/3MF/STL/OBJ/glTF 导入特性 |
| **L4** | `engine` | **会话与命令注册表（一切都是命令）** |
| **L5** | `gpu` `ui-egui` `mcp` | 计算着色器求值；可换桌面前端；**MCP 服务器（headless 或桥接桌面端）** |
| apps | `solidcraft` `solidcraft-cli` | 桌面应用、headless CLI |

### ⭐ 核心设计原则（德勤最该抄的一条）

> **One command surface.**
> 工具栏、脚本、控制通道、MCP、（将来）浏览器内 Agent —— **全部走同一套 engine commands**。
> 无人值守路径只用 dialog-free 命令，MCP 也遵守同一规则。

**这条直接对应德勤 `ExecutorAdapter` 的设计**：执行器、脚本、Agent 不应该有三套语义。

### 能力清单（README "What works"）
- **草图与约束**：直线、圆弧、样条、文本，自研约束求解器，参数驱动尺寸
- **特征**：拉伸、旋转、扫掠、放样、圆角、倒角、抽壳、拔模、螺纹、阵列、镜像、分割、组合，全在可编辑参数化时间线上
- **参数与配置**：带单位表达式
- **装配体**：关节、运动研究、接触集、干涉检测、质量属性
- **钣金**：翻边、包边、展开/折回、平板展开图、塑胶外壳特征
- **格式**：STEP / IGES / 3MF / STL / OBJ / glTF 进出，URDF 导出
- **运行形态**：桌面 App、浏览器 App、**headless CLI**、**MCP 服务器** —— 跑同一套命令

### 精度可信度
> 76 个公开参考零件中，**75 个**的体积/面积/质心/包围盒与解析解或 FreeCAD 计算值一致（1 个是已追踪 bug）。

**这条对德勤很有说服力**——不是 demo 级精度。

---

## 四、⭐ MCP 接入（何大人最关心的点）

### 启动方式
```bash
# Headless：进程内独立设计会话，无窗口（截图走 GPU 设备）
solidcraft-cli mcp

# Headless，从文件开始
solidcraft-cli mcp --in part.sc

# 桥接到运行中的桌面端（可以看着 Agent 建模）
solidcraft &
solidcraft-cli mcp                 # 自动发现运行中的 app
solidcraft-cli mcp --connect 127.0.0.1:7878
```
Claude Code 接入：
```bash
claude mcp add solidcraft -- solidcraft-cli mcp
```

### 协议
- **stdio / JSON-RPC 2.0**，一行一条消息
- 协议版本：**2025-06-18、2025-03-26、2024-11-05**（三个版本兼容）

### 自动配置的客户端（10 个）
```
opencode / claude-desktop / claude-code / cursor / codex /
gemini / copilot / windsurf / zed / vscode
```
> ✅ **本机就装了 OpenCode**（`opencode2 serve`）→ 官方原生支持 OpenCode 配置路径。

### 工具集（约 18 个）

| 工具 | 作用 | 备注 |
|---|---|---|
| `list_commands` | 命令目录（id/标签/面板/快捷键/参数文档）| 支持 filter |
| `describe_command` | 单命令参数文档 + **JSON Schema (2020-12)** | 输入 schema + 输出 schema |
| `execute` | 执行任意命令 | 失败**不改设计**；返回 feature / bodies / created_bodies / changed_bodies / removed_bodies |
| **`batch`** | 批量执行 | ⭐ **默认 rollback=true：首错即停并回滚已完成的步骤**；返回 failed.index / failed.command / rolled_back / undone / applied / not_run；`coalesce_parameters` 合并连续参数改动只重建一次 |
| `inspect_design` | 设计全貌 | metadata / parameters / **timeline（含 suppressed/rolled_back/error/warning/timing）** / bodies / sketches（含 DOF、求解状态）/ joints / selection / undo depth |
| `measure` | 度量 | 面积、体积、质心、密度、质量；几何拾取（面/边/点/草图曲线/轮廓）|
| `body_topology` | 拓扑 | 边（中点、长度）、面（面积、法向、质心、圆柱参数）|
| `set_parameter` | 改参数 | 报告 `recomputed` / `restored`（复用先前结果）/ 失败特征 |
| `screenshot` | PNG 图像内容块 | headless 走 GPU 或 CPU 光栅器；bridged 可截应用窗口或模型视图 |
| `export` | 导出 | STEP / 3MF / STL / OBJ / URDF（装配含 mesh）|
| `undo` `redo` | 撤销重做 | |
| `pending` | 长任务等待 | 最多等 60s |
| `running` | 当前在跑什么 | 每个客户端的连接、id、方法、耗时 |
| `crash_reports` | 崩溃报告 | 含 backtrace、命令、design_path、replay_path |
| **`skill_reference`** | 读内置 skill 文档 | 4 个 skill：modeling / mechanisms / editing / checking |
| `new_design` `open` `save` | 文件操作 | |

### ⭐ 安全模型（三层，借鉴价值极高）

**1）文件路径沙箱**
- 只能访问：**设计所在文件夹**（须严格在 home 或 temp 内、非隐藏目录）+ SolidCraft 自己的恢复目录 + MCP 私有临时目录 + 每个 `--allow-path DIR`
- **启动工作目录本身不算授权** → `~/.ssh`、`~/.aws`、`.bashrc` 默认不可达
- 隐藏目录（`~/.config`）与隐藏文件（`.env`、`.git`）不可达
- **路径先解析（canonicalize）再比较** → `..` 和指向外部的 symlink 被拒绝（存到链接里，链接目标才是真实归属）
- 新文件必须落在已存在文件夹内；缺文件夹会报错而**不会自动创建、不会放宽权限**

**2）控制通道令牌**
- 桌面端默认开 `127.0.0.1:27878`（占用则顺延），**仅本机可达**
- **每次启动现场生成新 token**，只有该用户可读
- 端口写在 `control/current.port`，`solidcraft-cli mcp` 无参即可读取
- `--token T` / `SOLIDCRAFT_CONTROL_TOKEN` 可显式指定（**推荐用环境变量，因为命令行参数在进程列表里对其他用户可见**）

**3）长任务与崩溃语义**
- 超 60s 的请求返回 "still running"，**不是失败、不是取消**，连接保留
- app 中途崩溃：未完成的调用返回明确错误，**并提示"检查设计状态后再重发"**
- `batch` 发送失败说"app 没在跑" → **可以安全重发**
- stdout 只走协议消息，错误走 stderr

### 参数校验
`--param-check off|warn|strict`（默认 off）
- `warn`：执行并在结果里加 `param_warnings`，例如 ``unknown key `operaton`; did you mean `operation`?``
- `strict`：直接拒绝调用，**设计保持原样**
- 桥接到 app 的调用暂不校验

### 内置 Skills（4 个）—— ⭐ 与德勤"Skill 提示词开发"直接对应
```
solidcraft-modeling     solidcraft-mechanisms
solidcraft-editing      solidcraft-checking
```
- 每个 skill 有 `SKILL.md` + `reference.md`
- `skill_reference` 工具直接从 SolidCraft 内置副本返回文档，**不读磁盘路径** —— 没有文件权限的 Agent 也能用
- SolidCraft 自带的聊天会**关掉 Agent 的文件工具**，所以这是它在内部读 skill 的方式
- 可复制到 `~/.claude/skills/` 给 Claude Code 用

---

## 五、浏览器版（wasm）与容器化部署

### 架构（`docs/web-runtime.md`）
- wasm 应用，设计存在 **OPFS**（origin private file system）+ 可选 File System Access 导入导出
- WebGPU 视口跑主线程（wgpu via eframe）
- 三个墙：**Quota**（大 STEP/容器 blob 与自动保存抢 OPFS）、**主线程**（打开/保存/时间线求值同步跑在 egui UI 线程）、**Agent**（MCP 在进程外，标签页没有一等 agent session）
- 设计方向：`craft-libs`（storytold/craft-libs）里实现 `craft-tier-store` / `craft-worker-host` / `craft-gpu` / `craft-runtime` 一次，Web 和 Native 共用同一套 trait
- **Do not duplicate cloud IO**：认证云存储用 `craft-cloud` + CollabCraft

### ⭐ 官方 Docker 化（`packaging/docker/`）
```yaml
services:
  solidcraft:
    image: ghcr.io/tangency-labs/solidcraft-web:latest
    ports: ["${SOLIDCRAFT_PORT:-8080}:8080"]
    restart: unless-stopped
    read_only: true          # 根文件系统只读
    tmpfs: ["/tmp"]
    security_opt: ["no-new-privileges:true"]
    cap_drop: ["ALL"]
```
**基镜像 `nginxinc/nginx-unprivileged:1.29-alpine`，静态站由 `trunk build --release` 产 wasm**

### 镜像实测体积（2026-10-28，GHCR manifest）
```
ghcr.io/tangency-labs/solidcraft-web:latest
  多架构 index：linux/amd64 + linux/arm64 + 2 个 attestation
  amd64：12 层，压缩总 51 MB
```
> ✅ **51MB**，比 Rakazo 的 8.2GB 轻两个数量级。

### ⚠️ 官方明确提醒
> **Saving designs needs HTTPS or localhost**（浏览器私有文件存储要求）→ 服务器上必须前置 TLS 反代。

---

## 六、部署（已在本机完成，2026-10-28）

### ✅ 浏览器版已上线

| 项 | 值 |
|---|---|
| **访问地址** | **`https://101.35.52.96.sslip.io/solidcraft/`** |
| 容器 | `solidcraft-web`（`ghcr.io/tangency-labs/solidcraft-web:latest`）|
| 内部端口 | `127.0.0.1:5181`（容器内 8080）|
| compose | `/root/solidcraft/compose.yaml` |
| 镜像体积 | 压缩 51MB / 展开 **204MB** |
| 硬��化 | `read_only: true` + `tmpfs:/tmp` + `no-new-privileges` + `cap_drop: ALL`（官方默认）|
| nginx 路由 | 加在 `/etc/nginx/conf.d/rakazo.conf` 的 `location /solidcraft/` |

### 为什么用路径路由而不是子域名
现有证书 `openwork.crt` 是**自签 CA**，SAN 只有：
```
DNS:101.35.52.96.nip.io, DNS:101.35.52.96.sslip.io, IP Address:101.35.52.96
```
`101.35.52.96.sslip.io` 已被 Rakazo 占用；新子域名不在 SAN 里会证书报错。
官方文档明确 **"the site works under any URL path"** → 用 `/solidcraft/` 路径，**不动现有证书**。

### 验证结果
```
/solidcraft/                              → HTTP 200  (2093B)
/solidcraft/solidcraft-web-*.js           → HTTP 200  (183KB)
/solidcraft/solidcraft-web-*_bg.wasm      → HTTP 200  (85MB)
/solidcraft/sw.js                         → HTTP 200
/solidcraft/manifest.webmanifest          → HTTP 200
```

### ⭐ Chrome 无头渲染实测
| 尝试 | 结果 |
|---|---|
| `--disable-gpu` | ❌ "SolidCraft failed to start: failed to create wgpu surface … webgl2 not available" |
| `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader` | ✅ **完全加载 v0.25.1** |

**渲染确认**：Start 页面完整（New design / New design, inches / Open / Import 卡片）、6 个 Sample（Sample Plate、Sheet Metal Bracket、Hinge Assembly、Plastic Enclosure、Bolted Flange、Vent Plate）、顶栏 File/undo/redo/Settings/Help/Report a bug/v0.25.1、左侧 Start·New·Open·Recover。

> ⚠️ **硬需求：浏览器必须有 WebGPU 或 WebGL2**。无 GPU 的老机器/虚拟机需开 SwiftShader 软件渲染。

### 本机资源开销
| 项 | 值 |
|---|---|
| 内存 | 约 30-50MB（纯 nginx 静态站）|
| CPU | ≈ 0（wasm 视口在**客户端**跑，服务端只发文件）|
| 磁盘 | 204MB（镜像）|

**结论：✅ 部署成本几乎为零，比 Rakazo 轻两个数量级。**

### ⚠️ 拉取同样踩 GHCR 限速
官方 `ghcr.io/tangency-labs/solidcraft-web:latest` 直连 **TLS handshake timeout**（与 Rakazo 同一个 CDN 问题）。
✅ 同样走代理：
```bash
docker pull ghcr.chenby.cn/tangency-labs/solidcraft-web:latest
docker tag ghcr.chenby.cn/tangency-labs/solidcraft-web:latest ghcr.io/tangency-labs/solidcraft-web:latest
```

### 踩坑：nginx `http2 on;` 语法
本机 nginx **1.24.0**（Ubuntu 24.04）不支持 `http2 on;` 独立指令（那是 1.25.1+）。
→ 改用 `listen 443 ssl http2;`。
> 第一次 `nginx -t` 失败导致 `systemctl reload nginx` 失败 —— **老配置保留，nginx 未中断，Rakazo / yuanzhi 均正常**（reload 失败 ≠ 停服）。

### 踩坑：`server_name` 冲突
两个 conf 都声明 `101.35.52.96.sslip.io` → nginx warn "conflicting server name … ignored"。**这就是改用路径路由的原因。**

---

## 七、MCP 接入到 OpenClaw（方案已就绪，CLI 下载受阻）

### OpenClaw 原生支持 MCP 客户端 ✅
查 OpenClaw 文档（`docs/cli/mcp.md`）确认：OpenClaw 有 **MCP 客户端注册表**。

```bash
# 查看已注册的 MCP server
openclaw mcp list
openclaw mcp show <name> --json

# 注册一个 stdio MCP server
openclaw mcp set solidcraft '{"command":"/root/solidcraft/solidcraft-cli","args":["mcp"]}'

# 移除
openclaw mcp unset solidcraft
```

**关键机制**：
- 定义存在 OpenClaw config 的 `mcp.servers` 下，**由 OpenClaw 集中管理**，下游 runtime（embedded Pi 等）不需要自己维护重复的 MCP 列表
- `set` 只写配置，**不连接、不校验可达性**
- 传输类型：stdio（`command`+`args`）/ `streamable-http`（`url`+`transport:"streamable-http"`）
- **embedded Pi 的 `coding` 和 `messaging` tool profile 默认包含 MCP 工具**；`minimal` 隐藏；`tools.deny: ["bundle-mcp"]` 可显式关闭
- stdio MCP server 由 OpenClaw 启动，**关机时按进程树回收**，子进程不残留
- 会话级 MCP runtime 在空闲 `mcp.sessionIdleTtlMs`（默认 10 分钟）后回收

### ⭐ SolidCraft 官方已原生支持 OpenCode
SolidCraft 的 `solidcraft-cli mcp --client` 自动写入配置，支持 10 个客户端：
```
opencode / claude-desktop / claude-code / cursor / codex /
gemini / copilot / windsurf / zed / vscode
```
**本机已跑 `opencode2 serve`** → `~/.config/opencode/opencode.json` 可直接被 SolidCraft 写入。

### ⚠️ CLI 下载受阻（同一个 GitHub CDN 问题）
```
https://github.com/tangency-labs/solidcraft/releases/download/v0.25.1/solidcraft-0.25.1-linux-x86_64.tar.gz
  → 18 秒采样：速度 0 B/s，下载 0 B  ← release assets CDN 完全卡死
```
（容器 CDN `pkg-containers.githubusercontent.com` 之前实测 16 KB/s，同样是问题源。）

**因此 `solidcraft-cli` 二进制目前拿不到**。可选路径：
1. 让何大人在**浏览器直接访问** `https://101.35.52.96.sslip.io/solidcraft/`（✅ 已可用，wasm 版自带完整功能）
2. CLI 从境外网络下载后再传上来（`scp` / 微信传文件）
3. 源码构建（`cargo build --release -p solidcraft-cli`）→ 2 核机器上 32MB Rust 代码，耗时不现实

---

## 八、对德勤项目（AI Native MVP）的借鉴点

### 1. ⭐ "One command surface" → ExecutorAdapter 的统一语义
> 工具栏 / 脚本 / 控制通道 / MCP / Agent 全部走同一套命令。

德勤的执行器抽象层如果为每种 Agent（Hermes / OpenClaw / Codex / Claude Code）各做一套适配，就会出现 N×M 语义分裂。SolidCraft 的做法是：**先定义与 Agent 无关的 engine command 层，再把 MCP / CLI / UI 都做成它的薄壳**。→ 这条应该写进德勤执行器抽象层的架构原则。

### 2. ⭐ `describe_command` 的 JSON Schema → 直接对上赛力斯 JD 里的"Tool 动态 Schema 注册"
赛力斯 JD 要求"配置驱动的 Tool 动态 Schema 注册"。SolidCraft 的做法是：
- **输入 schema + 输出 schema 都声明式**（JSON Schema 2020-12）
- `describe_command` 可运行时查询 → Agent 能**在调用前自检参数**
- `--param-check warn/strict` 两档：warn 给出"你是不是想写 operation"这类纠错提示；strict 直接拒绝且**保持设计不变**

→ 德勤可以直接抄这个两级校验 + schema 自描述模式。

### 3. ⭐ `batch` 的事务语义 → Agent 动作的原子性
```
默认 rollback=true：首错即停 + 回滚已完成步骤
返回 failed.index / failed.command / failed.error / rolled_back / undone / applied / not_run
```
→ **Agent 执行器必须提供事务边界**，否则一次失败会留下半成品状态。德勤 ExecutorAdapter 建议照此定义 `executeBatch`。

### 4. ⭐ 文件沙箱 + 现场令牌 → 执行器隔离基线
- 路径先 canonicalize 再比较，`..`/symlink 逃逸被拒
- 隐藏目录/隐藏文件默认不可达
- 每次启动新令牌，令牌只在进程内传递（用环境变量而非命令行）
→ 对应德勤金融/政务客户的安全评审基线（与之前 DSH 的 Secret 遮蔽是同一类）。

### 5. ⭐ 内置 skill + `skill_reference` → "Skill 提示词开发"的标准范式
- skill 与工具**分离**：工具是能力，skill 是怎么用这个能力的方法论
- `skill_reference` **不走文件读取**，所以在禁文件权限的环境里也能用
→ 德勤的 Skill 体系可以直接借鉴这个"能力/方法论分离"的结构。

### 6. `pending` / `running` / `document.revision` → Agent 感知的异步语义
- `document.revision` 只在设计真正变化时递增 → Agent 可判断"我的上一步到底生效没有"
- `running` 告诉 Agent 当前在跑什么、排队多少
- `pending` 处理超过 60s 的调用

### 7. 免责声明
SolidCraft 是 **CAD 垂直工具**，跟德勤金融科技/政务主业无直接关系。它的价值是**"领域软件如何把能力暴露给 Agent"的参考实现**，不是技术选型对象。

---

## 九、风险清单

| 风险 | 说明 |
|---|---|
| **项目仅 3 周** | v0.25.1，0.x 版本，API 会破坏性变更 |
| **issue 洪水** | 8,235+ issue / 4,028 未关，工程质量信号弱于 star 数 |
| **维护者单点** | 主要作者 `bherbruck`（SolidCore 同作者），Tangency Labs 团队 |
| **内核许可** | SMLib 移植 → 正式商用前需法务过 `NOTICE.md` / `THIRD-PARTY-LICENSES.txt` |
| **桌面端无签名** | 官方明说 "The downloads aren't signed yet" → 企业分发需自建签名流程 |
| **浏览器端存储** | OPFS 配额限制；大 STEP 导入会撞墙 |

---

## 十、待办

- [x] 浏览器版已部署到本机并验证（第六节）
- [x] OpenClaw MCP 客户端注册表路径已确认（第七节）
- [ ] `solidcraft-cli` 二进制下载（被 GitHub CDN 卡住，需外部协助）
- [ ] 拿到 CLI 后执行 `openclaw mcp set solidcraft '{"command":"/root/solidcraft/solidcraft-cli","args":["mcp"]}'` 并实测
- [ ] 法务视角复核 SMLib 移植许可（如果德勤要用）
- [ ] 桌面版 GUI 通过 x11vnc（101.35.52.96:5901）实际体验一次

---

*记录人：小助 ｜ 2026-10-28 ｜ 数据源：GitHub API + 仓库 README/docs/architecture.md/mcp.md/web-runtime.md*
