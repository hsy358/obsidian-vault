---
title: "Vercel Labs 开源了一个 Zig 桌面应用框架，想做更轻的 Electron 替代方案？"
author: "TJ君"
publish_date: "2026-06-15 13:10:00"
saved_date: "2026-06-15"
source: "wechat"
url: "https://mp.weixin.qq.com/s/t6Wccx3q6ms8Wn0DdUWPdQ"
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/t6Wccx3q6ms8Wn0DdUWPdQ
---
# Vercel Labs 开源了一个 Zig 桌面应用框架，想做更轻的 Electron 替代方案？
这两年桌面应用有一个很明显的现象：很多产品看起来是“原生应用”，但本质上都是一个 Web 应用套了壳。

这条路线并不奇怪。Web 技术栈成熟，React、Vue、Svelte、Next.js 这些工具链开发效率很高，团队也更容易招到会写的人。但问题也很明显：如果用 Electron 这类方案，很多时候相当于给每个应用都带上一个完整的 Chromium 运行时。

这就带来了几个经典吐槽：

- • 安装包大；
- • 启动慢；
- • 内存占用高；
- • 明明只是一个小工具，却像一个浏览器一样重。
所以我今天看到 Vercel Labs 开源的 **Zero-Native** 时，第一反应不是“又一个跨平台框架”，而是：这个方向值得看一下。

它的思路很直接：**用 Zig 做原生应用壳，用 Web 技术写 UI，在轻量和一致性之间做选择。**

---

## 它是什么？

Zero-Native 是 Vercel Labs 开源的一个跨平台原生应用框架，官方描述是：

> Build desktop + mobile apps with Zig and web UI.

翻译一下，就是：用 Zig 和 Web UI 构建桌面、移动应用。

它不是让你完全抛弃前端技术栈，重新去学一套原生 UI 框架。相反，它默认承认一个现实：很多团队还是希望继续用 Web 技术写界面。

但它想解决的问题是：**能不能不要为了一个桌面应用，就默认塞进去一整个浏览器？**

Zero-Native 提供了两种 Web 引擎选择：

- 1. **System WebView**
- • macOS 上使用 WKWebView；
- • Linux 上使用 WebKitGTK；
- • 优点是应用壳更小、启动更快；
- • 缺点是不同平台的 WebView 行为可能存在差异。
- 2. **Chromium / CEF**
- • 通过 CEF 打包 Chromium；
- • 优点是渲染一致性更强；
- • 缺点是体积和运行时负担会更接近 Electron 路线。
这其实是一个挺实用的设计。它没有简单地说“Electron 太重，所以我完全不用 Chromium”，而是把选择权交给开发者：如果你想要轻，就用系统 WebView；如果你更在意渲染一致性，就打包 Chromium。

---

## 为什么是 Zig？

Zero-Native 最值得关注的地方，不只是“又一个 WebView 框架”，而是它把原生层放在了 Zig 上。

Zig 这几年在系统编程圈子里存在感越来越强，常见卖点包括：

- • 编译快；
- • 生成物相对可控；
- • 能比较自然地调用 C；
- • 适合做底层库、工具链、运行时相关项目；
- • 不像 C/C++ 那样背着太多历史包袱。
放到桌面应用框架里，Zig 的价值主要体现在两点。

第一，**原生壳可以更轻**。Zero-Native 的目标不是把大量逻辑塞到一个庞大的运行时里，而是用 Zig 写一个相对薄的 native shell。对小工具、开发者工具、内部应用来说，这个方向天然有吸引力。

第二，**和系统能力打交道更直接**。桌面应用经常需要访问文件系统、窗口、通知、剪贴板、系统 API、本地库等能力。如果底层语言能比较方便地调用 C 和平台 SDK，理论上会比纯 Web 层绕来绕去更直接。

当然，这不代表 Zig 一定比别的语言更适合所有桌面应用。这里的关键在于：Zero-Native 想做的是“Web UI + 轻量 native shell”，而 Zig 刚好适合承担这个 shell 的角色。

---

## 基本用法长什么样？

根据官方 README，Zero-Native 的上手方式比较接近现代前端工具。

先安装 CLI：

```
npm install -g zero-native
```

然后创建应用：

```
zero-native init my_app --frontend nextcd my_appzig build run
```

第一次运行时，它会安装前端依赖、构建生成的 native shell，然后打开一个桌面窗口来渲染你的 Web UI。

它支持的前端示例包括：

- • Next.js
- • React
- • Svelte
- • Vue
这点很关键。它不是要求你用某个全新的 UI DSL，而是尽量复用现有 Web 前端生态。对很多团队来说，这比“重新学一套桌面 UI 框架”更现实。

---

## 和 Electron 有什么区别？

Zero-Native 很容易被拿来和 Electron 对比，但要先说清楚：它现在还不是一个成熟的 Electron 替代品。

Electron 的优势很明显：

- • 生态成熟；
- • 文档多；
- • 案例多；
- • 跨平台一致性强；
- • 大量第三方库和经验可以复用。
它的问题也同样明显：**重**。

Zero-Native 的切入点，就是在“Web 开发体验”和“原生应用轻量化”之间找一个新的平衡点。

如果用 System WebView 模式，Zero-Native 不需要默认把 Chromium 打进应用包里。这意味着应用体积和启动速度有机会更好。但代价是你需要接受平台 WebView 的差异，比如不同系统上的 Web API 支持、渲染细节、版本差异等。

如果用 Chromium / CEF 模式，Zero-Native 又可以把渲染一致性拉回来。但一旦你选择打包 Chromium，它和 Electron 的差异就不再主要体现在“轻量”上，而是更多体现在 Zig native shell、配置方式、安全模型和框架设计上。

