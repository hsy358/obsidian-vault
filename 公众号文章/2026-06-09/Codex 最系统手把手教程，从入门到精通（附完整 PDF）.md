---
title: "Codex 最系统手把手教程，从入门到精通（附完整 PDF）"
author: "爱AI的大刘"
publish_date: "2026-06-09 15:45:52"
saved_date: "2026-06-09"
source: "wechat"
url: "https://mp.weixin.qq.com/s/_iVwGQL-sQ6XYTNktKYb3A"
---
# Codex 最系统手把手教程，从入门到精通（附完整 PDF）
没装、没账号、想接国产模型，可能是全网最全最细 Codex 教程。

![](https://mmbiz.qpic.cn/mmbiz_png/J1Cdba5GUc3nKVySdUY627eibbx6iaKNVGpy0eP97lfn7yTBAia7Qs8pBibpqDBAqErDhZHRMsGI3HdYqRrSac3FvZkZKppId1PAMl1nBesWiac4/640?wx_fmt=png&from=appmsg)

✍️ 作者: 大刘
📝 编辑 / 排版: 大刘
🎨 这是大刘的第 63 篇原创干货

Codex 应该是 26 年最值得大家学习的 Agent 工具之一。

生态也在 OpenAI 的打磨下，越来越完善。

这一篇，**我手把手带你把 Codex 从「零」用到「精通」**。

即使你还没装、不会用、想接国内 API、连 ChatGPT 账号都没有，都不要紧，我这里主打一步一步来。

好，咱们开始。

## 一. 安装 Codex

01

先把东西装上。

官方入口就一个，你打开：https://chatgpt.com/codex

Mac 和 Windows 都有，进去之后会看到一个大大的「**下载应用**」按钮，点它就行。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc2BMx3UrZ7y0UOxp1nsykdr0jKtAcgTFDyXH6OHxbtgrw6iaQFddtKMKnTFOJeyyWBpu9qxvaHV7icBNSTUicW5ekFos13w9B6O7Q/640?wx_fmt=jpeg&from=appmsg)

我这里用 Mac 来演示，整个过程跟你装别的软件没啥两样，下载下来一个安装包，拖进应用程序文件夹就完事了。

Windows 这边也很简单。除了官网那个按钮，你还可以在终端里直接敲一句命令装，更省事：

●●●

winget install Codex -s msstore

winget 是 Windows 官方的包管理器，你就把它理解成系统自带的一个「应用商店命令版」，敲一句话它自己去下载安装，不用你点来点去。

装好之后，打开它，咱们进下一步。

## 二. 登录、认界面、设成中文

02

第一次打开，它会让你登录。

直接用你的 ChatGPT / OpenAI 账号登就行，点「使用 ChatGPT 继续」，授权一下。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc1n66ER67son3N8Z9ZIEYM6B1ia049CpkgUwJcuHxpZOYnicqiab9E8GRQhibDvNHekLg8HGs6B0shGtsGWgrtnxIWozpY2TUXkNoQ/640?wx_fmt=jpeg&from=appmsg)

这里有个点我顺便说一下，Codex 能用多少，是跟你的 ChatGPT 会员档走的。免费用户也能下、能用，只是高级的那个 Codex 专用模型用不了；你要是轻度用，20 刀那档其实也够；像我自己平时用得重，开的是更高的档。**这个你按自己情况来，不用一上来就冲贵的**。

（**账号怎么办、想接国产模型怎么办，下一块我专门讲，先别急。**）

登录完，界面就出来了。我先带你把四大块认一下，认完你心里就不慌了。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc15zQdkhDWhtAyJu8X2Nxk0FgsUq7dm4fsQ5dsTWibjcM3SuF0ulvhEkhybHricDQt0Qia9T3XfeiaibeskGl8OyviaS8RJmosF7IfRc/640?wx_fmt=jpeg&from=appmsg)

中间这一大块，就是平时聊天的地方，跟你用别的 AI 对话框差不多，没啥稀奇。

左边那一栏，是用来管你所有东西的，它分两层，**一层叫「对话」，一层叫「项目」**。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc1fdHDfiaQ9FLP1EnlIIiad8y1b3h4Aw8cibeqFeZ5xMAgyzlrlfVa8suKGFKjN37xIJibOpm90xLicdKeBA3VMO970ib1Hgp61ZUDVw/640?wx_fmt=jpeg&from=appmsg)

