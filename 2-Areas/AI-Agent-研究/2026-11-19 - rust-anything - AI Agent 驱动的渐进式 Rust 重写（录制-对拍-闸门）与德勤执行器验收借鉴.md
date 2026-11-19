---
title: rust-anything —— AI Agent 驱动的渐进式 Rust 重写（录制-对拍-闸门）与德勤执行器验收借鉴
date: 2026-11-19
type: research-note
subject: github.com/erkamyaman/rust-anything（MIT / Rust / 2026-11-16 建仓）
tags: [开源, Rust, 代码迁移, Agent工具, MCP, 验收闸门, 德勤项目, 执行器抽象层]
related_notes:
  - 2026-10-28 - DeepSeek Harness + DS Bot - 架构分析与德勤项目借鉴点.md
  - 2026-11-05 - 德勤 Agent 平台借鉴清单 v1（Autoloop×Super-agent×DSH）.md
  - 2026-11-05 - JevAgentHarness 分析 - 决策模型与LLM共享控制权.md
  - ../../1-Projects/德勤/AI-Native/kernel/README.md
---

# rust-anything 分析（2026-11-19）

> **一句话**：把"重写整个应用"拆成 **profile → analyze → bridge → record →（Agent 写 Rust）→ build → diff → bench → shadow → gate** 十步；
> **AI 只负责写代码，"对不对"由机器判定** —— 录下原实现的真实行为（cases.jsonl），回放对拍，全绿才准上线。
> 真正的价值不是 Rust，而是这套 **"录制—对拍—闸门"验收范式**，它正好补我们执行器抽象层最缺的一环：
> **如何机器判定"Hermes / Claude Code / Codex / OpenClaw 换个执行器后行为等价"。**

---

## 0. 何大人转述的核实结果：属实 5 条，需更正/加注 4 条

| 转述 | 核实 | 备注 |
|---|---|---|
| 开源地址有效 | ✅ | `github.com/erkamyaman/rust-anything`，作者 Erkam Yaman，MIT，主语言 Rust |
| 渐进式迁移热点代码，不一次性重写 | ✅ | 核心是 profile 找热点 → analyze 排波次 → 按 unit 逐个移植 → app lift 变纯 Rust |
| "先用 AI Agent 把原逻辑录下来" | ⚠️ **主体搞反** | **录行为的是工具本身**（`record` 跑原实现、生成边界输入、落 cases.jsonl）；**Agent 只写 Rust**。README 明说："rust-anything does not translate code" |
| "写 Rust 替代" | ✅ | bridge 生成 crate + 绑定 + `port.rs` 存根，Agent 填 `unimplemented!()` |
| "影子比对保证行为一致" | ⚠️ **这是两层，别混** | ① `diff` = 用录制的 cases.jsonl **回放对拍**（这是正确性主闸）；② `shadow` = 生产双跑 drop-in，返回旧结果并报不一致，`RUST_ANYTHING_MODE=old\|shadow\|new` |
| "Python 快 17 倍、Node.js 快 20 倍" | ⚠️ **数字属实，但有前提** | 都是 **batch 场景**（把整个循环搬进 Rust，一次交 2 万/5 万条）。**逐条调用移植通常更慢**：TS 0.2–0.4x（即慢 2.5–5 倍）、Go 0.93x、Java 0.68x |
| "低内存占用" | ✅ | Rust 无 GC；batch crate 用 mimalloc（**用系统分配器时 Go batch 比单线程还慢**——这条比"低内存"更有信息量） |
| "出错回滚" | ⚠️ **不是自动回滚** | 是**模式开关** + 闸门不通过不许 ship：`RUST_ANYTHING_MODE=old` 即刻切回原实现；gate 不过则 diff/gate 直接失败 |

**额外核实（视频没提但决定能不能用）**：仓库 **2026-11-16 才建仓，到今天仅 3 天**；已 3,322 star / 262 fork / 7 open issue，2026-11-18 仍在高频提交。PHP、C# 仅 **preview**（只能 analyze，不能桥接 unit）；MCP server 状态是 **Tested**（协议测试）而非 Verified；`profile` 是 Tested。

---

## 1. 它是什么 / 不是什么

**不是**：编译器、不是代码翻译器、不是"AI 自动重写神器"。

**是**：给 Agent 装的**一套工程脚手架 + 验收闸门**，补的是"AI 猜不准的那部分"：

