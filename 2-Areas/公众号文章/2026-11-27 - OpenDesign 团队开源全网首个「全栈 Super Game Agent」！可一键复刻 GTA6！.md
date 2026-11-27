---
title: "OpenDesign 团队开源全网首个「全栈 Super Game Agent」！可一键复刻 GTA6！"
author: "开源星探"
publish_date: "2026-11-27 07:46:00"
saved_date: "2026-11-27"
source: "wechat"
url: "https://mp.weixin.qq.com/s/yVTxkqCJnYOkwdi5-1mZrQ"
---
# OpenDesign 团队开源全网首个「全栈 Super Game Agent」！可一键复刻 GTA6！
AI 写代码这件事，已经从「能帮你补个函数」走到了「能帮你搭个完整的 Web 应用」。

但有一个领域，LLM 和代码 Agent 始终在边界线上打转——那就是游戏。

原因很简单：游戏不是静态的。它有实时渲染循环、状态耦合、场景接线、物理引擎、动画系统……几百上千个文件互相咬合，牵一发动全身。

让 Claude Code 帮你写一个 React 组件很轻松，但让它从零搭一个能跑起来的 3D 竞速游戏？大概率是跨几个文件就开始出现场景断连、状态错乱、逻辑打架的情况。

但昨天，OpenDesign 团队正式在 GitHub 开源了 **OpenGame**。也是全网首个开源的全栈游戏工作室。

