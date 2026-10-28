---
title: "OpenWork Local CA：解决浏览器“不安全”警告"
type: document
source: self-hosted
file_type: md
file_path: /root/vault/6-System/证书/2026-10-28 - OpenWork Local CA 自签证书方案.md
uploaded_date: 2026-10-28
title_short: "OpenWork Local CA"
description: "为 101.35.52.96 上所有服务（Rakazo / SolidCraft / OpenWork）建立一套可被手机/电脑信任的根 CA + 叶证书体系，根治浏览器“不安全”警告"
size_bytes: 0
tags:
  - tls
  - certificate
  - nginx
  - ssl
  - openwork
  - security
  - rakazo
  - solidcraft
related:
  - "1-Projects/OpenWork-部署/2026-10-28 - Rakazo 部署实录（2C4G 服务器完整落地）.md"
  - "2-Areas/AI-Agent-研究/2026-10-28 - SolidCraft - 纯 Rust 参数化 3D CAD 与 MCP Agent 接入.md"
server: "101.35.52.96 (腾讯云 2C4G, Ubuntu 24.04, nginx 1.24.0)"
---

# OpenWork Local CA —— 根治浏览器“不安全”警告

> **日期**：2026-10-28 23:00 ｜ **触发**：何大人发来截图，Rakazo 登录页显示「不安全」
> **状态**：✅ 已完成并全站生效

---

## 一、问题本质

何大人看到的「不安全」**不是没加密**，而是**浏览器不信任签发方**。

原配置用的是一张**自签证书**（`openwork.crt`）：
```
subject = CN = 101.35.52.96.nip.io, O = OpenWork
issuer  = CN = 101.35.52.96.nip.io, O = OpenWork   ← 自己签自己
```
浏览器不认这个 issuer → 标「不安全」→ **登录框里的邮箱密码虽然走 TLS，但浏览器无法确认对面真是这台服务器**。

---

## 二、为什么拿不到 Let's Encrypt 证书（重要结论）

试过三条路，**全部失败**，根因是**腾讯云的 ICP 备案拦截 + 边缘网络重置**。

### 路径 1：certbot + HTTP-01（webroot）
```
Domain: 101.35.52.96.sslip.io
Detail: 43.174.225.201: Invalid response from
        https://dnspod.qcloud.com/static/webblock.html?d=101.35.52.96.sslip.io: 566
```
腾讯云把 `sslip.io` 泛域名劫持到了 **`dnspod.qcloud.com/static/webblock.html`**（未备案域名的拦截页）。

### 路径 2：certbot + HTTP-01（nip.io）
```
Domain: 101.35.52.96.nip.io
Detail: 101.35.52.96: Connection reset by peer
```
直接被重置。

### 路径 3：acme.sh + **TLS-ALPN-01**（走 443，完全不发 HTTP 请求）
```bash
./acme.sh --issue --server letsencrypt --keylength ec-256 \
  -d 101.35.52.96.sslip.io -d 101.35.52.96.nip.io --alpn
# → "101.35.52.96.sslip.io: Invalid status. Verification error details:
#    101.35.52.96: Connection reset by peer"
```
**连 ALPN 也被重置** → 说明是**腾讯云边缘对境外验证节点的网络层封锁**，不是 HTTP 层拦截。

> ⚠️ acme.sh 需要独占 443，与 nginx 冲突 → 签发时需短暂停 nginx（约 20 秒）。
> **最终结论：除非有自己的域名（且能配 DNS-01），这台机器拿不到 Let's Encrypt 证书。**
> acme.sh 已装在 `/root/acme.sh`（Gitee 镜像 `gitee.com/neilpang/acme.sh` 可下载，GitHub 官方源在本机不通），备用。

---

## 三、最终方案：自建根 CA + 叶证书（两级链）

### 证书体系
```
OpenWork Local Root CA   (CA:TRUE, 10 年, 到 2036-10-25)  ← 何大人装这个
        ↓ 签发
101.35.52.96.sslip.io    (CA:FALSE, 825 天, 到 2029-01-30) ← nginx 用这个
   SAN: DNS:101.35.52.96.sslip.io, DNS:101.35.52.96.nip.io, IP:101.35.52.96
```

### 关键设计决策
| 决策 | 理由 |
|---|---|
| **两级链**（根 CA + 叶证书）| 叶证书可短命（825 天，符合 Apple 政策），根 CA 长期；将来续期只需重签叶证书，**何大人不用重装信任** |
| **叶证书 825 天** | Apple 对公开信任证书的限制；用户自装根不受此限，但 825 天最保险 |
| **nginx 发完整链** | `ssl_certificate` 必须指向 **leaf + root** 拼接的 fullchain，否则客户端提示 "unable to verify the first certificate" |
| **保留旧自签证书** | 备份为 `openwork.crt.bak.<ts>`，回滚用 |
| **统一所有站点** | `rakazo.conf` + `openwork.conf`（默认站点 `server_name _`）全部切到同一张证书 → **一次安装，全站生效** |

### 文件位置
| 文件 | 用途 |
|---|---|
| `/root/solidcraft/ca/ca.crt` | **根 CA 证书**（要发给何大人的）|
| `/root/solidcraft/ca/ca.key` | 根 CA 私钥（10 年，用于签发叶证书）|
| `/root/solidcraft/ca/server.crt` | 叶证书 |
| `/root/solidcraft/ca/server.key` | 叶证书私钥 |
| `/etc/nginx/ssl/openwork-fullchain.crt` | **nginx 实际使用**（leaf + root）|
| `/etc/nginx/ssl/openwork-server.key` | nginx 实际使用 |
| `/etc/nginx/ssl/openwork-ca.crt` | 供 HTTP 下载 |
| `/etc/nginx/ssl/openwork.crt.bak.*` | 旧自签证书备份 |