1. 时间到底花在哪（profile，跑真实负载）
2. 先移哪个、按什么顺序移（analyze，输出波次与依赖）
3. 怎么桥接（bridge，调用方 API 保持不变）
4. **必须匹配的确切行为**（record，cases.jsonl）
5. 怎么安全发布（shadow 双跑 + 模式开关）
6. **这块算不算做完**（gate，机器判定）

**形态**：Rust CLI + crates.io + npm（预编译二进制，无需 Rust 工具链）+ **MCP server + workflow skill**，一键注入 Claude Code / Codex / Cursor / Gemini CLI（`rust-anything setup`）。形态上和我们自己的 skill 体系完全同构。

---

## 2. 十步主循环（本机实测过前四步）

```
profile ──> analyze ──> bridge ──> record ──> port.rs ──> build ──> diff ──> bench ──> shadow ──> gate
时间花在哪   移什么/顺序   生成crate   原实现真行为    Agent写    编译     回放对拍    快了没    生产双跑   算不算完
```

| 步 | 命令 | 关键机制 |
|---|---|---|
| 0 Profile | `profile <repo> -- node bench.mjs` | 跑真实负载，按语言原生 profiler（node / cProfile / go pprof / JFR / Ruby tracer）出 inclusive time 热点 + 谁在调它 + 哪些循环值得 batch；**会标记"已是编译型（numba/Cython/JAX）→ Rust 收益小"** |
| 1 Plan | `analyze <repo>` | 切 unit、排波次（import 靠前的先移，循环依赖一起移）、每个 unit 选 bridge（napi / wasm / PyO3 / JNI / cgo / magnus）、风险带 `file:line`、给 readiness + priority |
| 2 Bridge | `bridge <repo> <unit>` | 生成 crate + 绑定 + `port.rs` 存根；TS 走 napi-rs/wasm-bindgen + **生成的二进制 wire**（JSON 只兜底，且带 `{"$undefined":true}`、`{"$num":"NaN"}`、UTF-16 代理对标记）；Python 走 PyO3(abi3) |
| 3 Record | `record <crate>` | 跑原实现：生成边界输入（非 ASCII / emoji / `-0` / NaN / int 当 float …）+ **每个参数的语义陷阱**（串长与大小写、有符号除法、溢出边界、浮点打印、Map/Set 顺序）+ 可选 `--from-tests` 抓原测试套件真实调用 → `cases.jsonl`；**跑两遍**把会变的（时间、id）转通配符、顺序不同则乱序比、行数不同则 `...`；存文件指纹 `recorded-from.json` → 原实现后来变了，diff 警告、gate 直接失败 |
| 3b Build | `build <crate>` | 编出 `.node` / wasm / Python ext / so |
| 3c Diff | `diff <crate>` | **回放全部录制用例**，列出不一致 —— 正确性的主闸 |
| 3d Bench | `bench <crate>` | 原实现 vs Rust（含桥接开销）的计时与结论 |
| 4 Shadow | `shadow <crate>` | 生产双跑 drop-in：返回旧结果 + 报不一致，`RUST_ANYTHING_MODE=old\|shadow\|new` |
| 5 Gate | `gate <crate>` | fmt + `clippy -D warnings` + tests + **unsafe 审计** + 无未移植项 + **每条错误路径都有录到的失败用例** + 禁止在原实现返回 error 的地方 `unwrap/expect/panic`（除非标 `// INFALLIBLE: <why>`）+ build + API + behavior |

---

## 3. 性能数字（官方 demo，4 核；仓库自带 benchmark，先验结果一致）

| 语言 | 负载 | 原实现 | 逐条移植 | **批量（batch）** |
|---|---|---:|---:|---:|
| TS/Node | x18n 搜索，50,000 keys | 10 ms | 0.2–0.4x（更慢） | **18–22x**（0.45–0.56 ms，napi+索引结构）/ wasm 单线程 11.5x |
| Python | slugify，20,000 串 | 98 ms | — | **17x** |
| Ruby | slugify 20,000 / shellescape 50,000 | 110 / 88 ms | — | **12.7x / 11.8x** |
| Go | slugify，50,000 串 | 49 ms | 0.93x | **4x** |
| Java | slugify，50,000 串 | 43 ms | 0.68x | **3x** |

- 桥接成本实测：napi 一次同步调用 **22 ns**，传一个参数约 **55 ns** → 逐条调用必然打不过 JIT。
- 真实项目 verdict（作者原话）：vercel/ms 移植 **"a good port and a bad speed target"** —— 975/975 用例全对齐、gate 通过，但逐条调用 0.56x，批量 18x。
- README 头条：**38,251 个录制用例回放，0 不一致**。

---