![](https://mmbiz.qpic.cn/mmbiz_png/rfBHhQhezUjhKxk7aeibulGsyoayzf2rHD6euIUpQQccQHGgOHF7H6Q6WZwhGdQYwrbpPvXMY9N3M5Ha9EkhAzwSmK2MLYnxTyQEEXTAg41k/640?wx_fmt=png&from=appmsg)

📦 4 Parts + Conclusion

👉 滑动

PART 01

OpenGame 是什么？

PART 02

四个让游戏开发者兴奋的亮点

PART 03

快速上手

PART ///

写在最后

01

PART

## OpenGame 是什么？

**它是首个开源的「全栈 Super Game Agent」——把你的 DeepSeek、Claude Code、Codex 或任意本地编程 Agent，变成一座开源版虚幻引擎 + Unity + 小游戏变现工作台。**

**![](https://mmbiz.qpic.cn/sz_mmbiz_png/rfBHhQhezUgrsVCMqoaUUNbya4D9vVdtmSMCarIQR0ibahsjYMBzOtfOgqoHUBsxPx8bDc2Kz0Wnt6szF5ia2oIIajrIkQy6HzdBQ5iaWP8nh4/640?wx_fmt=png&from=appmsg)**

背后团队是 OpenDesign——就是那个之前做了「开源 Claude Design 替代品」的团队，已经在 AI 设计领域积累了 150+ 设计系统、17 个 Agent 适配器和 Apache 2.0 开源生态。这次跨界做游戏，一出手就是大格局。

OpenGame 的定位不是「AI 帮你写游戏代码」，而是覆盖了两条完整的生产链：

3A 级 3D 游戏链 从一句话创意 → 可玩的 3D 动作/竞速/开放世界，驱动 full-stack 3D gameplay、美术、音乐、配音

爆款小游戏变现链 从模板 Remix → 自动平衡检测 → 无头测试 → 9:16 Playable Ads 导出 → 对接微信小游戏、TikTok、抖音

而且它的核心原则是 **BYOA + BYOK（Bring Your Own Agent + Bring Your Own Key）**——不锁模型、不锁 Agent、不锁 API Key，所有代码、美术、音乐、配音、Three.js 3D 引擎全部开源（Apache 2.0）。

02

PART

## 四个让游戏开发者兴奋的亮点

### 1. 🎮 一句话生成 3A 级 3D 游戏

OpenGame 支持直接驱动 **DeepSeek（DSH）、Claude、Codex、Gemini** 等大模型，从一个 prompt 到可玩的 3D 动作、竞速、开放世界游戏。

它内置了 Game Skill 架构——这是从论文里搬过来的核心设计：

Template Skill 从每次生成中积累项目骨架模板，越用越稳

Debug Skill 维护一个「已验证修复」的活协议，Agent 遇到集成错误时先查协议而不是瞎试

这两个 Skill 加上团队自研的 **GameCoder-27B** 专用模型（三阶段训练：持续预训练 → 监督微调 → 执行强化学习），解决的正是之前 LLM 做游戏最容易翻船的跨文件不一致和场景接线问题。

### 2. 🔄 25 个可玩模板，一键 Remix & Re-style

如果你不想从零开始「造轮子」，OpenGame 直接打包了 **25 个开箱即用的完整游戏模板**，所有模板都带完整源代码、美术资源、控制逻辑和本地化。分三大类：

**3D、体素 & 动作游戏（16:9）：**

Tidebreaker——风暴群岛快艇竞速，八个检查点、物理波浪、礁石躲避

Starlight Bastion——体素空间塔防，五波递增敌人，roguelite 升级系统

Skyline Courier——赛博朋克屋顶跑酷，90 秒送三个包裹，含 wall-kick 和 double-jump

Neon Drift——霓虹公路赛车，近失擦碰充能 boost，冲击距离记录

Harbor Skirmish——3D FPS，grappling-hook + double-jump + slide，完整战斗系统

**风格化叙事 & 氛围游戏（16:9）：**

Glyph Garden——动漫三消，24 步内 2200 分，连锁 bloom 特效

Lantern Hop——像素平台跳跃，狐狸主角，月光屋顶 + 灯笼收集

Lighthouse Log——视觉小说 + 生存，七夜守灯塔，燃料管理 + 无线电选择

**9:16 竖屏小游戏 & Playable Ads：**

Gate Legion——算术门跑酷（+10 / ×2），Boss 军队对撞

Pin Rescue——拔针解谜，水 + 熔岩 = 石头，五关通关

Sky Runner——3D 霓虹悬浮滑板跑酷，车道切换 + 金币收集

每个模板都能 **Remix（改玩法参数）** 或 **Re-style（换美术风格）**，几分钟就能把一个现有游戏改成自己的 IP。

### 3. 💰 构建 → 验证 → 变现，全链路打通

这是 OpenGame 跟其他 AI 游戏生成工具最大的区别：它不只是帮你生成游戏，还帮你 **验证能不能跑、能不能卖**。内置工具链包括：

自动逻辑检查 静态分析 + 规则验证

平衡模拟 数值平衡自动测试

Headless Playtesting：无头浏览器自动试玩

封面 & 预告片自动生成 用于上架和推广

竖屏 Playable Ads 导出：单文件导出，直接能给微信小游戏、TikTok、抖音用

### 4. 🔓 22 个本地 Agent 全支持，彻底不锁

OpenGame 的 README 里列了 **22 个支持的本地 Agent**——从 DeepSeek TUI/Harness、Claude Code、Codex、Cursor Agent、Kimi CLI、Qwen Code，到 Aider、Devin、Trae CLI 全都在。任何你正在用的 Agent 都能接进来，配好 API Key 就能直接驱动。

03

PART

## 快速上手

### 方式 1：给你的 Agent 贴一段 Prompt（最快）

直接把这段 prompt 贴到你用的 Agent 里，它会自动帮你完成 OpenGame 的连接和安装：

`Follow https://github.com/nexu-io/opengame/blob/main/docs/opengame-setup.mdto connect OpenGame to this agent. For a new install, use a shallow clone(--depth 1) and skip LFS downloads. Open the Game Studio template galleryso I can choose a game. Fetch that game‘s assets when I play or remix it.`

支持 DeepSeek TUI/Harness、Claude Code、Codex、Cursor、Gemini CLI、Kimi CLI 等全部 22 个 Agent。

### 方式 2：用 Skills CLI 一键安装

`npx skills add nexu-io/opengame --skill opengame`

安装主入口 Skill 后，Agent 就能调用 12 个 `openmotion_game_*` 工具，打开 Game Studio 界面浏览模板。

### 方式 3：从源码本地启动 Studio

需要 Node.js 22.18+（CI 用 26.11.1）、Git、Git LFS、npm：

`# 浅克隆，跳过 LFS 下载，加速git -c filter.lfs.process= -c filter.lfs.smudge= \    -c filter.lfs.required=false \    clone --depth 1 --single-branch --branch main \    https://github.com/nexu-io/opengame.gitcd opengamegit lfs install --local --skip-smudgenpm cinpm run build:studionpm start`

启动后直接浏览模板目录即可，**Tidebreaker 快艇竞速模板支持离线运行**，其他模板在首次玩或 Remix 时才下载资源。

///

LAST

## 写在最后

OpenGame 现在还非常新——GitHub 昨天才开源，463 Star 说明它还在早期发酵。

但 OpenDesign 团队的底子、arXiv 论文的技术深度、25 个可玩模板的丰富度、以及变现链路的完整度，都说明这不是一个蹭热点的 Demo。

如果你是独立开发者想试试 AI 做游戏，或者想做小游戏变现但不会代码，或者只是好奇 Agent 能不能真的把「一句话」变成「可玩的东西」——这个项目值得关注。

GitHub：https://github.com/nexu-io/opengame

![](https://mmbiz.qpic.cn/mmbiz_gif/NjA8gwicXyeKqAjyn8A3ob9xT4DDY8DB3JCvIaM6JKWXFsgCxznXicJhpRYJ5MIPb9xvgGA4WYhPagIKorlScib0Q/640?wx_fmt=gif)

如果本文对您有帮助，也请帮忙点个 赞👍 + 在看 哈！❤️

**在看你就赞赞我！**

![](https://mmbiz.qpic.cn/mmbiz_gif/NjA8gwicXyeLZdEkueqhds4y07sImrPvibkDIsnVCibl5ibS6jSiccRh6RtH8ZqBPBWSib0kn7Ep6mP5YPJCJkraJ3kw/640?wx_fmt=gif)
