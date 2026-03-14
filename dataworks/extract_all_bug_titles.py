#!/usr/bin/env python3
"""
完整提取后台二组 bug 标题和状态
"""

import glob
import re
import json

files = glob.glob('*.doc')
target = [f for f in files if '领视' in f][0]

print("=" * 60)
print("📊 提取后台二组所有 bug")
print("=" * 60)
print(f"\n文件：{target}")

with open(target, 'rb') as f:
    content = f.read().decode('utf-8', errors='ignore')

print(f"文件大小：{len(content):,} 字符\n")

# 提取所有 [GD-XXXX] 标题
pattern = r'\[GD-(\d+)\]&nbsp;<a [^>]+>([^<]+)'
matches = re.findall(pattern, content)

print(f"✅ 提取到 {len(matches)} 个 bug 标题\n")

# 整理 bug 列表
bugs = []
for jid, title in matches:
    bugs.append({
        'jira_id': f'GD-{jid}',
        'title': title.strip()[:150]
    })

# 去重
seen = set()
unique_bugs = []
for bug in bugs:
    if bug['jira_id'] not in seen:
        seen.add(bug['jira_id'])
        unique_bugs.append(bug)

print(f"去重后：{len(unique_bugs)} 个唯一 bug\n")

# 按 ID 排序
unique_bugs.sort(key=lambda x: int(x['jira_id'].split('-')[1]))

# 显示前 50 个
print("📋 前 50 个 bug:")
for bug in unique_bugs[:50]:
    print(f"  {bug['jira_id']}: {bug['title'][:60]}")

# 统计 ID 分布
id_ranges = {
    'GD-5xxxx': 0,
    'GD-60xxx': 0,
    'GD-61xxx': 0,
    'GD-62xxx': 0,
    'GD-63xxx': 0,
    'GD-64xxx': 0,
    'GD-65xxx': 0,
    'GD-66xxx': 0,
    'GD-67xxx': 0,
    'GD-68xxx': 0,
    'GD-69xxx': 0,
    'GD-70xxx+': 0
}

for bug in unique_bugs:
    prefix = bug['jira_id'][:6]
    for r in id_ranges.keys():
        if prefix in r or (r == 'GD-70xxx+' and bug['jira_id'].startswith('GD-7')):
            id_ranges[r] += 1
            break

print("\n📊 ID 分布:")
for r, count in id_ranges.items():
    if count > 0:
        print(f"  {r}: {count} 个")

# 查找 Not A Bug 相关的 bug
nab_keywords = ['不是 bug', 'Not a bug', '功能如此', '设计如此', '理解偏差', '统计口径', '逻辑问题']
nab_bugs = []

for bug in unique_bugs:
    # 在完整内容中查找该 bug 是否有 NAB 标记
    bug_pattern = bug['jira_id'] + r'[^\n]{0,500}(不是 bug|Not a bug|功能如此|设计如此)'
    if re.search(bug_pattern, content, re.IGNORECASE):
        nab_bugs.append(bug)

print(f"\n🎯 找到 {len(nab_bugs)} 个可能的 Not A Bug")
for bug in nab_bugs[:20]:
    print(f"  {bug['jira_id']}: {bug['title'][:60]}")

# 保存结果
result = {
    'total_bugs': len(unique_bugs),
    'bugs': unique_bugs,
    'nab_bugs': nab_bugs,
    'id_distribution': id_ranges
}

with open('backend_all_bugs.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ 结果保存到 backend_all_bugs.json")