## 4. 它抓不到什么（对我们最重要的一节）

> **通过 = 与"录到的东西"一致，除此之外一概不管。**

- **没录到的输入就是天花板**：生成器 + 陷阱 + 原测试 + 你手输的 `--inputs`，仅此而已。
- **正则**：Rust `regex` crate 没有 lookahead/backreference；即使能编译，`\w` `\b` `\d` 与忽略大小写在非 ASCII 上与 JS/Python/Java 不同（作者在 vercel/ms 移植中真的踩到：`/i` 不带 `u` 只折叠 ASCII，Rust 默认折叠 Unicode → `"1 ſ"` 会被当秒）。工具会给用正则的文件自动加陷阱（土耳其无点 `ı`、Kelvin 符号、long s、final sigma、ZWJ…），**但真实模式仍要自己 fuzz**。
- **浮点**：数字转字符串的格式（`1e21`、`-0`、有效位数）必须完全一致；`--float-tolerance` 只免四舍五入，**不免格式**。
- **只比对 stdout / stderr / exit code / 写入的文件 / HTTP 响应** → **不比对数据库、网络、信号、时序、内存、并发**。
- **原实现会跑两遍、每个用例跑一遍** → 写文件/连库的代码**副作用会重复发生** → 官方警告：必须在**项目副本 + 测试库 + 环境无生产凭证**下跑。
- **跨平台**：录在哪台机器就只证明那台机器；C 的类型宽度/字节序/编译器相关结果会变。
- **不能跨 bridge 的**（只能留在原语言）：函数参数/返回值、generator/iterator、RegExp、`instanceof`、`Proxy/Reflect/Symbol`、动态 `eval`/`import()`、泛型（仅数据型的 T 可用 `--as-json` 桥接）。

---

## 5. 本机实测（2026-11-19，我方动手，非引用）

环境：本机**没有 Rust 工具链**，故只跑到第 3 步（record）。`npm install -g rust-anything`（1.5.1，含预编译二进制，无 postinstall）→ `rust-anything --version` = 1.5.1 ✅

自建 13 行 Python demo（`slugify.py` + `truncate`）后：

| 步 | 结果 |
|---|---|
| `analyze .` | ✅ 输出迁移计划：1 unit、readiness 96、priority 65、bridge=PyO3、风险 `slugify.py:18 字符串偏移与切片`（并解释 UTF-16 vs UTF-8 偏移差异） |
| `bridge . slugify.py` | ✅ 生成 `rust/slugify-rs/`（Cargo.toml、src/lib.rs、src/port.rs、build.rs、python 包装、rust-anything.json），`port.rs` 里两个函数是 `unimplemented!()` 存根并注明"原实现抛错处要返回 Err" |
| `record rust/slugify-rs` | ✅ **录到 447 个用例**（slugify 219 / truncate 228，0 抛错），并自动追加"非 ASCII \w/\b/大小写折叠"正则陷阱；样例：`{"fn":"slugify","args":["a😀b😀c"],"ok":"abc"}` |
| `build` / `diff` / `gate` | ⛔ 本机无 cargo，**未跑**（需装 Rust 工具链 = 机器级变更，未擅自装） |

**未跑 `rust-anything setup`**：它会改 `~/.claude.json`、`~/.codex/config.toml`、`~/.cursor/mcp.json`、`~/.gemini/settings.json` → 属于 agent 配置变更，按规矩先看现状再动，不该我顺手改。

---

## 6. 对德勤 / Hermes MVP 的借鉴（重点）

> **可抄的不是 Rust，是「录制 → 对拍 → 闸门」三件套，加上"把循环搬进去"的性能观。**

### 6.1 执行器抽象层缺的那块：机器可判定的等价性验收

我们已定的架构原则是"Hermes / OpenClaw / Codex / Claude Code 都是可插拔执行器"，但**至今没有回答：换一个执行器，怎么证明行为没变**？DSH 的 Capability Seam 定义了角色（Definition/Provider/Consumer），也没给 Consumer 侧的验收方法。rust-anything 给的模板直接可用：

| rust-anything | 我们的等价物 |
|---|---|
| `record` → cases.jsonl | 录一批标准任务的 **Agent 执行 trace**：工具调用序列、关键中间产物、最终答复、token/成本/耗时 |
| `diff` → 回放对拍 | 换执行器跑同一批用例，产出**差异表**（漏工具 / 答复不一致 / 成本差） |
| `gate` → 完成判据 | 谁说 done，谁必须过门：必需工具召回 100%、关键事实一致率 ≥95%、成本 ≤ 基线 ×1.2 —— **机器判定，不靠人眼看 diff** |

