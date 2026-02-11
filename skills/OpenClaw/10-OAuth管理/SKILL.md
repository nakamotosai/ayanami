---
name: OpenClaw-OAuth管理
description: 依据官方文档更新的 OAuth 更换流程（OpenAI Codex / ChatGPT OAuth 等）。
priority: HIGH
---

# OpenClaw OAuth 更换流程（官方正确版）

> 适用场景：更换 OAuth 账号（OpenAI Codex / ChatGPT OAuth 等），或额度用完需要切换账号。
> 依据官方文档：`https://docs.openclaw.ai/concepts/oauth`

---

## ✅ 核心事实（请牢记）

- OAuth 凭据是**按 agent 存储**，位置：
  `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- 运行时缓存：`~/.openclaw/agents/<agentId>/agent/auth.json`（**不要手改**）
- 旧版导入：`~/.openclaw/credentials/oauth.json`（仅迁移用）

---

## 🔧 正确更换 OAuth（推荐流程）

### 1) 可选：先停网关（避免后台写回旧 token）

```bash
systemctl --user stop openclaw-gateway
```

### 2) 删除旧账号的 auth-profiles

**主 agent (main)：**

```bash
rm /home/ubuntu/.openclaw/agents/main/agent/auth-profiles.json
```

**其他 agent：**

```bash
rm /home/ubuntu/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

> 只删 `auth-profiles.json`，**不要删** `auth.json`（运行时缓存会自行重建）。

### 3) 触发 OAuth 登录

推荐官方命令：

```bash
openclaw models auth login --provider openai-codex
```

或使用向导：

```bash
openclaw onboard --auth-choice openai-codex
```

### 4) 无头/远程服务器登录（重点）

OAuth 回调默认会尝试 `http://127.0.0.1:1455/auth/callback`。
如果服务器无法打开浏览器，会提示你**粘贴重定向 URL**。

流程：

- 在你本地浏览器打开 OpenClaw 提供的 OAuth 登录链接
- 用**新账号**完成授权
- 将浏览器地址栏的**最终 redirect URL**粘回服务器终端

### 5) 验证授权是否生效

```bash
openclaw models status
```

可选：进行真实 probe（会实际请求）：

```bash
openclaw models status --probe --probe-provider openai-codex
```

---

## 🔁 多账号切换/优先顺序（可选）

OpenClaw 支持一个 provider 多个 profile。可指定优先顺序：

```bash
openclaw models auth order set --provider openai-codex <profileA> <profileB>
```

查看顺序：

```bash
openclaw models auth order get --provider openai-codex
```

---

## ✅ 常见问题

### Q1: 删除 auth-profiles 会影响记忆或配置吗？

不会。只会清空 OAuth/Key 凭据。

### Q2: 没有 openclaw logout 命令怎么办？

官方推荐方式就是**删除 auth-profiles.json**，然后重新登录。

### Q3: 为什么还是旧账号？

通常是：

- 网关没停，旧 token 被后台写回
- 登录时浏览器没切账号（仍是旧账号）
- 多 profile 但 order 没设置，仍在轮转旧账号

---

## ✅ 适配 Anthropic (补充)

Anthropic 订阅 OAuth 使用 setup-token 流程：

```bash
openclaw models auth setup-token --provider anthropic
```

或粘贴已有 token：

```bash
openclaw models auth paste-token --provider anthropic
```

---

## ✅ 最短执行清单（复制即可）

```bash
systemctl --user stop openclaw-gateway
rm /home/ubuntu/.openclaw/agents/main/agent/auth-profiles.json
openclaw models auth login --provider openai-codex
openclaw models status
systemctl --user start openclaw-gateway
```
