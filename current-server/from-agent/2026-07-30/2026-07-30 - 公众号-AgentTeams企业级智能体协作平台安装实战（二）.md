---
title: "AgentTeams企业级智能体协作平台安装实战（二）"
author: "AI易用君"
publish_date: "2026-07-22 22:35:51"
saved_date: "2026-07-30"
source: "wechat"
url: "https://mp.weixin.qq.com/s/7RrXQitPXZX57dFyvE39uQ"
---
# AgentTeams企业级智能体协作平台安装实战（二）
# 五、第三天：最终调试和收尾

## 5.1 再次重装

第三天，我发现在使用AgentTeams登录后，不能配置模型，不能正常使用所有功能，让助手修复来修复去，折腾了不少时间，但一直无法完全正常使用，我决定做最后一次彻底的重装，确保一切都是干净的，彻底解决使用时报错的问题。本文较长，偏重于运维，如果你不感兴趣，可以下滑到最底看看我的建议即可。

这次是我自己在终端里执行安装脚本，让AI远程辅助检查和调试。这种"用户操作 + AI 辅助"的模式比之前"AI 全程操作"更可靠——我能直接看到终端输出，遇到交互式提示可以自己做决定。

先清理了现有安装环境后，我按照官方给的文档，一步一步操作，一开始还是不行，每次安装完成后，在完成最后阶段，都报如下错误：

“容器之间无法正常通讯。”

AgentTeams 的架构是多容器协作——Controller、Manager、Tuwunel（Matrix）、Element Web 等，它们需要通过 Docker bridge 网络互相访问。但部署后发现：

Manager 启动后几秒就退出，日志显示连接 MinIO 超时

Controller 和 Manager 虽然用 --network container: 共享了网络命名空间，但某些内部服务仍然访问不通

用 curl 在宿主机上访问容器端口没问题，但容器之间互相 curl 就超时

---

## 第一次排查：Shell 环境变量

最直觉的怀疑是 Shell 环境变量里有代理设置。

-

```
$ env | grep -i proxy
```

输出为空。Shell 层没有代理。

-

```
$ cat /etc/environment
```

（无代理相关配置）

排除。

---

## 第二次排查：Docker daemon 代理

Docker daemon 有自己的代理配置，通过 systemd drop-in 文件设置：

-
-
-
-
-
-

```
$ cat /etc/systemd/system/docker.service.d/proxy.conf[Service]Environment="HTTP_PROXY=http://192.168.100.223:1081"Environment="HTTPS_PROXY=http://192.168.100.223:1081"Environment="NO_PROXY=localhost,127.0.0.1,192.168.0.0/16"nbsp;cat /etc/systemd/system/docker.service.d/proxy.conf[Service]Environment="HTTP_PROXY=http://192.168.100.223:1081"Environment="HTTPS_PROXY=http://192.168.100.223:1081"Environment="NO_PROXY=localhost,127.0.0.1,192.168.0.0/16"
```

这个配置影响的是 docker pull（拉镜像时的网络流量），不影响容器内部的网络通讯。容器运行时的流量走的是 Docker bridge 网络，不经过 daemon 代理。

排除 daemon 层是根因。

---

## 第三次排查：容器内环境变量（发现异常！）

随机挑一个刚创建的容器，看看它内部的环境变量：

-
-
-
-

```
$ docker exec casdoor env | grep -i proxyHTTP_PROXY=http://192.168.100.223:1081HTTPS_PROXY=http://192.168.100.223:1081NO_PROXY=localhost,127.0.0.1
```

奇怪了——这个容器创建时没有传 -e HTTP_PROXY 参数，为什么会有代理环境变量？

再检查几个容器：

-
-
-
-
-
-
-
-

```
$ docker exec dify-api env | grep -i proxyHTTP_PROXY=http://192.168.100.223:1081HTTPS_PROXY=http://192.168.100.223:1081NO_PROXY=localhost,127.0.0.1$ docker exec openproject env | grep -i proxyHTTP_PROXY=http://192.168.100.223:1081HTTPS_PROXY=http://192.168.100.223:1081NO_PROXY=localhost,127.0.0.1
```

