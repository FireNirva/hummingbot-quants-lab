#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将PDF截图转换为Markdown格式
这个脚本需要安装以下库：
pip install pypdf2 pillow
"""

import os
import sys
import re
from pathlib import Path
import subprocess

try:
    import pypdf
except ImportError:
    print("请安装必要的库: pip install pypdf")
    sys.exit(1)

def pdf_to_text(pdf_path):
    """从PDF中提取文本"""
    text = ""
    try:
        # 打开PDF文件
        reader = pypdf.PdfReader(pdf_path)
        
        # 提取文本内容
        for i, page in enumerate(reader.pages):
            print(f"处理页面 {i+1}/{len(reader.pages)}...")
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
            
        return text
    except Exception as e:
        print(f"处理PDF时出错: {e}")
        return ""

def manual_extract_text():
    """如果自动提取失败，提供手动输入选项"""
    print("\n自动文本提取可能会失败，特别是对于截图PDF。")
    print("请考虑手动输入交易对列表，格式为：符号 名称，每行一个")
    
    tokens = []
    print("请输入交易对（每行一个，格式为'符号 名称'，输入空行结束）：")
    while True:
        line = input().strip()
        if not line:
            break
            
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            symbol, name = parts
            tokens.append((symbol, name))
        else:
            print(f"忽略无效输入: {line}")
    
    return tokens

def save_to_markdown(tokens, output_path, ecosystem_name):
    """保存为Markdown格式"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {ecosystem_name} 生态系统代币\n\n")
        f.write("| 符号 | 名称 |\n")
        f.write("|------|------|\n")
        
        for symbol, name in tokens:
            symbol = symbol.strip()
            name = name.strip()
            if symbol and name:  # 确保不为空
                f.write(f"| {symbol} | {name} |\n")

def extract_token_pairs(text):
    """提取代币对信息"""
    # 查找代币符号和名称
    # 这个正则表达式需要根据实际PDF内容格式进行调整
    token_pattern = re.compile(r'([A-Z0-9]{1,10})\s+([A-Za-z0-9\s]+)')
    tokens = token_pattern.findall(text)
    
    # 如果没找到任何代币对，提供手动输入选项
    if not tokens:
        print("未能自动提取到代币对信息，可能是因为PDF是截图形式。")
        tokens = manual_extract_text()
    
    return tokens

def main():
    # 输入和输出目录
    input_dir = Path("config/gateio_pairs_lists/screenshot")
    output_dir = Path("config/gateio_pairs_lists/markdown")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理所有PDF文件
    for pdf_file in input_dir.glob("*.pdf"):
        print(f"正在处理: {pdf_file.name}")
        
        # 确定生态系统名称
        ecosystem_name = pdf_file.stem.split('_')[0]
        
        # 提取文本
        text = pdf_to_text(pdf_file)
        print(f"提取的文本长度: {len(text)} 字符")
        
        if len(text) < 10:  # 如果提取到的文本太少
            print("警告: 提取到的文本非常少，这可能是因为PDF是截图，无法提取文本内容。")
            print(f"请查看此PDF: {pdf_file}")
            
            # 询问是否手动输入
            answer = input("是否手动输入此PDF的交易对信息？(y/n): ")
            if answer.lower() == 'y':
                tokens = manual_extract_text()
            else:
                print(f"跳过 {pdf_file.name}")
                continue
        else:
            # 提取代币对
            tokens = extract_token_pairs(text)
        
        if tokens:
            # 保存为Markdown
            output_path = output_dir / f"{pdf_file.stem}.md"
            save_to_markdown(tokens, output_path, ecosystem_name)
            print(f"已保存: {output_path} (包含 {len(tokens)} 个交易对)")
        else:
            print(f"未能提取到任何交易对信息，跳过 {pdf_file.name}")

if __name__ == "__main__":
    main() 