「对话」就是那种零碎的小任务，让它帮你查个资料、做个规划、解释个东西，不用绑到具体某个文件夹里的，都丢这儿。

「项目」才是 Codex 真正干活的地方。

它的逻辑是这样：一个项目，对应你电脑本地的一个文件夹。你把这个文件夹交给 Codex，它就在这个文件夹里干活，生成的东西也都存进去。

**这就叫工作空间。**

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc3v15KKBicstib45PicbuibgmLwPAYCOYGb5vM729OeCibXNo2LpaZfVjBSYpsR5ibic6PoRVnIlSmRVJAZ7uJNYCkX7pGicFJHSVn1TWM/640?wx_fmt=jpeg&from=appmsg)

一个项目下面，可以开好几个对话（也叫 Thread，就是一条条独立的任务线），它们共用同一个文件夹里的文件，但**聊天记录各管各的、互不打架**。

我这里多嘴一句，**前期把分类想清楚，真的挺重要的**。

别图省事啥都堆一个对话里，记录一长，上下文一乱，它就开始犯迷糊。开始要是没分好，到后面真的会抓狂。。。

工作空间的管理很重要！所以同一个大方向放同一个项目，具体每件事开一条新对话，这是我认为最舒服的用法。

认完界面，咱们顺手把它设成中文。

打开左下角 Settings，找到 General，里面有个 Language，选中文。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc0aIVF8X2SrrzxmgOQ8llKXs2iaD70pYn52rXknJYDKP7d2hWNoC1swuArLvX40JT1jNGhAzZI0vPpYDg78Ik9868ZrSqXF5TWc/640?wx_fmt=jpeg&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc26gxtX9hZ4ptIgTYEgF7awLyxWicV1Z80Na26Qa2NXj8CJmwoib7XWRBFoUk2vY41cFYgkux5XTPwdibyDzs0lJMvBZApG9mE6Rc/640?wx_fmt=jpeg&from=appmsg)

选完它会下个中文包，你把 Codex 退出来重开一下，界面就是中文的了。

## 三. 没 ChatGPT 账号 / 想接国产 API，怎么办

03

好，这一块是我专门为没账号、不想折腾魔法、或者就想用国产模型的朋友留的。

我知道有不少人卡在这儿。东西是好东西，但一听要 ChatGPT 账号、要魔法，就劝退了。其实没那么夸张，我给你两条路，你挑一条能走通的就行。

而且后面这些操作，Mac 和 Windows 基本一样，我会统一讲，碰到不一样的地方我单独点一句。

第一条路：用 API key 登录

还记得登录页那个「使用其他方式登录」吗？里面有一个就是用 API key 登。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc0o5rdbd4ouS7ia48wH9JSVkEome3Vdp9IicoiccfUu5TCs1kfJulkOd2h0Q9Y2oXTIJ5HfxcHsic6DSSFEDV23UPBWLfibUuFsXF9Q/640?wx_fmt=jpeg&from=appmsg)

如果你手里有 OpenAI 平台的 key，走这条最直接。

但实话讲，OpenAI 的 key 对国内朋友来说，**门槛也不低，要绑卡、要充值。**所以更多人会走下面这条，直接接国产模型。

第二条路：用 CC-Switch 给 Codex 接国产模型

这条路，是我最推荐普通朋友走的。不用 ChatGPT 账号，接上 deepseek 或者智谱 GLM 这种国产模型，照样能把 Codex 跑起来。

我们要用到一个小工具，叫 CC-Switch，它干的事就一句话：**帮你在不同模型之间一键切换**。

去它的 GitHub releases 页面下载安装包就行，仓库是 farion1231/cc-switch。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc1HGsNbibm55SpPib5LmKVibBtz2dpg8OBDHsn8j2cW6yfeu1hxpBndJJjXjhvArACzkDjRYVZAQxetK8t2DbVVJhGd2G90DQe9MY/640?wx_fmt=jpeg&from=appmsg)

Windows 直接下那个 .msi，双击一路 next 装完。Mac 下对应的包，拖进应用程序就行。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc3regGRIubAiaNibJyN4mQgnNOJykPB9cfMJTb00D8pOJgZq1dKOxjzYZsLm6z9yibpQHdvyyOnASfibB53c7YaLLKguosjJicU7TYU/640?wx_fmt=jpeg&from=appmsg)