所有新创建的容器都有代理环境变量，而且 NO_PROXY 只有 localhost,127.0.0.1，没有 Docker bridge 子网（172.16.0.0/12、10.0.0.0/8）。

这就意味着：容器间通过 Docker bridge 网络（172.16.x.x、10.x.x.x）的流量，会被路由到 192.168.100.223:1081 这个代理。而代理无法访问 Docker 内部网络，所以通讯失败。

---

## 根因：Docker CLI 客户端代理注入

问题出在一个大多数人不知道的地方——~/.docker/config.json。

-
-
-
-
-
-
-
-

```
$ cat ~/.docker/config.json | jq .proxies{"default": {"httpProxy": "http://192.168.100.223:1081","httpsProxy": "http://192.168.100.223:1081","noProxy": "localhost,127.0.0.1"  }}nbsp;cat ~/.docker/config.json | jq .proxies{"default": {"httpProxy": "http://192.168.100.223:1081","httpsProxy": "http://192.168.100.223:1081","noProxy": "localhost,127.0.0.1"  }}
```

Docker CLI 客户端会读取~/.docker/config.json中的proxies.default配置，并将其静默注入到所有新创建的容器中——作为环境变量 HTTP_PROXY、HTTPS_PROXY、NO_PROXY 等。

这个行为和 daemon 代理、Shell 环境变量完全独立，是第四层代理注入。很多人（包括我）都不知道有这层。

为什么会有这个配置？

这个配置可能是之前配置 Docker 代理拉镜像时，误操作写入的。Docker 的代理配置有四个层级，各管各的：

层级

配置位置

影响范围

1️⃣ Docker daemon

systemd drop-in `proxy.conf`

daemon 拉镜像时

2️⃣ **Docker CLI 客户端**

**~/.docker/config.json proxies.default****所有新创建的容器（根因）**3️⃣ Shell 环境

bashrc/profile 的 `HTTP_PROXY`

当前shell 的 `docker run`

4️⃣ Compose

`.env /docker-compose.yaml`对应 compose 项目

daemon 层的代理只影响 docker pull/docker push。但 CLI 层的代理影响所有新创建的容器——它会在 docker run 时自动把代理注入容器环境变量。

---

## 修复过程

## 步骤 1：备份并清除 config.json 中的代理配置

# 备份

-
-

```
cp ~/.docker/config.json ~/.docker/config.json.bak
```

# 编辑，删除 proxies 段

-

```
vi ~/.docker/config.json
```

删除 "proxies" 整个对象：

-
-
-
-
-
-
-
-
-
-
-
-
-

```
 {    "auths": {      "higress-registry.cn-hangzhou.cr.aliyuncs.com": { ... }-   },-   "proxies": {-     "default": {-       "httpProxy": "http://192.168.100.223:1081",-       "httpsProxy": "http://192.168.100.223:1081",-       "noProxy": "localhost,127.0.0.1"-     }-   }+   }  }
```

## 步骤 2：重建受影响的容器

⚠️ 关键：docker restart 不会重新读取 config.json！

Docker 只在容器创建时（docker run）读取 config.json 注入代理。docker restart 只是重启容器进程，不会重新注入环境变量。所以已有的容器仍然有代理环境变量。

必须重建（删除 + 重新创建）：

# 对于有 restart policy 的容器，先禁用

-

```
docker update --restart=no <container>
```

# 删除容器

-

```
docker rm -f <container>
```

# 重新创建（不带 -e HTTP_PROXY 等参数）

-

```
docker run -d --name <container> ...
```

## 步骤 3：逐一验证

# 检查新容器内是否有代理环境变量

-

```
docker exec <container> env | grep -i proxy
```

# 应该无输出

---

## 深层问题：NO_PROXY 格式不兼容

在排查过程中还发现一个问题——即使配置了 no_proxy，格式不对也不管用。

daemon 代理配置中用了 CIDR 格式：

-

```
NO_PROXY=localhost,127.0.0.1,192.168.0.0/16
```

但 config.json 中注入到容器的是：

-

```
NO_PROXY=localhost,127.0.0.1
```

即使我手动在 config.json 里加上 192.168.* 通配符格式，Python 的 httpx 库不认这个格式：

