#!/usr/bin/env python3
"""
解析 JIRA 导出文档 - 后台二组 bug 修复记录
"""

import os
import re
import json

filepath = "/home/admin/.openclaw/workspace/dataworks/上海领视信息科技-bug 管理系统.doc"

print("=" * 60)
print("📊 解析 JIRA bug 导出文档")
print("=" * 60)
print(f"\n文件：{filepath}")
print(f"大小：{os.path.getsize(filepath) / 1024 / 1024:.2f} MB\n")

# 读取文件
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print(f"读取成功！内容长度：{len(content):,} 字符\n")

# 提取所有 Jira ID
jira_ids = re.findall(r'GD-\d+', content)
print(f"📋 找到 {len(jira_ids)} 个 Jira ID")
print(f"前 50 个：{jira_ids[:50]}")

# 去重
unique_ids = list(set(jira_ids))
print(f"\n去重后：{len(unique_ids)} 个唯一 Jira ID")

# 提取包含 Jira ID 的段落/行
print("\n" + "=" * 60)
print("📝 提取 bug 记录...")
print("=" * 60)

# 尝试提取表格行或段落
bugs = []
lines = content.split('\n')

for i, line in enumerate(lines[:500]):  # 先看前 500 行
    if 'GD-' in line and len(line.strip()) > 20:
        bugs.append({
            'line': i,
            'content': line.strip()[:200]
        })

print(f"\n找到 {len(bugs)} 条包含 Jira ID 的记录\n")
for bug in bugs[:20]:  # 显示前 20 条
    print(f"行 {bug['line']}: {bug['content']}")

# 保存分析结果
result = {
    'total_jira_ids': len(jira_ids),
    'unique_jira_ids': len(unique_ids),
    'jira_ids_sample': unique_ids[:50],
    'bugs_sample': bugs[:20]
}

with open('jira_analysis_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ 分析结果已保存到 jira_analysis_result.json")
