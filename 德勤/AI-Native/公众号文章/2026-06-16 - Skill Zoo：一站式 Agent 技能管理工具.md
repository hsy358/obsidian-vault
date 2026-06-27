---
title: "Skill Zoo：一站式 Agent 技能管理工具"
author: "星汐引力"
publish_date: "2026-06-16 06:11:00"
saved_date: "2026-06-27"
source: "wechat"
url: "https://mp.weixin.qq.com/s/r27iCI7rFCDnVWzkbOO0RQ"
---
# Skill Zoo：一站式 Agent 技能管理工具
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/e7Am6S8kTlicDich5XB33wb0oyAeF5KduLGBISkfqaSIBAZnBdj6BnTZtqZibA6psYRxnPO2OrK5uf0lxeAF7rVicCPgmLgm7ibyP5YheK7tChAw/640?wx_fmt=webp&from=appmsg)

> 给所有流浪的技能宝宝一个家

自 Coding Agent 爆火以来，Agent 技能作为其能力的重要载体也备受关注。 Agent 技能本质上是文档，但凭借其可插拔、任务间通用和渐进式披露等特性，已经变成了 prompt 的一种独特存在形式。

Agent 技能尤其擅长有套路、有 SOP、需要风格迁移的任务，比如网页设计、数据分析、制作幻灯片等。下面是我用 ThariqS 佬开源的 HTML 模板做的 Slide。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/e7Am6S8kTl9ujCH7X3HYM9z0GDsQdpM426emOHj4WX1kUl0icWmr7XCUdLPPlNsNY5J1zcAcgAL7PfVQicbxUCw4WAZP9B2CbDEHwWbUYO66Q/640?wx_fmt=jpeg&from=appmsg)

这个 Slide 偏简洁风，如果你喜欢其它风格，可以上 GitHub 搜索相关 Skill。

### 一、如何管理技能

Agent 技能良莠不齐，下载下来用不用得上另说，上下文总归被占用了。如果技能数量太多，技能列表甚至会被截断。

因此，技能是需要管理的：不用的要删除，过时的要更新。同时技能管理又是一件挺主观的事，哪些技能有用，哪些技能质量高，需要我们主动判断。阅读方便就变成一个很重要的指标。npx skills 这种 CLI 不方便阅读，需要一个 App 来提供阅读和管理功能。

Skill Zoo 就打算做好这件事。它提供了一系列随点随用的功能，帮我们降低技能管理成本，拉近我们和技能之间的距离。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/e7Am6S8kTlicOGX120XZMcjQGsVMdyKHVDRJLYYWc9aTLvRE3OflFGwHiauzhncSdqAUYgZEuktNGWLicHkpQb98OdLuImUBxN1LwMSJRYguNM/640?wx_fmt=jpeg&from=appmsg)

项目地址：luochang.ink/skill-zoo

### 二、产品设计

为了达成这个目标，我开发了覆盖 Agent Skills 整个生命周期的管理功能。

#### 2.1 SSOT 模式

为解决 Agent 技能跨编程工具复用的问题，Skill Zoo 采用 **唯一真实源（SSOT）+ 软链接** 的方法，将已有技能链接至其他编程工具的 Skill 目录使用。

SSOT 是什么？Claude Code 和 Codex 都有技能文件夹。如果一个技能分别存放在不同的技能文件夹里，会造成技能重复存放、技能版本不可控等问题。SSOT 就是维护唯一的技能文件夹，统一管理技能。

```
# 唯一真实源~/.agents/skills/web-search/# Agent 目录只放软链接~/.claude/skills/web-search  →  ~/.agents/skills/web-search/~/.codex/skills/web-search   →  ~/.agents/skills/web-search/
```

这里存在一个 trade-off。如果把用户技能收归 SSOT 目录管理，对架构是最优的。但如果用户同时在使用其他工具，比如 npx skills，其更新功能依赖技能目录里的真实文件而非软链接。强制收归统一目录管理将导致更新失败。

选择最优架构，还是尊重用户习惯，这是一个产品决策。我最终还是决定尊重用户习惯，宁愿增加一些架构复杂度，也不强制移动用户文件。只有对原本就在统一目录下或使用 Skill Zoo 安装的技能，才以 SSOT 的方式管理。

#### 2.2 搜索发现

搜索支持模糊匹配，比如搜索「stock」就可以找到股票相关的技能，也可以直接输入 GitHub 链接或 repo_owner/repo_name 仓库标识。