# httpx 内部的 proxy 排除逻辑

# ❌ 不支持

"192.168.*"

# ✅ 支持

"192.168.0.0/16"

Python httpx 要求 CIDR 格式（192.168.0.0/16），不接受通配符。这会导致 Python 应用（如 Dify API）在访问 192.168.100.x 内网服务时，流量仍然走代理。

---

## 排查清单（4 层代理排查顺序）

遇到 Docker 容器间通讯问题时，按这个顺序排查：

1️⃣ Docker daemon 代理

-

```
cat /etc/systemd/system/docker.service.d/proxy.conf
```

影响：docker pull/docker push。不影响运行中的容器通讯。

2️⃣ Docker CLI 客户端代理（最容易遗漏！）

-

```
cat ~/.docker/config.json | jq .proxies
```

影响：所有新创建的容器。这是最容易被忽略的一层。

3️⃣ Shell 环境变量

-

```
env | grep -i proxy
```

影响：当前 shell 中执行的 docker run。

4️⃣ Compose 项目配置

-

```
cat <project>/.env | grep -i proxy
```

影响：对应 compose 项目。

---

## 经验教训

1. Docker 代理有 4 层，不是 2 层

大多数人只知道 daemon 层和 Shell 层。CLI 客户端层（~/.docker/config.json）是第三种，而且是最隐蔽的——它不影响 daemon 拉镜像，不影响 Shell 命令，但会静默污染所有新创建的容器。

2. docker restart 不会重新读取 config.json

这是最大的坑。你以为改了 config.json，重启容器就生效了？不会。Docker 只在 docker run（创建）时读取一次。要生效，必须删除重建。

3. no_proxy 格式很重要

不同语言、不同库对 no_proxy 的解析规则不同。最安全的写法是 CIDR 格式：

NO_PROXY=localhost,127.0.0.1,192.168.0.0/16,172.16.0.0/12,10.0.0.0/8

覆盖所有常见的内网子网。

4. 容器间通讯问题第一时间检查代理

如果宿主机能访问容器，但容器之间互相访问不了——大概率是代理问题。直接进容器看环境变量：

-

```
docker exec <container> env | grep -i proxy
```

5. 配置代理时要分清"给谁用"

给 docker pull 用 → 配 daemon 层

给容器内应用用 → 手动在 docker run 时用 -e 传入

不要在 config.json 里配 proxies.default

——除非你真的想让所有容器都走代理

---

## 写在最后

这个故障排查花了大半天。根因就是 ~/.docker/config.json 里一个不起眼的 proxies 段，导致 11 个容器全部被注入了错误的代理配置。

Docker 的代理设计确实有点反直觉——四层配置，各管各的，互相不覆盖。CLI 客户端层尤其隐蔽，因为它不报错、不警告，就默默把代理塞进容器。

如果你遇到容器间通讯异常，记住第一件事：进容器看环境变量里有没有代理。

---

经过艰难的处理，安装脚本再次执行成功，所有容器正常启动。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/D2xbkDicZsVG8U1yhGrqnHjJGm9kUZO2eoh5b3iaPpooVX0bzkytuU62zcKJXOkfo089lAuP7mwuhSVyMd6kYEALtbYQQMsHj05neoACAy1kk/640?wx_fmt=png&from=appmsg)

登录就可以看到界面了：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/D2xbkDicZsVHhTM7SnqhWKNQP7oU3TYKSwxD2STBpe2jGpwVLoSl8mQdIpHL4YlDtGlHxT6wdDiconTIchw2Y7OXbYeG9aAdNFkcKoEE1OGyY/640?wx_fmt=png&from=appmsg)

## 5.2 最终验证

逐一检查了所有 12 个服务的可达性：

-
-
-
-
-
-

```
服务            端口   状态Higress Gateway 8080 ✅ 正常Higress Console 18001 ✅ 正常CoPaw Manager 18888 ✅ 正常Element Web 18088 ✅ 正常Tuwunel (Matrix) 内部 6167 ✅ 正常
```

## 5.3 剩余的技术问题

完全跑通后，Element Web 的浏览器控制台还有一些告警，不影响核心使用但值得一提：