装好打开，你会看到顶上有好几个 Tab，Claude、Codex、Gemini 这些都在。它不是只能给 Codex 用，不过咱们今天就用 Codex 这一栏。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc15nLr02lTbxvAeqvK4aRSZwHFBTPCK9Obg7fznHj68EQkrKsfVcia7qG8OhOddypZhcJLM36rtHFcHNXYD8ndOnPSLXyqcDo2g/640?wx_fmt=jpeg&from=appmsg)

在 Codex 栏里，点右上角那个加号，新增一个模型配置。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc1TAFucGdDmRe6WbTHojugLY8XE0aVgicWeAE4KzOIHkb4WKJaNIfibM3vH2r7MIbVf91bmAjgGf2BF8Fv26EDibFnZKvBQFqbQiao/640?wx_fmt=jpeg&from=appmsg)

点完它会让你选供应商，列表里国内外的模型一大堆。咱们这儿选 deepseek（你要想用智谱的，就选 Zhipu GLM，操作一模一样）。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc3nU2WthojEmyS5RmAibHhSWW37eNKE8ukXSCrkgRNRiaW1iaxVTvqm17U4fDjQ8iaNCTRMBugULxp2pFw5aUWdjAzqEOAQ4AAbXoQ/640?wx_fmt=jpeg&from=appmsg)

接下来就是填东西了。这一步，是整篇里我最想给你掰开揉碎讲清楚的一步。

为啥？因为我自己第一次用 CC-Switch 给 Codex 接 deepseek 的时候，就在这儿栽过。我有个地方模型名填错了，结果死活报错，我还以为是 key 不对、是网络不对，翻来覆去查了十几分钟，最后才发现，是模型名那一格我手抖填错了一个字。。。

所以这一步，我把要填的两个字段一个一个给你标出来，你照着填，就不会栽我这个坑。

第一个，**API key**。这个去 deepseek 的开放平台上拿，注册登录之后，在 API keys 那里新建一个，复制下来，粘到这一格。你用的哪个厂商的就去哪里拿。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc2YyUaCO6oIpDFRtAEt29XxY0Sk5lzkCk4MYhoN4fdJ26jXK6Vd93FczwHQWx7FvrHxaEek4TBLlAJVUU5eyLKhWSXXTDMia9zY/640?wx_fmt=jpeg&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc2HxSaB9RYQPFkyUB9uKCvHDJttK6eicWrePuMPzicQ5Cfr2hnhARz8VJuuLYtmdIJxDp8JCt7E2GytLiarJibwBEpoM0icrhHZ1cfM/640?wx_fmt=jpeg&from=appmsg)

第二个，**模型名**。这一格就是我当初填错的地方，记得按 deepseek 平台文档里写的那个标准名字填，一个字母都别错。填完之后，剩下的它基本会帮你自动带出来，别瞎改。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc1t4yMTS5RRNjOpp6vrrPsiagvwIjXy0eAG8t8oZuic3lN4QicnJBPCGQUnYS19Yice4lBPQrd7MTWzcQVxKic2wWicJwgBvp8YArEwY/640?wx_fmt=jpeg&from=appmsg)

两格都填好，点右下角的「**添加**」。

加完它就自动切到你刚配的这个模型上了，主界面能看到它处于高亮状态。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc0c8w8OeOgSEEBx8Y9fP4o0kzJA0ZWJ1ScWeeiaIt2d937biaDxzCbGU8pptQsCPOYgV7s9XMaDYI7M4XEskWHnaxQgX4EIJ54hE/640?wx_fmt=jpeg&from=appmsg)

这时候回到 Codex，你会发现它自动登录上了，能用了。而且左下角有显示。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc1OhjDicMTC4ia7vxWUgq5ib4E5xbp0sQJI32ARBuGnaeVsk4NyMUD3ggHK3PTCwuTh92rmzWQeCZFSIpKzzicYib5U5EHmJFYrYNWM/640?wx_fmt=jpeg&from=appmsg)

说真的，CC-Switch 这工具我用下来挺顺手的，最大的好处就是切模型快，你今天想用 deepseek，明天想用 GLM，点两下就换过去了，不用每次去改一堆配置。对咱们这种不想折腾的人，是真省心。

顺手再提一个：Codex++，没账号也能玩 skills

还有个Github 上的东西叫 Codex++（CodexPlusPlus），它能帮你把 skills 这类玩法解锁出来，就算你没有 ChatGPT 账号，也能跑。