### 6.2 内核下限可以加第 9 条（建议）

我们内核 v0.1 已有 8 条下限（唯一写入点/授权不可变/指令数据分离/链级熔断/事件溯源+why/零出站/厂商中立/首投灰度）。建议加：

> **第 9 条：任何"替换"（换模型、换执行器、换实现）都必须先有录制基线 + 回放对拍 + 机器闸门；没有基线的改动不允许上线。**

这条与已有的"事件溯源"天然兼容：我们已经在链上存事件，只要把 **回放对拍**接到同一张表（`chain_key` + `trace_id` 天然就是回放单元），就能把"可替换执行器"从口号变成可验收。

### 6.3 "把循环搬进去"这条性能观更值钱

rust-anything 的第一性原理：**逐条跨界调用永远输给 JIT；只有把批循环整体搬进目标侧才赢。**

映射到我们的世界：

- 不要在 Python 侧**逐条**调 LLM（每次一次网络往返）→ 要"一次请求批处理"或"把多个子任务收进一次 Agent 执行"。
- 它的省往返手法可直接抄：**字符串拼成一条 + 偏移量表一次过、数字走 `Float64Array`、结果拼接后切**（napi 实测字符串快 2x、数字快 20x）→ 这就是我们的"批量任务协议"该长的样子。
- 隐含推论：**换执行器的价值 ≠ 换语言的价值**。我们换 OpenClaw/Hermes/Codex 时也要问："哪些热路径值得整体搬运，而不是逐条桥接？"

### 6.4 明确不建议做的

- ❌ 不要把"用 Rust 重写"写进德勤提案或客户交付物（客户栈以 TS/Python 为主，收益点在别的层）。
- ❌ 不要在生产环境跑 `record`/`app record`（会真实执行副作用代码）。
- ❌ 现在别动 agent 配置（`setup`）—— 要接 MCP 就先看现有 `~/.claude.json` / `~/.codex/config.toml` 现状再合并。
- ⚠️ 成熟度：仓库 3 天大，PHP/C# 仅 preview。**只借方法论，不进关键路径**；MIT 许可可商用但代码太新。

---

## 7. 落地建议（低成本试点，两周内可验证）

**试点 A（推荐）**：**Hermes 执行器回放对拍器**（不碰 Rust，纯借方法论）

1. 选题：从内核 kernel 的 24/24 验收用例里挑 10 个 + 3 个真实咨询任务
2. record：跑 Hermes v0.14 一次，录 trace（工具序列 + 答复 + token + 成本 + 耗时）→ JSONL
3. diff：换另一个执行器（Claude Code / Codex / OpenClaw）跑同一批 → 差异表
4. gate：定阈值 → 机器判定 → 出一份《执行器可替换性验收报告》
5. 产出价值：正好补 DSH Capability Seam 里 Consumer 侧的空缺，也是德勤内核"第 9 条下限"的最小实现

**试点 B（更小）**：内核加一条 `replay <trace_id>` 命令，做链路级回放 —— 一个下午的量级。

---

## 8. 事实清单（可核对）

- 仓库：`github.com/erkamyaman/rust-anything`；MIT；主语言 Rust；建仓 2026-11-16；2026-11-19 实测 3,322 star / 262 fork / 7 open issues；最近提交 2026-11-18
- 版本：crates.io / npm 均 **1.5.1**（npm 带预编译二进制，macOS/Linux/Windows；本机实测 `--version` = 1.5.1）
- `docs/STATUS.md`（2026-11-18）自述状态：TS / Python / Go / Ruby / Java / C 六语言 **Verified**（真实项目跑通）；PHP / C# **Preview**；MCP server = Tested；profile = Tested
- 真实跑通记录：json-server（6 units / 3,399 cases / gate 通过）、Fuse.js 3,414/3,414、vercel/ms 975/975、x18n 7,925 cases、CPython `colorsys` 2,400/2,400、Go `path` 2,642/2,642、Ruby `shellwords` 1,617/1,617、JDK 21 4,492/4,492、glibc 1,859/1,859
- 文档：`docs/how-it-works.md`（主循环 / bridge 决策 / analyze 风险表 / **What it can't catch**）、`docs/whole-apps.md`、`docs/real-world.md`（真实跑通细节）、`docs/STATUS.md`、`DECISIONS.md`
- 我方未做：未装 Rust 工具链（故 build/diff/gate 未跑）、未跑 `setup`、未在任何真实项目上试
