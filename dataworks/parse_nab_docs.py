#!/usr/bin/env python3
"""
解析 nab-project-cases 目录下的 HTML 格式 Word 文档
提取 Jira ticket 关键信息
"""

import os
import re
import json
from html.parser import HTMLParser

class JiraHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_tag = None
        self.current_class = None
        self.in_title = False
        self.in_table = False
        self.in_cell = False
        self.current_row = []
        self.table_data = []
        self.title = ""
        self.text_content = []
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        self.current_class = attrs_dict.get('class', '')
        
        if tag == 'title':
            self.in_title = True
        elif tag == 'tr':
            self.current_row = []
        elif tag in ['td', 'th']:
            self.in_cell = True
            
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'tr' and self.current_row:
            self.table_data.append(self.current_row)
        elif tag in ['td', 'th']:
            self.in_cell = False
            
    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_cell:
            self.current_row.append(data.strip())
        elif data.strip():
            self.text_content.append(data.strip())

def parse_doc(filepath):
    """解析单个文档"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    parser = JiraHTMLParser()
    try:
        parser.feed(content)
    except:
        pass
    
    # 提取标题中的 Jira ID
    title_match = re.search(r'\[?(GD-\d+)\]?\s*(.+)', parser.title)
    jira_id = title_match.group(1) if title_match else "Unknown"
    issue_title = title_match.group(2) if title_match else parser.title
    
    # 尝试从表格中提取关键信息
    info = {
        'jira_id': jira_id,
        'title': issue_title.strip(),
        'table_data': parser.table_data,
        'text_snippet': ' '.join(parser.text_content[:50])[:500]
    }
    
    return info

def main():
    docs_dir = "nab-project-cases"
    output_file = "nab-project-cases/summary.json"
    
    files = sorted([f for f in os.listdir(docs_dir) if f.endswith('.doc') or f.endswith('.docx')])
    
    print(f"📂 找到 {len(files)} 个文档\n")
    
    all_cases = []
    
    for filename in files:
        filepath = os.path.join(docs_dir, filename)
        print(f"📄 解析：{filename}")
        
        info = parse_doc(filepath)
        all_cases.append(info)
        
        print(f"   Jira ID: {info['jira_id']}")
        print(f"   标题：{info['title'][:80]}...")
        print()
    
    # 保存为 JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_cases, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 解析完成！结果保存到 {output_file}")
    print(f"📊 共解析 {len(all_cases)} 个案例")

if __name__ == "__main__":
    main()
