---
title: "把CAD交给Agent，全新的CAD快速看图Skill来了"
author: "NewbimAI"
publish_date: "2026-10-23 23:23:59"
saved_date: "2026-10-28"
source: "wechat"
url: "https://mp.weixin.qq.com/s/1pnQ7IO4sxQGtB5BhELrPw"
---
# 把CAD交给Agent，全新的CAD快速看图Skill来了
图纸是很多行业信息密度非常高的文件，却偏偏是大模型吃不进去的格式 。

AI 什么都能读 ：PDF、Word、网页、截图，丢进去就能聊。

但你把一张 DWG 丢给它， 它打不开 。DWG是二进制格式，目前大模型没有办法直接解析。

我也试过一些 CAD 方向的 Skill，没有图形预览界面，体验一言难尽：有的只是把图纸转成一堆原始文本丢给你，看图还是得靠自己。

于是我决定自己做一个CADViewer-Skill，现在它来了！

![](https://mmbiz.qpic.cn/sz_mmbiz_png/XlOLDQTcQVVTWamibakibBu9dyvdlLCDpNOyToibiaicEpkbQZjG8OiaUsCLAC04k8312fcxUKG3WvGTFKhkjytInFhd3bQFNBeHTUsQ0wf66gFlU/640?wx_fmt=png&from=appmsg)

— WorkBuddy中CADViewer使用界面

01

DELIVERABLES

### 成果是什么？直接放链接

TOOL 1CADViewer桌面端

免安装便携版： https://github.com/NewbimAI/NewbimAI-CADViewer/releases

如果想本地使用，直接下载桌面端，使用简单

TOOL 2CADViewer Skill

Skill 轻量包：

https://github.com/NewbimAI/NewbimAI-CADViewer

注册进Workbuddy、OpenCode等都智能体，一条命令的事

装完之后，你对 AI 说“帮我解析这张图纸”， 它就会自动启动解析服务，统计图纸信息，把图纸数据报给你 。还可以直接在智能体中轻量化查看图纸，支持格式转换，可导出JSON、PNG、DXF、PDF。

以下能力在桌面端和Skill里通用，已开源。

02

FEATURES

### 有哪些能力？

拖动到视图 + 打开按钮

打开 DWG/DXF、滚轮缩放、拖拽平移，非常丝滑

![](https://mmbiz.qpic.cn/mmbiz_gif/XlOLDQTcQVVMiaBEqnFHR766pzwxZp11mHZZb0Ckd5cjcO3sQYEUmqaILjiaJAZCAvb4mSZ6BIwLhNdhlXVZ17W2gLSoWtxyN0b07E2BfZQXM/640?wx_fmt=gif&from=appmsg)

滚轮缩放、拖拽平移，上万图元的图纸也能跟手操作

图层显隐 + 聚焦灰显

双击图层或图块那一行，该层保留原色、其余灰显；单击还原。

![](https://mmbiz.qpic.cn/mmbiz_gif/XlOLDQTcQVWODJ4bQ9fVcUgNxQnXzTTUlVox7LLKCNjpRnxnxBwztrYPCnodkOFlcZGcIibGQXpNmmmAz9dQPWGUJDLISKz1icSIzMpqsMPMo/640?wx_fmt=gif&from=appmsg)

图层显隐开关：想看哪层点哪层

![](https://mmbiz.qpic.cn/mmbiz_png/XlOLDQTcQVVld9XCvq0GbPgRIn0JeBIOXuTTJNiacNcIcp1bDx4zTlXRD458LS7ZGFJERuwhXmgYpRoWPNWDQyLxVIJdeiaC9pY3jCs7EMt8A/640?wx_fmt=png&from=appmsg)

双击图层：当前图层保留颜色，其他图层内容灰显

![](https://mmbiz.qpic.cn/mmbiz_gif/XlOLDQTcQVUHkBeE1CxXmo9o3h8tCQmianaluwVxTkRTOt5J9fz5VHamTL0Qu6MZiapaQ4GB576LvczOwpHulyZ03kfkH6qqBwzwYic3IZMPJE/640?wx_fmt=gif&from=appmsg)

聚焦动态效果：双击保留原色、其余灰显，单击即还原

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/XlOLDQTcQVXJs0Cf48oviaicibNcjk7EXlafTXyBUlpnGYZa88iaMFQUTN8ZiaYm8ZT42dicicGyADZboslfDt0N3rdAoHpfav0ibISLc1GZ4HSFarg/640?wx_fmt=gif&from=appmsg)

图层搜索：按名字搜索定位

图块统计

常规块和动态块均能准备识别，解决匿名块识别和统计不准的问题

![](https://mmbiz.qpic.cn/sz_mmbiz_png/XlOLDQTcQVWmPXMicqIKjB6z5nuPeEM4vIKSCm2vTzwksqvj1Cp0DO9m8Pvg4mxial078IoHINRBWO01afpURjM1GkXYbEYicO5FXc3uIngn0k/640?wx_fmt=png&from=appmsg)

图块面板按引用次数降序排列，块名、引用数、实体数一目了然

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/XlOLDQTcQVWm5zeCia6licpKksIg3yEF1TYtHyftyj136l1xxeibaYp38PYhias3hesTbOb7m3EBKH4RktrKHEicWcX5jFp1ekicjvScG7tla41Ao/640?wx_fmt=gif&from=appmsg)

双击图块行，该块的全部实例保留原色、其余灰显

导出全家桶

支持导出：PNG（白底、2 倍清晰度）、统计 JSON、原始 DXF、矢量 PDF（A3 单页，文字转轮廓不炸字体）。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/XlOLDQTcQVXSEBWPIeO3ST6dsH1xtp5mOOGiae60OXPdS2xAZPrWxHnLOIlgCf5JCZktfxyduDNMib79l7MPjlZw70srJnEou7tsf8MA77wgk/640?wx_fmt=gif&from=appmsg)

导出菜单展开动画：四种格式一目了然

∞

THE END

### 写在最后

目前仅支持Windows，其他系统暂不支持。如果是天正图纸，需要先转T3，这个版本暂不支持天正对象的识别。目前桌面端基本可实现CAD快速看图同等的浏览效果。

如果需要其他功能或建议，欢迎评论区交流。直接需要安装包，也可以后台滴滴！

我是NewbimAI，专注于分享普通人能懂能用的AI！

如果你觉得今天这篇有收获，欢迎 点赞、在看、转发 ，我们下篇见！

- END -
