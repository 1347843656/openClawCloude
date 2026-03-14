#!/usr/bin/env python3
"""
完整解析 JIRA bug 导出文档 - 后台二组
"""

import os
import re
import json
from html.parser import HTMLParser

class JiraBugParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_cell = False
        self.current_row = []
        self.table_data = []
        self.current_cell = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag in ['td', 'th'] and self.in_table:
            self.in_cell = True
            self.current_cell = ""
        elif tag == 'tr' and self.in_table:
            self.current_row = []
            
    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        elif tag in ['td', 'th'] and self.in_cell:
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
        elif tag == 'tr' and self.in_table and self.current_row:
            self.table_data.append(self.current_row)
            
    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

# 解析文件
filepath = "/home/admin/.openclaw/workspace/dataworks/上海领视信息科技-bug 管理系统.doc"

print("=" * 60)
print("📊 解析后台二组 bug 记录")
print("=" * 60)

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print(f"\n文件大小：{os.path.getsize(filepath) / 1024 / 1024:.2f} MB")
print(f"文本长度：{len(content):,} 字符")

# 解析 HTML
parser = JiraBugParser()
parser.feed(content)

print(f"\n解析到 {len(parser.table_data)} 个表格行")

# 提取 Jira ID 和对应的 bug 信息
bugs = {}
current_bug = None

for row in parser.table_data:
    row_text = ' '.join(row)
    
    # 检测是否是新的 Jira ID
    jira_match = re.search(r'\[?(GD-\d+)\]?', row_text)
    if jira_match:
        jira_id = jira_match.group(1)
        if jira_id not in bugs:
            bugs[jira_id] = {
                'jira_id': jira_id,
                'title': '',
                'status': '',
                'module': '',
                'description': [],
                'resolution': ''
            }
        current_bug = bugs[jira_id]
        
        # 提取标题
        if ']' in row_text:
            title_part = row_text.split(']')[-1].strip()
            if len(title_part) > 5 and len(title_part) < 200:
                current_bug['title'] = title_part
    
    # 提取其他信息
    if current_bug:
        if '状态:' in row_text:
            current_bug['status'] = row_text.replace('状态:', '').strip()
        elif '模块:' in row_text:
            current_bug['module'] = row_text.replace('模块:', '').strip()
        elif '解决结果:' in row_text:
            current_bug['resolution'] = row_text.replace('解决结果:', '').strip()
        elif len(row_text) > 20 and '评论' not in row_text and '注释' not in row_text:
            # 可能是描述或评论
            if len(current_bug['description']) < 10:  # 最多保存 10 条描述
                current_bug['description'].append(row_text[:300])

# 统计
print(f"\n提取到 {len(bugs)} 个唯一的 bug")

# 显示前 20 个
print("\n" + "=" * 60)
print("📋 前 20 个 bug 记录")
print("=" * 60)

for i, (jid, bug) in enumerate(list(bugs.items())[:20]):
    print(f"\n{i+1}. {jid}")
    print(f"   标题：{bug['title'][:80]}")
    print(f"   状态：{bug['status']}")
    print(f"   模块：{bug['module']}")
    print(f"   解决结果：{bug['resolution']}")

# 统计模块分布
modules = {}
for bug in bugs.values():
    module = bug['module'] or '未分类'
    modules[module] = modules.get(module, 0) + 1

print("\n" + "=" * 60)
print("📊 模块分布统计")
print("=" * 60)

for module, count in sorted(modules.items(), key=lambda x: -x[1])[:15]:
    print(f"  {module}: {count} 个")

# 保存结果
output = {
    'total_bugs': len(bugs),
    'bugs': list(bugs.values())[:50],  # 保存前 50 个
    'modules': modules
}

with open('backend_team_bugs.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n✅ 结果保存到 backend_team_bugs.json")
