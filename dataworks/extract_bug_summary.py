#!/usr/bin/env python3
"""
提取后台二组 bug 摘要信息
"""

import glob
import re
import json

# 找到文件
files = glob.glob('*.doc')
target = [f for f in files if '领视' in f][0]

print("=" * 60)
print("📊 提取后台二组 bug 记录")
print("=" * 60)
print(f"\n文件：{target}")

# 读取文件
with open(target, 'rb') as f:
    content = f.read().decode('utf-8', errors='ignore')

# 提取所有 Jira ID
all_ids = re.findall(r'GD-\d+', content)
unique_ids = sorted(list(set(all_ids)), key=lambda x: int(x.split('-')[1]))

print(f"总出现次数：{len(all_ids)}")
print(f"唯一 bug 数：{len(unique_ids)}")

# 按 ID 范围分组
id_ranges = {
    'GD-5xxxx (早期)': [x for x in unique_ids if x.startswith('GD-5')],
    'GD-60xxx-64xxx': [x for x in unique_ids if x.startswith('GD-60') or x.startswith('GD-61') or x.startswith('GD-62') or x.startswith('GD-63') or x.startswith('GD-64')],
    'GD-65xxx-69xxx': [x for x in unique_ids if x.startswith('GD-65') or x.startswith('GD-66') or x.startswith('GD-67') or x.startswith('GD-68') or x.startswith('GD-69')],
    'GD-70xxx+ (最新)': [x for x in unique_ids if x.startswith('GD-7')]
}

print("\n📋 Bug 分布（按 ID 范围）:")
for range_name, ids in id_ranges.items():
    print(f"  {range_name}: {len(ids)} 个")

# 提取每个 bug 的标题（查找 GD-XXXX 后面的文本）
bugs_with_title = []
for jid in unique_ids[:100]:  # 先处理前 100 个
    # 查找 Jira ID 附近的文本
    pattern = re.escape(jid) + r'[^\w\u4e00-\u9fa5]([^\n]{5,100}?)'
    match = re.search(pattern, content)
    title = match.group(1).strip() if match else ''
    
    if title:
        bugs_with_title.append({
            'jira_id': jid,
            'title': title[:100]
        })

print(f"\n✅ 提取到 {len(bugs_with_title)} 个带标题的 bug")

# 显示前 30 个
print("\n📝 前 30 个 bug:")
for bug in bugs_with_title[:30]:
    print(f"  {bug['jira_id']}: {bug['title']}")

# 保存结果
result = {
    'total_bugs': len(unique_ids),
    'id_distribution': {k: len(v) for k, v in id_ranges.items()},
    'bugs_sample': bugs_with_title[:50],
    'all_ids': unique_ids
}

with open('backend_bugs_summary.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ 结果保存到 backend_bugs_summary.json")
