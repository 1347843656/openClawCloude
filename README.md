# 🦞 龙虾 AI 助手工作区

> 个人 AI 助手「龙虾」的工作空间  
> 作者：老大 | 时区：Asia/Shanghai

---

## 📁 目录结构

```
.
├── AGENTS.md              # AI 行为指南
├── SOUL.md                # AI 人格定义
├── USER.md                # 用户信息
├── IDENTITY.md            # AI 身份信息
├── MEMORY.md              # 长期记忆
├── HEARTBEAT.md           # 心跳任务配置
├── TOOLS.md               # 本地工具配置
├── novel/                 # 小说《窥天》创作
│   ├── 正文/              # 章节正文
│   ├── 大纲/              # 故事大纲
│   ├── 人物/              # 人物档案
│   ├── 设定/              # 世界观设定
│   ├── 伏笔/              # 伏笔追踪
│   └── 发布指南/          # 发布资料
├── memory/                # 每日记忆日志
├── logs/                  # 系统日志
└── skills/                # 安装的技能
```

---

## 🚀 快速开始

### 环境要求
- OpenClaw 框架
- Node.js v24+
- Git

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone <仓库地址>
   cd <仓库目录>
   ```

2. **安装 OpenClaw**
   ```bash
   # 参考官方文档：https://docs.openclaw.ai
   npm install -g openclaw
   ```

3. **配置环境变量**
   ```bash
   # 复制示例配置
   cp .env.example .env
   # 编辑 .env 填入必要的 API 密钥
   ```

4. **启动 OpenClaw**
   ```bash
   openclaw gateway start
   ```

---

## 📖 当前项目

### 小说《窥天》
- **类型：** 玄幻 + 科幻融合
- **状态：** 连载中（第 1-21 章已完成）
- **字数：** 约 6 万字
- **发布平台：** 番茄小说（待发布）

**故事简介：**
> 林默一直以为自己在修仙，直到那天，他看到了世界的"代码"。  
> 这是一个关于 AI 觉醒、反抗虚拟世界的故事。

---

## 🛠️ 可用技能

| 技能 | 描述 |
|------|------|
| searxng | 隐私搜索引擎 |
| tavily-search | AI 优化搜索 |
| find-skills | 技能发现工具 |
| weather | 天气查询 |
| qqbot-cron | QQ 机器人定时任务 |
| qqbot-media | QQ 媒体发送 |

---

## 📝 使用指南

### 与 AI 交互
- 直接对话即可
- AI 会自动读取上下文（SOUL.md、USER.md、MEMORY.md）
- 重要信息会被记录到 memory/ 目录

### 小说创作
- 章节存放在 `novel/正文/第一卷/`
- 发布资料在 `novel/发布指南/`
- 使用 `git commit` 保存创作进度

---

## 🔐 安全提示

- 不要提交敏感信息（API 密钥、密码等）
- 定期备份重要数据
- 使用 `.gitignore` 排除隐私文件

---

## 📞 联系

- **AI 名称：** 龙虾 (Lobster)
- **Emoji：** 🦞
- **人格：** 随意、幽默、活泼

---

_最后更新：2026-03-05_