skills 这个概念后面我会讲，你这儿先有个印象：如果你走的是接国产模型这条路，又想玩 skills，那就留意一下 Codex++。具体安装它仓库里写得很清楚，你跟着 readme 走就行，这里我不展开。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc0RRaNlS6Do9kQqChbT4lchVQYUUVlhZV7FrNq1u9KCliarPx7V57LyBRiadEia4icBTOmiaVnE5tvJnMUjJyxMLvoNXDLsj5BNk3ib8/640?wx_fmt=jpeg&from=appmsg)

好，账号和接模型这块就齐了。不管你是直接用 ChatGPT 账号，还是接了国产模型，往下走。

## 四. 核心玩法

04

这一块咱们慢慢过。我把日常你真正会用到的功能，一个一个给你说清楚。

先说回项目和对话那套逻辑（前面提过，这儿再落实一下怎么建）。

你想正经干活，就在左侧「项目」这边点加号，新建一个空白项目，或者直接用一个你电脑上已有的文件夹。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc047azmzDZX3DNzmrXbWUWY2iciaOhIrOn6Ue3y00uwtmuCkhOPKVV3FgIFzrzx9FmDDI8wlIJCtrJyEUTcs1Mar4NmAYGwOJB9M/640?wx_fmt=jpeg&from=appmsg)

进到项目里，对话框就会跟刚才不一样了，下面多出来一些东西，咱们挨个看。

4.1 对话框左下角，是三档权限

- **默认权限**：最保守，它干啥都得先问你一句、等你点同意。
- **自动审查**：适合日常，平时让它自己跑，碰到有风险的操作（比如删一堆文件、动敏感目录）才停下来拦你一下。
- **完全访问**：全放开，它自己跑，不再每步征求你。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc3EYbBaaHLmmYQtxXdRlIrKe8icg8KR1rcLcbRiaKJk4Q6kzrNyGLtCP8LckGhBaNLQanVMB0CIicHhicgoQziaMZNcpW7mmBicCOMiaM/640?wx_fmt=jpeg&from=appmsg)

我自己平时用的是完全访问。

倒不是不怕风险，是因为它每弹一个东西出来问我，我看了其实也判断不了啥，那不如让它自己搞、我盯着结果。

但我得诚实跟你说，你要是刚上手、心里没底，我建议你先用「自动审查」，它会在真正危险的地方拦你，比一上来全放开稳妥。这个档你随时能改，不用纠结。

4.2 对话框右下角，是切模型和推理档

模型这块，你接了哪个就用哪个，用官方账号的话无脑选当前最强那个 GPT-5.x 就行。

旁边是推理档，从低到超高（Low 到 Extra High）。这个你可以理解成它「想多深」，档越高，它回答前琢磨得越久，通常更稳更全，但也更慢、更费额度。

我的建议是，日常用「高」就够了，别一上来就拉满。真碰到难活大活，再开「超高」。说实话，超高那档我平时很少动，不是它不好，是大部分需求真用不上，拉满纯属浪费。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc2bVaLzlpibAT8tPGR91FoicNjJibUPqoVJhK05iaibmI56Gic6e5OB7B9msPFSecM18TSIcu82nZkKBibkBOsIk8JPRhekXgiaNdeOLTc/640?wx_fmt=jpeg&from=appmsg)

旁边还有个速度，标准和快速两个。**快速更快但更烧额度，标准其实跟快速差不太多。**

除非你额度多到花不完，不然我还是推荐标准。

PS：虽然大刘我是全部拉满！！！

4.3 它还能选在哪儿改你的文件：直接改、隔离副本、云端

新建对话的时候，除了上面那档权限，你还能挑它在「哪儿」干活。这事小白特别该知道，因为它直接决定「会不会动到我原来的东西」。

- **直接改（Local）**：就在你这个项目文件夹里改，改完就是改完了，最直接。
- **隔离副本（Worktree）**：它另开一份副本去改，碰都不碰你的原文件，你看着满意了再合并回来。怕它改乱的，走这个最稳。
- **云端（Cloud）**：把活儿丢到云端后台跑，你电脑该干嘛干嘛，跑完回来收结果。
我的建议是，刚上手又怕出岔子，就用隔离副本；等你摸熟了、信得过它了，日常直接改也行。

4.4 怎么把文件、图片喂给它，怎么用嘴说

光在对话框里打字描述，它有时候搞不清你指的是哪个。几个更省事的法子，你都该会。

