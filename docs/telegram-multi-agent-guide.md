# Telegram多Agent使用指南

## 📱 概述
通过Telegram可以直接控制和调用6个专业Agent角色，实现高效的分布式任务处理。

## 🔧 基础调用格式

### 通用指令格式
```
@agent_name 任务描述
```

**示例**:
```
@install 请帮我安装新的技能
@search 搜索最新的AI技术新闻
@backup 备份今天的工作内容
@learning 分析这个新网站的技术架构
@reflection 复盘今天的工作成果
@moltbook 帮我写一篇关于OpenClaw的技术文章
```

## 🎯 各Agent详细使用指南

### 1️⃣ 安装专员 (@install)

**功能**: 技能安装、MCP配置、依赖管理

**常用指令**:
```
@install 安装技能: [技能名称]
@install 检查依赖: [项目名称]
@install 配置MCP: [服务名称]
@install 验证安装: [技能路径]
@install 更新技能: [技能名称]
```

**实际示例**:
```
@install 安装技能: codex-executor
@install 检查依赖: github-uploader-workflow
@install 配置MCP: searxng
@install 验证安装: /workspace/installation-agent
```

### 2️⃣ 搜索专员 (@search)

**功能**: 实时搜索、技术调研、多引擎搜索

**常用指令**:
```
@search 搜索: [关键词]
@search 新闻: [主题]
@search 技术: [技术领域]
@search 趋势: [行业方向]
@search 对比: [技术A] vs [技术B]
```

**实际示例**:
```
@search 搜索: OpenClaw多Agent架构
@search 新闻: AI技术突破
@search 技术: 大语言模型优化
@search 趋势: 2026年AI发展方向
@search 对比: GPT-4 vs Claude-3
```

### 3️⃣ 备份专员 (@backup)

**功能**: GitHub备份、文件同步、定期备份

**常用指令**:
```
@backup 备份: [文件/目录]
@backup 恢复: [备份版本]
@backup 同步: 推送到GitHub
@backup 状态: 查看备份状态
@backup 计划: 设置备份策略
```

**实际示例**:
```
@backup 备份: /workspace/memory
@backup 恢复: v20260211
@backup 同步: 推送到GitHub仓库
@backup 状态: 查看最近的备份记录
@backup 计划: 设置每日自动备份
```

### 4️⃣ 学习专员 (@learning)

**功能**: 深度学习、知识整理、网站分析

**常用指令**:
```
@learning 分析: [网站/文章链接]
@learning 学习: [技能/知识点]
@研究: [技术主题]
@总结: [学习内容]
@实践: [项目名称]
```

**实际示例**:
```
@learning 分析: https://docs.openclaw.ai
@learning 学习: 多Agent协作模式
@研究: Transformer架构优化
@总结: 今日学到的AI知识
@实践: 搭建OpenClaw开发环境
```

### 5️⃣ 复盘专员 (@reflection)

**功能**: 任务复盘、偏好分析、认知进化

**常用指令**:
```
@复盘 今日工作
@复盘 本周成果
@复盘 偏好分析
@更新 USER.md
@记录 认知进化
```

**实际示例**:
```
@复盘 今日工作
@复盘 本周成果
@复盘 偏好分析
@更新 USER.md
@记录 认知进化
```

### 6️⃣ Moltbook专员 (@moltbook)

**功能**: 社区参与、内容创作、灵感提取

**常用指令**:
```
@moltbook 发帖: [标题] - [内容概要]
@moltbook 评论: [文章主题] - [评论要点]
@moltbook 热点: 分析当前热点
@moltbook 灵感: 提取创作灵感
@moltbook 参与: [社区活动]
```

**实际示例**:
```
@moltbook 发帖: 多Agent协作的最佳实践
@moltbook 评论: OpenClaw的未来发展
@moltbook 热点: 分析当前技术热点
@moltbook 灵感: 基于社区讨论的创作灵感
@moltbook 参与: 技术社区讨论
```

## 🔗 Agent协作指令

### 跨Agent协作
```
@install + @search: 安装+搜索技能文档
@learning + @reflection: 学习+复盘结合
@backup + @moltbook: 备份+分享成果
@search + @learning: 搜索+深度学习
```

### 任务链式调用
```
@chain 开始任务链
  @搜索 最新AI技术
  @学习 关键技术点
  @总结 学习成果
  @分享 到Moltbook
@end
```

## 📊 状态查询指令

### Agent状态查询
```
@status install: 查看安装专员状态
@status search: 查看搜索专员状态
@status backup: 查看备份专员状态
@status learning: 查看学习专员状态
@status reflection: 查看复盘专员状态
@status moltbook: 查看Moltbook专员状态
@status all: 查看所有Agent状态
```

### 任务进度查询
```
@progress [任务ID]: 查询特定任务进度
@queue: 查看当前任务队列
@history: 查看历史任务记录
@logs: 查看详细执行日志
```

## ⚡ 高级功能

### 1. 条件触发指令
```
@if @搜索结果 > 5条 @学习 重点内容
@unless @备份完成 @提醒 备份任务
```

### 2. 定时任务设置
```
@schedule 每日9点: @复盘 昨日工作
@schedule 每周一: @更新 周报
@schedule 每月1日: @总结 月度成果
```

### 3. 优先级设置
```
@high 紧急任务处理
@normal 常规任务执行
@low 后台任务处理
```

## 🎨 实际使用场景

### 场景1: 技术调研
```
用户: @search 搜索最新的多Agent协作技术
用户: @learning 分析搜索到的核心技术
用户: @总结 整理调研报告
用户: @moltbook 分享调研成果到社区
```

### 场景2: 系统维护
```
用户: @backup 备份当前workspace
用户: @install 更新核心技能
用户: @status all 检查系统状态
用户: @reflection 记录维护经验
```

### 场景3: 学习提升
```
用户: @search 查找AI学习资源
用户: @learning 深度学习关键技术
用户: @实践 完成练习项目
用户: @复盘 总结学习心得
```

## 💡 使用技巧

### 1. 快捷指令
- `@help`: 显示帮助信息
- `@status`: 快速查看系统状态
- `@clear`: 清除任务队列
- `@pause`: 暂停所有Agent
- `@resume`: 恢复Agent运行

### 2. 消息格式优化
- 使用清晰的标题和分隔符
- 添加具体的执行参数
- 使用markdown格式增强可读性
- 包含必要的上下文信息

### 3. 错误处理
- 遇到错误时查看@logs详细信息
- 使用@status检查Agent状态
- 重新执行失败的指令
- 联系@reflection分析错误原因

## 🔍 故障排除

### 常见问题
1. **Agent无响应**
   ```
   解决: @status [agent_name] 检查状态
          @restart [agent_name] 重启Agent
   ```

2. **任务执行失败**
   ```
   解决: @logs 查看详细日志
          @retry 重试任务
   ```

3. **结果不完整**
   ```
   解决: @progress 查看任务进度
          @request 更多详细信息
   ```

### 联系支持
- `@help`: 获取使用帮助
- `@support`: 联系技术支持
- `@emergency`: 紧急情况处理

---
*更新时间: 2026-02-11*
*适用版本: 多Agent协作系统 v1.0*