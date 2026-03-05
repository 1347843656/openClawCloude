# 🦞 龙虾 AI 助手 - Windows 安装指南

> 适用于 Windows 10/11 系统  
> 目标：在本地电脑部署 OpenClaw，让 AI 助手帮你做更多事！

---

## 📋 安装前准备

### 系统要求
- ✅ Windows 10 或 Windows 11
- ✅ 至少 8GB 内存（推荐 16GB）
- ✅ 至少 20GB 可用磁盘空间
- ✅ 稳定的网络连接
- ✅ 管理员权限

### 需要安装的软件
1. **Git for Windows**
2. **Node.js (v24+)**
3. **Google Chrome 浏览器**
4. **OpenClaw**

---

## 🚀 安装步骤

### 第一步：安装 Git

1. 访问：https://git-scm.com/download/win
2. 下载 **64-bit Git for Windows Setup**
3. 运行安装程序，一路 Next 即可
4. 安装完成后，打开 **Git Bash** 测试：
   ```bash
   git --version
   ```

---

### 第二步：安装 Node.js

1. 访问：https://nodejs.org/
2. 下载 **LTS 版本**（推荐）或 Current 版本（v24+）
3. 运行安装程序，一路 Next
4. 安装完成后，打开 **命令提示符** 或 **PowerShell** 测试：
   ```bash
   node --version
   npm --version
   ```

---

### 第三步：安装 Google Chrome

1. 访问：https://www.google.com/chrome/
2. 下载并安装 Chrome
3. **重要：** 记住 Chrome 的安装路径，后面配置浏览器要用

---

### 第四步：克隆仓库

1. 打开 **Git Bash** 或 **PowerShell**
2. 选择一个目录（如 `D:\Projects`）
3. 运行：
   ```bash
   git clone https://github.com/1347843656/openClawCloude.git
   cd openClawCloude
   ```

---

### 第五步：安装 OpenClaw

1. 打开 **PowerShell**（以管理员身份运行）
2. 运行：
   ```powershell
   npm install -g openclaw
   ```
3. 等待安装完成（可能需要几分钟）
4. 测试安装：
   ```bash
   openclaw --version
   ```

---

### 第六步：初始化工作区

1. 打开 **PowerShell**
2. 进入仓库目录：
   ```powershell
   cd D:\Projects\openClawCloude
   ```
3. 初始化：
   ```bash
   openclaw init
   ```
4. 按提示完成配置

---

### 第七步：启动 Gateway

```bash
openclaw gateway start
```

看到 `Gateway started` 表示成功！

---

## 🌐 配置浏览器（关键！）

### 安装 OpenClaw Browser Relay 扩展

1. 打开 **Google Chrome**
2. 访问 Chrome 网上应用店
3. 搜索：**OpenClaw Browser Relay**
4. 点击 **添加至 Chrome**
5. 安装完成后，点击扩展图标，确保状态为 **ON**

### 测试浏览器连接

在 PowerShell 中运行：
```bash
openclaw browser status
```

看到 `connected` 表示成功！

---

## ✅ 验证安装

### 测试 1：检查 Gateway 状态
```bash
openclaw gateway status
```

### 测试 2：检查浏览器连接
```bash
openclaw browser status
```

### 测试 3：让 AI 助手自我介绍
在 webchat 或配置的消息渠道中发送：
```
你好，你是谁？
```

如果 AI 回复正常，说明安装成功！

---

## 🔧 常见问题

### 问题 1：npm 安装失败
**原因：** 网络问题或权限不足

**解决：**
```powershell
# 使用管理员权限运行 PowerShell
# 或尝试使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm install -g openclaw
```

---

### 问题 2：Git 克隆失败
**原因：** 网络问题

**解决：**
```bash
# 使用 Gitee 镜像（如果有）
git clone https://gitee.com/你的用户名/openClawCloude.git

# 或使用代理
git clone -c http.proxy=http://127.0.0.1:7890 https://github.com/1347843656/openClawCloude.git
```

---

### 问题 3：浏览器扩展无法连接
**原因：** 扩展未激活或端口被占用

**解决：**
1. 确保 Chrome 扩展图标是 **ON** 状态
2. 关闭所有 Chrome 窗口，重新打开
3. 重启 Gateway：
   ```bash
   openclaw gateway restart
   ```

---

### 问题 4：中文路径问题
**原因：** Windows 中文路径可能导致某些工具异常

**解决：**
- 尽量使用英文路径，如 `D:\Projects\openClawCloude`
- 避免使用 `C:\Users\用户名\桌面` 等含中文的路径

---

## 🎯 安装完成后能做什么？

### 浏览器自动化 🌐
- 自动发布小说到番茄小说网
- 网页信息采集
- 自动填写表单
- 截图/录屏

### 文件管理 📁
- 自动整理文件
- 批量重命名
- 文档转换

### 消息通知 📧
- 邮件自动处理
- 日历提醒
- 消息推送

### 小说创作 ✍️
- 自动续写章节
- 大纲管理
- 人物设定追踪

### 搜索研究 🔍
- 隐私搜索引擎（SearXNG）
- AI 优化搜索（Tavily）
- 信息整理

---

## 📞 需要帮助？

如果安装过程中遇到问题：

1. 查看 OpenClaw 官方文档：https://docs.openclaw.ai
2. 加入 Discord 社区：https://discord.com/invite/clawd
3. 在 GitHub 提 Issue：https://github.com/openclaw/openclaw/issues

---

## 🦞 龙虾的温馨提示

1. **安装完成后，记得告诉我！** 我会测试连接是否正常
2. **浏览器扩展一定要装！** 这是我帮你操作浏览器的关键
3. **建议把仓库同步到本地后，先测试基础功能**，再逐步配置高级功能
4. **Token 要保存好！** 不要泄露给他人

---

_安装愉快！有问题随时问我！🦞_

_最后更新：2026-03-05_