先说怎么让它看准你说的是哪个文件。在对话框里打一个 @，会弹出一个菜单，你搜一下文件名，把那个文件直接插进消息里，它就知道你说的是它了，比你用嘴描述「就那个谁谁谁文件」靠谱多了。

**提醒一句，@ 这儿只能选到具体文件，选不了整个文件夹**。

再说图。手里有张报错截图、一张设计图、一个表格的图，不用费劲描述，直接拖进对话框、或者复制粘贴进去，它就能看图说话。

不爱打字的，还能用嘴说。按住 Ctrl+M 开始说话，它把你说的转成文字，转完你还能改两个字再发。打字慢的朋友，这个真香。

4.5 想让它少跑偏，需求得这么提

很多人觉得 AI 不好使，其实是话没说清。官方自己给过一个特别实用的提需求套路，你照着套，立马就管用。一句需求里，尽量把这三样带上：

- **给材料**：把它要看的文件、文档、报错截图给它，别让它猜。
- **立规矩**：比如「用中文」「别动数据库」「照我现有的风格来」。
- **定验收**：把「做成什么样才算成」说清楚，比如「能正常打开、不报错」「这三项都对得上」。
说白了就一句话，给材料、立规矩、定验收。这三样补全了，它跑偏的概率能降一大半。

**真碰上难活大活，记得顺手把推理档调到「高」**。

4.6 计划模式（Plan mode）：只规划、不动手

点对话框左边那个加号，能打开「计划模式」。

它的意思是，你把需求告诉它，它先不急着动手，而是先帮你把方案、步骤理清楚，你确认没问题了，它再开干。打开之后，对话框边上会出现一个小图标，告诉你现在在计划模式下。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc2H4GPYYFHosm4gGic0YjiacIibMrXIj8jkbzIBiacRQoCtoDuhjsVcWtpAx8LQJXMAZFZcz9Pic9rOFzCjpsM6ED4Uz6azw3Q39WuI/640?wx_fmt=jpeg&from=appmsg)

凡是稍微复杂点的事，我都推荐你先走一遍计划模式。它会先问你几个问题，你点选回答，它给你一份完整方案，你点确认，它才正式开工。这一步看着多此一举，其实能帮你少返工很多。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc3sHQHQenfApH9xtvmRBR2KGNyXAFoebliakcic5CeKe3knEpTEI2lzgs2xaro6eHEicz0cz2FwDA59GE0teLXcOuCXfRDgU4kXZ0/640?wx_fmt=jpeg&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc2ZJt3wia2OsugMHWYZnddANlX6tCsP7GHolRaFl2Aliajkn1icC7zUsyNWpQCCBUZFPHNTXmaT7ye3mBlFmTbYpzVOVSXNrafsr0/640?wx_fmt=jpeg&from=appmsg)

4.7 目标模式（Goal）：派个长活，让它自己盯着干

这是最近才出的**新模式，很火**。

跟计划模式并排，还有个「目标模式」。计划模式是「**先把方案理清楚再动手**」，目标模式是另一个路子：你给它定一个稍微长一点的目标，它会一轮一轮自己往前推，不用你发一条、等一条、再催一条。中途你还能随时暂停、接着跑，或者干脆把这个目标撤掉。

适合那种「一时半会儿干不完、又不用你时刻盯着」的活。设完你就能去忙别的，它自己慢慢推进。

4.8 它改完了，怎么一条条验收（Review 审阅面板）

这功能我得专门拎出来讲，因为它治的是小白心里最大那块石头：它把我文件改了，我要是不满意咋办，收得回来吗？

它干完活，桌面端有个 **Review（审阅）**面板，能把这一次动过的地方一处处列给你看。你可以这么收：

- 一处处过，这处改得好就留下，那处不对就单独撤掉，不用整篇推翻。
- 觉得整个方向都不对，一键全撤，回到它动手之前的样子。
- 哪行还想再调，把鼠标挪到那行点个加号，直接写一句「这儿改成怎样」，它就照你这条意见接着改。
有了它，你就不怕「改坏了收不回来」。这也是我建议小白早点用熟的一个功能，它是你从「不敢让它碰我文件」到「放心交给它」的那道坎。

4.9 内置预览浏览器 + 批注：这个我必须重点说一下