所以更准确的理解是：

> Zero-Native 不是简单说“我要干掉 Electron”，而是给 Web 桌面应用提供一个更可调的选项：你可以在轻量和一致性之间自己选。

---

## 我觉得比较值得看的几个设计

### 1. App 配置用 app.zon

Zero-Native 的项目配置主要放在 `app.zon` 里。这里会声明应用 ID、名称、版本、Web 引擎、权限、窗口、导航策略等信息。

示例大概是这样：

```
.{    .id = "com.example.my-app",    .name = "my-app",    .display_name = "My App",    .version = "0.1.0",    .web_engine = "system",    .permissions = .{ "window" },    .capabilities = .{ "webview", "js_bridge" },    .windows = .{        .{ .label = "main", .title = "My App", .width = 960, .height = 640 },    },}
```

这类 manifest 对桌面应用很重要，因为桌面应用不是网页，除了 UI，还有窗口、权限、打包、图标、平台能力等一堆东西需要管理。

### 2. JavaScript 到 Zig 的 bridge 是显式的

Zero-Native 提供 `window.zero.invoke()` 作为 JavaScript 调用 Zig 原生能力的桥。

这个桥不是无脑开放的。官方 README 里提到，它会做：

- • 调用大小限制；
- • origin 检查；
- • permission 检查；
- • 只路由到注册过的 handler。
这个设计我觉得是对的。很多 WebView 应用最大的问题就是边界不清：前端页面到底能不能调用本地能力？能调用哪些？外部链接打开后还算不算可信页面？这些问题如果不在框架层明确，后面很容易变成安全坑。

### 3. 安全模型默认把 WebView 当成不可信

这是 Zero-Native 让我比较有好感的一点。

官方强调：WebView 默认被视为不可信，native commands、permissions、navigation、external links、window APIs 都是 opt-in，并且由策略控制。

这和现在的应用形态很相关。很多桌面应用会加载本地页面、远程页面、插件页面，甚至可能让 AI Agent 或脚本参与操作。如果 WebView 和本地能力之间没有明确权限边界，风险会被放大。

### 4. 同时考虑桌面和移动嵌入

Zero-Native 目前主要看点在桌面，但 README 里也提到有 iOS 和 Android embedding 示例，通过 `libzero-native.a` 的 C ABI 接入宿主应用。

这说明它不只是想做一个桌面壳，而是想把 Zig 原生层做成可以被不同平台宿主复用的基础设施。当然，移动端现在更应该当作早期探索，不建议直接拿去押生产项目。

---

## 它适合谁关注？

我觉得 Zero-Native 适合这几类人先关注：

### 1. 做桌面工具的开发者

比如你想做一个小型开发者工具、效率工具、内部管理工具，但又不想每个应用都打包一个巨大的运行时。Zero-Native 这种 System WebView 路线值得看。

### 2. 已经有 Web 前端能力的团队

如果团队熟悉 React、Vue、Svelte、Next.js，又想做桌面应用，那么 Web UI + native shell 的路线比完全转向原生 UI 更容易接受。

### 3. 对 Zig 感兴趣的开发者

Zig 一直被很多人看作系统编程和工具链方向的新选择。Zero-Native 提供了一个更贴近应用层的观察样本：Zig 能不能进入桌面应用框架和跨平台运行时这一层？

### 4. 关心 Electron 替代方案的人

如果你一直觉得 Electron 太重，但又不想放弃 Web 前端生态，可以关注 Zero-Native、Tauri、Wails、Neutralinojs 这一类项目。它们共同的问题意识都是：Web UI 能不能更轻地进入桌面应用？

---

## 需要注意什么？

先别急着把它当成生产框架。

Zero-Native 官方 README 里已经写得很清楚：**pre-release**。也就是说，它还处在预发布阶段。

这意味着几个现实问题：

- 1. **生态还早**文档、社区、问题解决经验、第三方集成，都不可能和 Electron 这种成熟方案比。
- 2. **跨平台细节需要验证**System WebView 的优势是轻，问题是不同平台行为不完全一致。尤其是复杂前端应用、动画、媒体、权限、文件访问这些场景，都需要实际测试。
- 3. **Windows / Linux / macOS 的体验可能不均衡**README 提到桌面支持覆盖 macOS 11+、Linux 和 Windows build paths，但具体到日常开发体验、打包流程、CEF 支持成熟度，还需要项目继续迭代。
- 4. **移动端不要过早期待**iOS / Android 示例说明它有这个方向，但现在更适合看架构思路，不适合直接理解成“成熟跨端 App 框架”。
所以我会把它定位成：**值得关注的早期开源项目，而不是可以无脑替换 Electron 的成熟方案。**

---

## 小结

Zero-Native 有意思的地方，不在于它喊出了“替代 Electron”的口号，而在于它把几个趋势放到了一起：

- • Web UI 仍然是高效率的界面开发方式；
- • Electron 的体积和资源占用确实让很多人不满意；
- • Zig 正在从系统编程圈子向工具链、运行时、应用壳这类场景扩展；
- • 桌面应用越来越需要明确的 WebView 安全模型和权限边界。
如果你正在做小型桌面工具、开发者工具、内部应用，或者只是想观察 Zig 能不能进入更上层的应用开发生态，Zero-Native 值得收藏一下。

但如果你现在要做一个商业级桌面产品，我建议还是谨慎。现阶段更适合用它做 demo、原型和技术验证，而不是马上迁移生产项目。

---

## 项目地址

GitHub：https://github.com/vercel-labs/zero-native

官方文档：https://zero-native.dev
