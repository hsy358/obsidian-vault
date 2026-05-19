---
title: "AI 终于能写 PPT 了（不是糊弄你的那种）"
author: "AI小白笔记本"
publish_date: "2026-05-09 19:48:14"
saved_date: "2026-05-10"
source: "wechat"
url: "https://mp.weixin.qq.com/s/H7OyisP2xlsRiEcLK21kvg"
---
# AI 终于能写 PPT 了（不是糊弄你的那种）
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/z316SLBBS3kZYof2MPqtiaoia9DVBJ0lJ7JIOerrHxuIzsfDndGibKlo9jVB7Rwlgblew3HRxiaDSax5xpxmYaGWewVtGDI5icphU7dRIogsNdLM/640?wx_fmt=jpeg)

---

你有没有让 AI 帮你写过 PPT？

生成一堆文字，格式乱掉，图片不知道跑哪去了，还得自己一页一页手动调——最后发现，还不如自己写。

**这个工具专门解决这件事。**

---

## 它叫 OfficeCLI

开源免费，一行代码，让 AI 真正"掌控" Word、Excel 和 PPT。

不是帮你写内容——是让 AI **直接操作文件本身**。创建、修改、添加图表、调格式……全程不需要打开 Office。

以前 AI 生成 PPT，是这样的：

现在 OfficeCLI 只要这样：

officecli add deck.pptx / --type slide --prop title="Q4 Report"

**一行命令，搞定一张幻灯片。**

---

## 先看效果，再聊原理

这是 AI 用 OfficeCLI 全自动制作 PPT 的过程：

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/z316SLBBS3mV671WBN8ibcAAibTMMzWcOic1BdYz9EVU72XdMExyXlqRo3tfDGpmDdMGFa3vhkBbqu15DqvhgiaBia8OnTJMe67P317apQBU7VEs/640?wx_fmt=gif)
没有模板，没有人工干预，AI 自己读内容、排版、加图表，全程自动完成。

Word 也一样：

![](https://mmbiz.qpic.cn/mmbiz_gif/z316SLBBS3lDXBBlVg6sVSnbcS1Y3BTkicCFYDHDSMRT5AfXGiaGzsaxia9TYrJFKEkAUicibrGibrPHVTtNNmWWE6mfga86ZTaUAeV9w0ic9hEmME/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/z316SLBBS3mJptWHCuODNsaP1ic4xZa8aW2onHPtn90jWzGEdk6TXqeGZTeYQbsjYLoWkc7pF6Bmzu9gQt1vibicwrfXcicnRE7Mbnq28Gb4PfI/640?wx_fmt=gif)
Excel 数据处理、图表生成：

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/z316SLBBS3nvBzY3ol0oX3gDeMibGibeQ6kxWkFkcOkUtHd5eAJ6wX5SwibfFufuKVBUgxFx456DVlKpN9CnfBZtj9AOC2x32KnGwshVcKohF4/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/z316SLBBS3nt4sLSE8n2ghgxE81HF8CibRNZ7iaUqFFupPLjKgKg8ykZvE90VibykLIJhTAszlqxHJmicIia0vbNqptC6ySgibEFveB1a2rPbJXec/640?wx_fmt=gif)

---

## 为什么说它是"AI 原生"的？

普通 Office 工具是给人设计的——点击、拖拽、菜单。AI 用起来非常别扭。

OfficeCLI 从一开始就是给 AI 设计的，三个关键差异：

**1. 路径寻址，AI 不会迷路**

每个元素都有稳定的路径，比如 `/slide[1]/shape[2]`。AI 可以像访问文件夹一样精准定位任何一个元素，不需要理解底层 XML。

**2. AI 能"看见"自己做的东西**

内置渲染引擎，可以把文件渲染成 HTML 或截图，AI 能检查自己的输出，发现"这个标题溢出了""两个形状重叠了"，然后自己修复。

以前 AI 生成 PPT 是"盲跑"——它根本不知道做出来长什么样。

**3. 结构化 JSON 输出，不需要猜**

{

"tag": "shape",

"path": "/slide[1]/shape[1]",

"attributes": {

"text": "Revenue grew 25%",

"x": "720000"

}

}

每个操作都有确定性的返回值，AI 可以验证、纠错、自愈，不需要人工介入。

![](https://mmbiz.qpic.cn/mmbiz_jpg/z316SLBBS3mL0r0mmrHNtTylnT5m4yI9oDxxHDMSpVCW7zry0QIUMpiaIkvH0y9zKlpOKWUTg4e0QCOtNrvFR2BUEz4pMnPNLT7jCib9SpUO0/640?wx_fmt=jpeg)
👋 感觉这工具值得深入研究？扫码加我微信，备注【AI交流】，和一群爱折腾 AI 的朋友一起聊~

---

## 三种格式，一个工具全搞定

格式

读取

修改

创建

Word (.docx)

✅

✅

✅

Excel (.xlsx)

✅

✅

✅

PowerPoint (.pptx)

✅

✅

✅

Excel 还内置了 150+ 函数自动求值——你让 AI 写 `=SUM(A1:A10)`，它马上就能读到计算结果，不需要打开 Excel 重算。

---

## 装起来其实很简单

# macOS / Linux

curl -fsSL https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.sh | bash

# Windows (PowerShell)

irm https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.ps1 | iex

装完运行 `officecli install`，它会自动检测你用的 AI 工具——Claude Code、Cursor、VS Code Copilot——然后自动安装对应的技能文件。你的 AI 助手马上就能操作 Office 文档，不需要额外配置。

不想用命令行？也有桌面应用版本 [AionUi](https://github.com/iOfficeAI/AionUi)，用自然语言描述，底层由 OfficeCLI 驱动。

---

## 适合谁用？

**开发者**：从数据库自动生成报告、批量处理文档、在 CI/CD 里构建文档流水线。

**AI 重度用户**：让你的 Agent 不只会聊天，真正能交付可以用的文档。

**有模板需求的团队**：设计一次版式，用 `{{占位符}}` 填充 N 份，每份格式完全一致，零 token 成本。

---

开源地址：**github.com/iOfficeAI/OfficeCLI**

---

看到这里了，说明你是真爱👀

点个**赞和在看**支持一下。

搜索公众号**「AI小白笔记本」**，每周都有 AI 实用干货，不整虚的。
