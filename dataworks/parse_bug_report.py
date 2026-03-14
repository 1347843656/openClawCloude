#!/usr/bin/env python3
"""
解析 JIRA bug 导出文档
"""

import os
import re

filepath = "上海领视信息科技-bug 管理系统.doc"

print(f"读取文件：{filepath}")
print(f"文件大小：{os.path.getsize(filepath) / 1024 / 1024:.2f} MB\n")

# 尝试读取文件内容
try:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        print(f"读取成功！内容长度：{len(content)} 字符\n")
        
        # 提取 Jira ID
        jira_ids = re.findall(r'GD-\d+', content)
        print(f"找到 {len(jira_ids)} 个 Jira ID")
        print(f"前 20 个：{jira_ids[:20]}")
        
        # 提取表格内容（HTML 格式）
        if '<table' in content:
            print("\n检测到 HTML 表格格式")
        
        # 显示前 2000 字符
        print("\n=== 内容预览 ===")
        print(content[:2000])
        
except Exception as e:
    print(f"读取失败：{e}")
    
    # 尝试二进制读取
    print("\n尝试二进制读取...")
    with open(filepath, 'rb') as f:
        binary_content = f.read(1000)
        print(f"前 1000 字节：{binary_content[:200]}")
