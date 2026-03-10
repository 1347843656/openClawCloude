#!/bin/bash
# 小说写作提醒脚本 - 每小时运行一次

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
CHAPTER=$1

# 如果没传章节号，默认从 26 开始
if [ -z "$CHAPTER" ]; then
    CHAPTER=26
fi

# 写入提醒文件
cat > /home/admin/.openclaw/workspace/写作提醒.md << EOF
# ⏰ 小说写作提醒

**时间：** $TIMESTAMP

**当前进度：** 第 25 章已完成

**本章目标：** 第 $CHAPTER 章

**待办事项：**
- [ ] 写前检查（修为/位置/人物状态）
- [ ] 写作（2500-3500 字）
- [ ] 写后检查（冲突/悬念/伏笔）
- [ ] Git 提交

**回复龙虾：** "继续" 或 "写第 $CHAPTER 章"

---
_自动提醒 · 每小时一次_
EOF

echo "写作提醒已更新：第 $CHAPTER 章"
