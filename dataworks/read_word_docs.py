#!/usr/bin/env python3
"""
读取 nab-project-cases 目录下的 Word 文档
"""

import os
import sys

try:
    from docx import Document
except ImportError:
    print("正在安装 python-docx...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "python-docx", "-q"], check=True)
    from docx import Document

def read_docx(filepath):
    """读取 Word 文档内容"""
    try:
        doc = Document(filepath)
        content = []
        for para in doc.paragraphs:
            if para.text.strip():
                content.append(para.text)
        return "\n".join(content)
    except Exception as e:
        return f"读取失败：{e}"

def main():
    docs_dir = "nab-project-cases"
    
    if not os.path.exists(docs_dir):
        print(f"目录不存在：{docs_dir}")
        return
    
    files = sorted([f for f in os.listdir(docs_dir) if f.endswith('.docx') or f.endswith('.doc')])
    
    print(f"找到 {len(files)} 个文档:\n")
    
    for filename in files:
        filepath = os.path.join(docs_dir, filename)
        print(f"\n{'='*60}")
        print(f"📄 {filename}")
        print('='*60)
        
        content = read_docx(filepath)
        
        # 显示前 1000 字符
        if len(content) > 1000:
            print(content[:1000])
            print(f"\n... (还有 {len(content) - 1000} 字符)")
        else:
            print(content)
        
        print()

if __name__ == "__main__":
    main()
