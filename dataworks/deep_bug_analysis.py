#!/usr/bin/env python3
"""
深度分析后台二组 bug - 提取完整信息
"""

import glob
import re
import json
from html.parser import HTMLParser

class JiraTableParser(HTMLParser):
    """解析 JIRA HTML 表格"""
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_cell = False
        self.current_row = []
        self.current_cell = ""
        self.all_rows = []
        self.table_depth = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'table':
            self.table_depth += 1
            if self.table_depth == 1:
                self.in_table = True
        elif tag in ['td', 'th'] and self.in_table:
            self.in_cell = True
            self.current_cell = ""
        elif tag == 'tr' and self.in_table:
            self.current_row = []
            
    def handle_endtag(self, tag):
        if tag == 'table':
            self.table_depth -= 1
            if self.table_depth == 0:
                self.in_table = False
        elif tag in ['td', 'th'] and self.in_cell:
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
        elif tag == 'tr' and self.in_table and self.current_row:
            self.all_rows.append(self.current_row)
            
    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

# 读取文件
files = glob.glob('*.doc')
target = [f for f in files if '领视' in f][0]

print("=" * 60)
print("🔍 深度解析后台二组 bug")
print("=" * 60)
print(f"\n文件：{target}")

with open(target, 'rb') as f:
    content = f.read().decode('utf-8', errors='ignore')

print(f"文件大小：{len(content):,} 字符")

# 解析 HTML 表格
parser = JiraTableParser()
parser.feed(content)

print(f"解析到 {len(parser.all_rows)} 个表格行\n")

# 提取 bug 信息
bugs = {}
current_bug = None

for row_idx, row in enumerate(parser.all_rows):
    row_text = ' '.join(row).replace('\n', ' ').replace('\xa0', ' ')
    
    # 检测新的 Jira ID
    jira_match = re.search(r'\[?(GD-\d+)\]?', row_text)
    if jira_match and len(row_text) > 20:
        jira_id = jira_match.group(1)
        
        if jira_id not in bugs:
            bugs[jira_id] = {
                'jira_id': jira_id,
                'title': '',
                'status': '',
                'module': '',
                'type': '',
                'priority': '',
                'reporter': '',
                'assignee': '',
                'resolution': '',
                'created_date': '',
                'resolved_date': '',
                'description': [],
                'comments': [],
                'is_nab': False
            }
        current_bug = bugs[jira_id]
        
        # 提取标题（通常在 GD-XXXX 后面）
        title_match = re.search(r'GD-\d+\]?\s*(.+?)(?:创建日期|$)', row_text)
        if title_match:
            current_bug['title'] = title_match.group(1).strip()[:200]
    
    # 提取其他字段
    if current_bug and row_text:
        if '状态:' in row_text:
            current_bug['status'] = row_text.replace('状态:', '').strip()
        elif '模块:' in row_text:
            current_bug['module'] = row_text.replace('模块:', '').strip()
        elif '类型:' in row_text:
            current_bug['type'] = row_text.replace('类型:', '').strip()
        elif '优先级:' in row_text:
            current_bug['priority'] = row_text.replace('优先级:', '').strip()
        elif '报告人:' in row_text:
            current_bug['reporter'] = row_text.replace('报告人:', '').strip()
        elif '经办人:' in row_text:
            current_bug['assignee'] = row_text.replace('经办人:', '').strip()
        elif '解决结果:' in row_text:
            current_bug['resolution'] = row_text.replace('解决结果:', '').strip()
            if 'Not a bug' in row_text or '不是 bug' in row_text:
                current_bug['is_nab'] = True
        elif '创建日期:' in row_text:
            date_match = re.search(r'创建日期:\s*(\d{2}/\w+/ \d{2})', row_text)
            if date_match:
                current_bug['created_date'] = date_match.group(1)
        elif '已解决:' in row_text:
            date_match = re.search(r'已解决:\s*(\d{2}/\w+/ \d{2})', row_text)
            if date_match:
                current_bug['resolved_date'] = date_match.group(1)
        elif len(row_text) > 30 and '评论' not in row_text and '注释' not in row_text:
            # 可能是描述
            if len(current_bug['description']) < 5:
                current_bug['description'].append(row_text[:300])

# 统计
print(f"提取到 {len(bugs)} 个 bug\n")

# 统计模块分布
modules = {}
for bug in bugs.values():
    module = bug['module'] or '未分类'
    modules[module] = modules.get(module, 0) + 1

print("📊 模块分布:")
for module, count in sorted(modules.items(), key=lambda x: -x[1])[:15]:
    print(f"  {module}: {count} 个")

# 统计解决结果
resolutions = {}
for bug in bugs.values():
    res = bug['resolution'] or '未解决'
    resolutions[res] = resolutions.get(res, 0) + 1

print("\n📊 解决结果分布:")
for res, count in sorted(resolutions.items(), key=lambda x: -x[1]):
    print(f"  {res}: {count} 个")

# 统计 NAB 数量
nab_count = sum(1 for b in bugs.values() if b['is_nab'])
print(f"\n🎯 Not A Bug: {nab_count} 个")

# 显示 NAB 案例
if nab_count > 0:
    print("\n📋 NAB 案例列表:")
    for bug in bugs.values():
        if bug['is_nab']:
            print(f"  {bug['jira_id']}: {bug['title'][:60]}")

# 保存详细结果
result = {
    'total_bugs': len(bugs),
    'bugs': list(bugs.values()),
    'modules': modules,
    'resolutions': resolutions,
    'nab_count': nab_count
}

with open('backend_bugs_detailed.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ 保存到 backend_bugs_detailed.json")

# 显示前 10 个完整 bug 信息
print("\n" + "=" * 60)
print("📝 前 10 个 bug 详细信息")
print("=" * 60)

for i, bug in enumerate(list(bugs.values())[:10]):
    print(f"\n{i+1}. {bug['jira_id']}")
    print(f"   标题：{bug['title']}")
    print(f"   状态：{bug['status']}")
    print(f"   模块：{bug['module']}")
    print(f"   解决结果：{bug['resolution']}")
    print(f"   创建日期：{bug['created_date']}")
    if bug['description']:
        print(f"   描述：{bug['description'][0][:100]}...")