1. Homeserver 地址配置问题

Element Web 的配置文件里，base_url 被写成了 http://127.0.0.1:8080。当用户通过局域网 IP 访问时，浏览器会尝试连接自己本机的 8080 端口，自然连不上。

根因是：Element Web 会根据访问的域名/IP 查找对应的配置文件（比如 config.192.168.100.237.json），找不到就回退到默认配置，而默认配置里的地址是 127.0.0.1。

2. HTTP 环境下的功能限制

因为我们用的是 HTTP（没有 HTTPS），浏览器会在控制台报 Service Worker 不可用、crypto API 受限等警告。这是所有非 HTTPS 部署的通病，不是 AgentTeams 特有的。

3. WASM MIME 类型缺失

Matrix 的 Rust 加密库使用了 WebAssembly，但 nginx 没有配置 .wasm 文件的 MIME 类型，导致 WebAssembly.instantiateStreaming 失败，降级到普通的 WebAssembly.instantiate（慢一些但能用）。

# 六、技术细节：给想部署的同学参考

## 6.1 双容器架构理解

##

AgentTeams 采用的是 Controller + Manager 双容器架构：

│ hiclaw-controller

├── Higress Gateway (网关)

├── MinIO (对象存储)

├── Tuwunel (Matrix 聊天服务端)

└── mc mirror (数据同步)

│ 端口: 8080, 18001, 18088

│ hiclaw-manager

├── CoPaw (Agent 管理)

├── Python workspace

└── 连接 Controller 的各个服务

│ 端口: 18888

关键理解：

--network container: 只共享网络命名空间，不共享文件系统

Manager 可以通过 127.0.0.1 访问 Controller 的所有端口

但 Controller 里创建的文件，Manager 里看不到

## 6.2 端口规划建议

部署前先检查目标服务器的端口占用情况：

-

```
ss -tlnp | grep -E ':(8080|18080|8000|18001|18088|18888) '
```

AgentTeams 默认需要的端口：

-
-
-
-

```
8080：Higress Gateway（最常冲突的端口）18001：Higress Console18088：Element Web18888：CoPaw Manager
```

如果 8080 被占用，可以通过 AGENTTEAMS_PORT_GATEWAY 环境变量改到其他端口。但更建议把占用 8080 的服务迁走或卸载。

# 七、总结

## 实际体验 vs 官方宣传

官方说法 实际体验

一行命令、分钟级部署 ✅ 如果服务器有外网、端口没冲突、用 x86 架构，确实是分钟级

适用于企业级场景 ✅ 架构设计确实考虑了企业需求（安全、权限、IM 集成）

开箱即用 ⚠️ LLM 提供商需要额外配置，Element Web 有些小问题需要调

哪些情况会增加部署难度

服务器没有外网：镜像需要中转，多一步操作

目标端口已被占用：需要提前规划端口或卸载冲突服务

ARM64 架构：镜像兼容性需要确认（我用的鲲鹏 920 没问题）

SSH 远程操作：需要用非交互模式，所有参数通过环境变量传入

## 最终状态

折腾了三天后，AgentTeams 终于稳定运行在了我的 237 服务器上。现在可以通过 CoPaw Manager 控制台（http://192.168.100.237:18888）来管理 Agent，通过 Element Web（http://192.168.100.237:18088）来进行团队协作聊天。

说实话，如果一开始就用官方安装脚本，可能半天就能搞定。第一天手动拼 Docker 命令的做法浪费了大量时间。但这段经历也让我对 AgentTeams 的内部架构有了更深入的理解——这些理解在后续的调试和运维中还是很有价值的。

如果你也打算部署 AgentTeams，我的建议是：

- 先读官方文档，找到安装脚本
- 提前检查端口占用，规划好端口分配
- 准备好 LLM 服务的连接信息（地址、API Key、模型名）
- 遇到容器 crash loop 先等几分钟，不要急着动手
- LLM 提供商通过 Web UI 配置，不要直接改配置文件

我是AI易用君，我在此公众号分享探索、学习、使用AI的经验，让我们一起来学AI，用AI，AI（爱）让生活更美好。如果你觉得我说的对，欢迎点赞收藏。