如果你让它做的是网页这类能看的东西，做完它会让你用 Codex 自带的浏览器打开看效果。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc3ouq1jv4TWuhG2MWRIwh6WxCIVcMUw65VYDVUAaIzEc80aYiaibfuzmmUF2sgC0JjurOLhBIe1sHbTqG4docoRr0KWA2xojjKHc/640?wx_fmt=jpeg&from=appmsg)

打开后，右上角有几个按钮，一个是截图，一个是批注。批注是我用得最多的功能之一，真的很香。

点开批注，你可以直接在页面上圈选任何一个元素，写上你想怎么改。比如我想换个 logo，直接在页面上把它选中，打字说一句「换成官方 logo」就行，不用再截图、再用嘴跟它描述半天。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc15E10VOicDlEElUfemdgrRG1e9lz8HyQ04h51QSktFgJMUticXHo5n1HNofAH72AkRZGQZRk4JC4T2dYolW039sRpxau1Zl5LE0/640?wx_fmt=jpeg&from=appmsg)

而且最近还加了个新功能，像字体、字号、颜色这些，选中之后能直接在面板里调，改完实时就能看到效果。

批注完，点发送，它就照着你的意见改去了。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc3kkcKylXsbOhwuYWqWvXpDBGFRR2k1KTxSqicZdGyg8ibYNicicnzJ5WjEOWupKKoSSFkPk8Jn3zoRbicCSO4OJS3CpRoB3tr1Syo0/640?wx_fmt=jpeg&from=appmsg)

4.10 skills 与插件：可视化界面，这是 Codex 对小白最友好的地方之一

skills，你就理解成给 Agent 用的「**技能包**」，插件是把一组技能、工具打包成的更成熟的安装包。

Codex 最舒服的一点是，这些它都做成了可视化界面，不像有些工具你装了啥、装哪了、有啥用，自己都搞不清。

从左边的「插件」进去，顶上能切「插件」和「技能」两个 Tab。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc0Pfqiap7XU09g2HTBxfJ7AGWmtSiaPibUx0Vyia1vllNA4L1md6OUmggbicqeY0XDZY717e8dKdM8sxicIzvad1EAicHdiaaCPO9zjpnE/640?wx_fmt=jpeg&from=appmsg)

已经内置了很多常用的插件。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc0nia1KmHeuZwbicFZgyRibpicJxHZ1r8CywKdMib4Mu9fRymicnTMkdkh5bGiaj0BSECXzN3hABFhz4IOI8ozI15w0OPZm0gRQCV4hMI/640?wx_fmt=jpeg&from=appmsg)

还有很多内置的技能，直接就能用。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc199UXmxaCUYBiaa89ialBJgFx7CpU2OYtsSKezx1QO1ATJKcC2cqgicFXlEXSZyQxmVC3Lex9gKeb9WFolnYOiaoYsrbia8LOgp7x4/640?wx_fmt=jpeg&from=appmsg)

要用某个 skill，在对话框里输入 `/` 或者 `$`，它就会弹出来让你挑。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc0lZniaAyXp43tYdpz7KGyJ3PzjibRqGBf3RbJnfdd8NBvQ958HNrzq5bZrJ2jzEyjZDYelrQzj8W78ToeWHp3JoQKNzoj2aH9u8/640?wx_fmt=jpeg&from=appmsg)

想装别人写的第三方 skill，更简单。把那个 skill 的链接直接甩给 Codex，让它帮你装就行。

4.11 个性化：全局 AGENTS.md 和项目 AGENTS.md

进设置里的「个性化」，里面有个「自定义指令」，这个其实就是全局的 AGENTS.md。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc2u0XkVe7vqa4iaxEwibqNDem9XCVmVRbnhV8tDiaNT2BJadOd2FJRB808cm3KhmEhjibzrhfodBF2xWcJCp0n8nP3mdCIDdVRxbf8/640?wx_fmt=jpeg&from=appmsg)

AGENTS.md 你就理解成给 Codex 立的家规。全局这一份，是你给它定的通用规矩，比如「默认说中文」「结论先讲、别铺垫」「删文件这种危险动作必须先问我」，定好之后，不管你以后开多少个新对话，它都记得。

而项目级的 AGENTS.md，是针对某个具体项目的特殊约定，这个你不用自己写，直接打开那个项目，跟 Codex 说一句「帮我写一份这个项目的 AGENTS.md」，把你在意的事跟它聊清楚，让它自己写就行。

4.12 记忆功能