### CA 指纹（供核对）
```
SHA256: B2:7F:5B:E3:E2:47:04:A5:6F:DE:48:E1:48:8E:56:AB:6B:E1:AB:7A:A7:54:64:B4:AF:DF:A0:E8:59:F1:CF:5B
subject: C=CN, O=OpenWork Local CA, CN=OpenWork Local Root CA
valid:   2026-10-28 → 2036-10-25
```

---

## 四、下载入口

```
http://101.35.52.96.sslip.io/OpenWork-Local-CA.crt   （明文 HTTP，刻意不跳 HTTPS，避免浏览器拦截下载）
```
nginx 里专门开了 `location = /OpenWork-Local-CA.crt`，用 `application/x-x509-ca-cert` + `Content-Disposition: attachment`。

同时通过微信把 `.crt` 文件直接发给了何大人。

---

## 五、安装指引（发给何大人的）

### iPhone / iPad
1. 打开下载链接（或用微信里收到的 `.crt` 文件）
2. Safari 提示「已下载描述文件」→ 点「**设置**」
3. **设置 → 通用 → VPN与设备管理** → 点「OpenWork Local Root CA」→ **安装**
4. **设置 → 通用 → 关于本机 → 证书信任设置** → 打开「OpenWork Local Root CA」开关 ← **这一步最关键，不开不生效**

### Android
1. 下载 `.crt` 文件
2. **设置 → 安全 → 加密与凭据 → 安装证书 → CA 证书** → 选择文件
3. （部分机型：设置 → 安全 → 更多安全设置 → 凭据 → 安装证书 → CA 证书）
4. ⚠️ **注意**：Android 上**只有浏览器信任用户自装 CA**；部分原生 App 只认系统 CA，这是 Android 的设计限制

### Windows
双击 `.crt` → 「安装证书」→「本地计算机」→ 「受信任的根证书颁发机构」→ 完成

### macOS
双击 `.crt` → 钥匙串访问 → 把它拖进「**系统**」钥匙串 → 双击 → 「信任」→ **始终信任**

---

## 六、验证过程（全部实测）

| 测试 | 结果 |
|---|---|
| `openssl verify -CAfile ca.crt server.crt` | ✅ `server.crt: OK` |
| 服务端链 | ✅ 发送 2 个证书（leaf + root）|
| `openssl s_client -CAfile ca.crt` | ✅ `Verification: OK`，`Verify return code: 0 (ok)` |
| 干净 NSS 库（**无 CA**）| ❌ `<title>Privacy error</title>` ← 复现何大人的问题 |
| 干净 NSS 库 + **只装 CA** | ✅ `<title>Rakazo</title>` ← 警告消失 |
| 全站复验 | ✅ `/`、`/sign-in`、`/solidcraft/`、CA 下载全部 HTTP 200 |

### ⚠️ 一个测试陷阱
用 `HOME=/tmp/fakehome` 想模拟干净环境时 Chrome 仍被拦截 —— 原因是 **Chrome 用 `getpwuid()` 找 NSS 库，不认 `$HOME` 覆盖**。改用真实 HOME + 干净 `--user-data-dir` 才测出真实结果。

### ⚠️ nginx 也有个小坑
第一次只让 nginx 发叶证书（`ssl_certificate` 指向 `server.crt`），客户端报 `Verify return code: 21 (unable to verify the first certificate)`。必须发 **fullchain**（leaf + root 拼接）。

---

## 七、续期

| 对象 | 到期 | 处理 |
|---|---|---|
| 叶证书 | **2029-01-30** | 已建 cron 提醒（2028-01-15 触发，job id `eebcb52e-8fd7-4e47-bf4a-886c2b3591fc`）|
| 根 CA | 2036-10-25 | 基本不用动 |

重签叶证书：
```bash
cd /root/solidcraft/ca
openssl req -new -key server.key -out server.csr -subj "/C=CN/O=OpenWork/CN=101.35.52.96.sslip.io" \
  -addext "subjectAltName=DNS:101.35.52.96.sslip.io,DNS:101.35.52.96.nip.io,IP:101.35.52.96"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 825 -sha256 \
  -extfile <(printf "basicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth\nsubjectAltName=DNS:101.35.52.96.sslip.io,DNS:101.35.52.96.nip.io,IP:101.35.52.96\nsubjectKeyIdentifier=hash\nauthorityKeyIdentifier=keyid,issuer")
cat server.crt ca.crt > /etc/nginx/ssl/openwork-fullchain.crt
nginx -t && systemctl reload nginx
```

---

## 八、如果何大人有自己的域名（更优解）

那就直接上 Let's Encrypt，配 DNS-01 自动续期，不再需要装 CA：
```bash
# acme.sh 已装：/root/acme.sh（Gitee 镜像）
/root/acme.sh --issue --dns dns_xxx -d xxx.你的域名 --server letsencrypt
/root/acme.sh --install-cert -d xxx.你的域名 --fullchain-file /etc/nginx/ssl/xxx.crt --key-file /etc/nginx/ssl/xxx.key
```
> ⚠️ 但要注意：**域名指向国内腾讯云服务器同样需要 ICP 备案**，否则会被 webblock（这正是 sslip.io 失败的原因）。用**香港/海外节点**可绕过。

---

*记录人：小助 ｜ 2026-10-28*