![](https://mmbiz.qpic.cn/mmbiz_jpg/e7Am6S8kTl8HvyDMv0GPEicicxffNRAfH4orMr55vmb5JnfoDxiccwEPTPnYvjgJUYhXJSKz2OPMIiaj1LVcRfYvjJN9Eibdd0vD0WTkGz9a2lNY/640?wx_fmt=jpeg&from=appmsg)

进入仓库详情页，Skill Zoo 会自动下载技能对应的 GitHub 仓库，并解析仓库中的全部技能，提供给用户安装。

![](https://mmbiz.qpic.cn/mmbiz_jpg/e7Am6S8kTl88CnM1sFoH2bjk7pKMnS9gV7iacMdDic6xR3BTqv1fuThxmribwA9K9u3eL0asRYxGwm9FgAeZ9Opm3lzibgavFgC5t0ImEmVVSrw/640?wx_fmt=jpeg&from=appmsg)

#### 2.3 仓库筛选栏

回到 App 首页，点击对应的仓库按钮即可进入仓库页。这里左边展示该仓库下的技能，右边展示仓库 README.md 中的内容。

![](https://mmbiz.qpic.cn/mmbiz_jpg/e7Am6S8kTl8EXiagGlGv0sIVWicwGlKSIGDXYXG7E90M8vNpsjKGESp6gjwoxibR6JQVeicribF4MxKyK7rWWIYZGheCDwQyopW6OichkwaFCUrjg/640?wx_fmt=jpeg&from=appmsg)

#### 2.4 批量管理

出于防误触的考虑，技能卡片页没有做批量管理功能。如果需要批量管理，请点击右上角的视图切换按钮，切换到列表视图，然后点击复选框，即可批量归档或删除技能。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/e7Am6S8kTl9fq8OPPw7GCdlduFafyfA24Q7xcrDyc5OtCpFsUSM9lWMOBEGvp1okuMKYReiaWKajD7YuJd2bvmON0yn9iaEloLIkOTW59dsB8/640?wx_fmt=jpeg&from=appmsg)

#### 2.5 一致性检查

点击侧边栏的「一致性」按钮，进入一致性检查页面。该页面提供三种一致性检查，帮助我们发现技能重复、版本冲突、格式不规范等问题。

![](https://mmbiz.qpic.cn/mmbiz_jpg/e7Am6S8kTlicXGy7icdN6N1JvVkKoDWBeCtPQfw1DgnibicjUhriaMxia9GibLIAQ3TSf6xEk2PuMSbmtqormID0dZEw4jgYmI1HHL2UJwLZy47gXQ/640?wx_fmt=jpeg&from=appmsg)

#### 2.6 技能详情页

技能详情页支持软链接、查看、编辑、删除技能。还提供安全审计按钮，点击即可获取该技能在 skills.sh 社区的安全审计结果。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/e7Am6S8kTl9T0tlQZ7T5g72oyCia6tKaOyACzkd5gAEkclcnQapT9nz8ZJ2JbghozZicPhxLX1j1ibeeV3XNfdV84UKaynQKo1Dibjfd70fOOY8/640?wx_fmt=jpeg&from=appmsg)

### 三、漫谈 Agent Skills

一提起 Agent 技能，很容易联想到「顷刻炼化」这个词。大家往 Agent 技能里写的，往往是自己擅长且 AI 不擅长的事。我感觉发明 Skill 的人是在利用人民群众的免费劳动力给大模型找不足。所以下一代 AI 训练要做的事很简单，只需要将这些 Skill 内化，就能提升大模型在相关场景的能力。短期看大家被炼化成 Skill，长期看大家都要被炼化进模型。

Agent Skills 数量这么多，从中炼化出东西不奇怪。但并非所有技能都值得被炼化，那些偏流程、偏业务、不够泛化的技能，大模型未必看得上。所以 Agent Skills 长期看仍有价值。特别是那些只属于你、只服务于长尾需求的 Skill，很难被取代。

### 四、下载和安装

Skill Zoo 基于 MIT 协议开源。你可以从 GitHub Releases 获取安装包。macOS 用户下载 dmg，Windows 用户下载 exe。安装包通过 GitHub Actions 制作，构建过程透明、可审计，完全可以放心使用。GitHub 链接：

https://github.com/luochang212/skill-zoo

期待您用 Skill Zoo 探索更多 Agent 技能。如果这个 App 对你有帮助，欢迎 Star 我们的 GitHub 仓库。
