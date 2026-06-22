---
title: 打不过就加入！OpenAI 亲手把 Codex 塞进了 Claude Code
author: AI信息Gap
publish_date: '2026-04-02 08:00:00'
saved_date: '2026-05-31'
source: wechat
url: https://mp.weixin.qq.com/s/PcZVz9Xf2-SFE_9_e41uVw
type: wechat-article
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
  source_url: https://mp.weixin.qq.com/s/PcZVz9Xf2-SFE_9_e41uVw
description: 你现在可以在 Claude Code 里用 Codex 了。
timestamp: '2026-04-02T08:00:00'
resource: https://mp.weixin.qq.com/s/PcZVz9Xf2-SFE_9_e41uVw
tags:
- AI
- Claude
- notes
- 公众号
---
# 打不过就加入！OpenAI 亲手把 Codex 塞进了 Claude Code
你现在可以在 Claude Code 里用 Codex 了。

还是 OpenAI 官方出的开源插件。

GitHub 仓库名叫 `codex-plugin-cc`。cc，Claude Code 的缩写。两天，8000 个 star。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VpHtkRLWJljZ1RnFSqnP55KgSX0Z0xmAFPu0wCnRMricZJTia22p4bYYKOCKWOr7ibg6kIZuYb5mQEpFgBDDxhQJqMpxib2nDGmPRSe6vcrS3RU/640?wx_fmt=png&from=appmsg)
把自家的 AI 编程助手 Codex 做成插件，装进竞争对手 Anthropic 的 Claude Code 里。

OpenAI，你真是个「商业鬼才」。

这就相当于你去肯德基点餐，菜单上多了个麦当劳。

---

OpenAI 开发者体验负责人 Romain Huet 这样说。

「我们看到 Claude Code 用户已经在自己接 Codex 做代码审查，并在复杂任务中用 `GPT-5.4`。我们就想，何不让这更简单一点？」

![](https://mmbiz.qpic.cn/mmbiz_png/VpHtkRLWJljLToCrs0gene6o7gp7KFzJU1lw82eADiaKh4W9BzLiczDzZUmx9sQAF8icvZL0CicdE8koQeoGQCAcLBREaYbF9Gg85nib4nqciaAyw/640?wx_fmt=png&from=appmsg)
这条推文，88 万次浏览。翻译一下，「打不过就加入。」

Claude Code 年化收入 25 亿美元，每天有 13.5 万个 GitHub 提交。OpenAI 应用 CEO Fidji Simo 两周前在内部全员大会上直接启动了「红色警戒」Code Red。然后砍掉了 Sora、Atlas 浏览器、硬件项目。算力资源全部押到更赚钱的推理、编程上。

OpenAI，慌了。

---

现在就能用。前提条件，Node.js 18.18 以上版本。

打开 Claude Code，三条命令搞定。

```
/plugin marketplace add openai/codex-plugin-cc/plugin install codex@openai-codex/reload-plugins
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VpHtkRLWJlhB8hl4QWy411bVJCiarwprDeBhLCCiaocmRsJjxiavtRrhiaHEHwPWZkmdx9vicl51GRia0TJbldB5fWqFTw8MS4X8q9Ybibt0rVHwjA/640?wx_fmt=png&from=appmsg)
然后运行 `/codex:setup`，它会自动检测你本地有没有安装 Codex CLI。没有的话它会帮你装，你也可以自己来，`npm install -g @openai/codex`。

划重点，这个插件不会另外装一套 Codex。它直接调用你电脑上已有的 Codex CLI，配置和登录状态全部共用。没登录的话，在 Claude Code 里输入 `!codex login`。ChatGPT 账号或 OpenAI API Key 都能登。

ChatGPT 免费用户也能用，有 ChatGPT 账号就行。插件用量自动算入你的 Codex 配额。

---

配置完你的 Claude Code 会多出一组命令。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/VpHtkRLWJlgShR8ibY0zjK8U2xk1Poib4ibSoBiavmTHANeaXlxDc0y9AYBquzXWDnZXIlskywBxcgZfIMa5GIcysfdbdOkBGyichhV61icOMUwtM/640?wx_fmt=png&from=appmsg)
`/codex:review`，让 Codex 帮你过一遍代码，只看不改。默认审查当前未提交的修改，加个 `--base main` 覆盖整个分支。多文件改动可以加 `--background`，Codex 自动在后台运行。

```
/codex:review --base main --background
```

审完了用 `/codex:status` 查进度，`/codex:result` 看结果。

`/codex:adversarial-review`，故意挑毛病。它专门质疑你的设计选择，追问竞态条件，挑战你的回滚方案。还可以指定让它重点关注某个方向，比如：

```
/codex:adversarial-review --background look for race conditions
```

`/codex:rescue`，直接把活儿甩给 Codex。写代码、调试 bug，Codex 化身后台牛马，你还能继续用 Claude Code 干别的。想省 token 还可以指定小模型。

```
/codex:rescue --model gpt-5.4-mini --effort medium fix the flaky test
```

OpenAI 这招，绝了。

---

还有个实验功能，「强制审查」。

运行 `/codex:setup --enable-review-gate`，开启之后每次你关闭 Claude Code 前，Codex 都会自动审查。有问题直接拦住，让 Claude 改完再说。

OpenAI 自己在文档里加了个警告，「两个 AI 互审，可能陷入死循环，配额烧得飞快。建议盯着屏幕的时候再开。」

---

每一次你在 Claude Code 里触发 `/codex:review`，底层跑的都是 OpenAI 的模型，消耗的都是你的 ChatGPT 配额。

这就相当于你来到 Anthropic 的店里，但有一部分钱流向了 OpenAI。

开发者选了 Claude Code，OpenAI 选择「打不过就加入」。

---

> 我是木易，Top2 + 美国 Top10 CS 硕，现在是 AI 产品经理。关注「AI信息Gap」，让 AI 成为你的外挂。

---

[![](https://mmbiz.qpic.cn/sz_mmbiz_png/VpHtkRLWJlgrK9C7hWibUvHqHJthShDhB0V1XuNxkxWhWowrbwe4phKcO1JAVQWCiajt15Gs8K0FStzlNNUcMoOwUhjH06DUibkjuHibe2BX8u4/640?wx_fmt=png&from=appmsg)](https://mp.weixin.qq.com/s?__biz=MzkwMzYzMTc5NA==&mid=2247512867&idx=1&sn=527fac560927326c65d10d116ec47710&scene=21#wechat_redirect)