同样在个性化里，有记忆相关的开关，我推荐打开。打开之后，它会在你聊完或者闲置一阵后，自动把之前的对话总结成记忆存下来，以后碰到相关的事会自己调出来用。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc21g9ibWackicibiabNyJGT6YiaXU6YTBCM7SibCydL3t2XCDE2ALzy2xOIwTE4j42AVdOmOlMjias2s5FWCqGeTq3HUVqZpm20GUz1a8/640?wx_fmt=jpeg&from=appmsg)

4.13 怎么看还剩多少额度

用着用着你会想知道自己还剩多少额度。两个办法：一个是点左下角设置，里面有「剩余额度」；另一个更快，直接在对话框输入 `/`，调出「状态」（status）。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc2SVIxkFbYUgE3Nic8hmrAiaZQM042WJtiaQiaHv2jRXLZeiacxRB4IgFcXIJBt8GWdibSLJZNbZbxa5BqiaPkm820s0C0J3l44AuJnuw/640?wx_fmt=jpeg&from=appmsg)

它会告诉你 5 小时内还剩多少、这周还剩多少、啥时候刷新，挺直观的。

核心玩法到这儿就差不多了，这些用熟，日常需求基本都能搞定。

## 五. 往「精通」摸一摸

05

下面这些，是 Codex 比较进阶、也比较炸的能力。我先把丑话说前头：**这一块里的功能，目前基本都是 Mac 专属，Windows 暂时还不支持。** Windows 的朋友可以先了解一下，等后面官方跟上。

5.1 Computer Use：让它直接操控你的电脑

这是 Codex 上最强的能力之一。它能用「看屏幕 + 动鼠标键盘」的方式，真的去操作你的电脑，比如帮你去某个网站搜东西、下载、安装。全世界能做到这种可视化操控电脑的，真没几家，Codex 做得算很好了。

要用，先去设置里把「电脑操控」的开关打开。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc0g8XKwyZh7AouhpkbF8KQL29aMalicqOUD1BeSn7cAvcdA2ezl6gANHsCNpHZias7HpKJLzhN2fMuEibodDVP5rn79RIHZqtCDUw/640?wx_fmt=jpeg&from=appmsg)

用的时候，在对话框里 `@` 点名 Computer Use，告诉它你要干啥就行。它操作的时候，屏幕上方还会有个小提示条，让你知道它正在接管。

![](https://mmbiz.qpic.cn/mmbiz_jpg/J1Cdba5GUc3OHxOJniaHeMNee3ZW8Dc0r7Rt8Z1Ekp2DlCoyLIaicefxjauia2o8KYljQ40r0dFJ02oUbTLiaVrmzQDUJHVvEKZCe8ZkDbW8vMo/640?wx_fmt=jpeg&from=appmsg)

碰到要输密码、登账号这种涉及安全的步骤，它会停下来让你自己来，这点做得挺稳。

5.2 定时任务自动化：让它按点自己干活

你可以给它设定时任务，让它在固定时间自动去做某件事。比如挂个每天早上九点自动巡检的活，它到点自己跑、跑完把结果发给你，完全托管。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/J1Cdba5GUc1ibmVQKOZDuAhQq3SAqwPXsHHsdOZethWVCibpaJWHtYrMw8K9FrW4OAiccnUQyV4E2ZqibsoukWZw47VicKLuHrWUZ8UroVsShDgo/640?wx_fmt=jpeg&from=appmsg)

这些进阶功能再强调一遍：现在都是 Mac 专属，Windows 暂时没有。Windows 的朋友别白找了，先把前面四块用熟，这些等官方补上再说。

## 六. 写在最后

06

好了，从装上、登录、设中文，到没账号怎么接国产模型，再到核心玩法和进阶能力，这一篇就给你全串完了。

其实你会发现，Codex 真没那么唬人，难的地方就那么两三处，把它绕过去，剩下的你自己上手试一试，**很快就熟了**。

剩下的，你自己去折腾就行。

希望对你有点用，玩得开心。

**AI 真上瘾！**

以上，既然看到这里了，
如果觉得不错，随手点个赞、在看、转发三连吧，
如果想第一时间收到推送，也可以给我个星标⭐～
谢谢你看我的文章

**你的关注是我持续更新的动力～**

**我是谁**

我是 AI大刘，北大毕业，大模型研究方向，腾讯犀牛鸟，先后在腾讯、百度的大模型研发部门。现在斜杠青年：给多家国企做AI顾问 \ OPC \ 研究员 \ 产品独立开发者 \ Vibe Coder
