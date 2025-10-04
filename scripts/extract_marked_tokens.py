#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从标记好的Markdown文件中提取被*标记的代币并生成YAML配置文件
"""

import re
import os
from pathlib import Path

def extract_tokens_from_file(file_path):
    """从Markdown文件中提取被星号标记的代币"""
    tokens = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 使用正则表达式提取被*包围的代币
            token_pattern = re.compile(r'\*([A-Z0-9]+)\*')
            matches = token_pattern.findall(content)
            
            print(f"  - 找到了 {len(matches)} 个标记的代币")
            
            for token in matches:
                tokens.append(token)
                print(f"    - {token}")
        
        return tokens
    except Exception as e:
        print(f"  - 读取文件时出错: {e}")
        return []

def save_to_yaml(tokens, output_path, ecosystem_name):
    """保存为YAML格式"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {ecosystem_name} 生态系统交易对配置\n\n")
        f.write(f"{ecosystem_name}_ecosystem:\n")
        
        for token in tokens:
            f.write(f"  - {token}-USDT\n")

def process_ecosystem(md_dir, output_dir, ecosystem_name, file_patterns):
    """处理特定生态系统的文件"""
    print(f"\n处理 {ecosystem_name} 生态系统...")
    all_tokens = []
    
    for file_pattern in file_patterns:
        file_path = md_dir / file_pattern
        if file_path.exists():
            print(f"正在从 {file_path} 中提取代币...")
            tokens = extract_tokens_from_file(file_path)
            all_tokens.extend(tokens)
        else:
            print(f"文件不存在: {file_path}")
    
    # 去除重复的代币
    unique_tokens = list(dict.fromkeys(all_tokens))
    
    if unique_tokens:
        # 保存为YAML
        output_path = output_dir / f"{ecosystem_name}_ecosystem.yml"
        save_to_yaml(unique_tokens, output_path, ecosystem_name)
        print(f"\n已保存YAML文件: {output_path} (包含 {len(unique_tokens)} 个交易对)")
        
        # 打印找到的所有代币
        print(f"\n{ecosystem_name} 生态系统中找到的代币:")
        for i, token in enumerate(unique_tokens):
            print(f"{i+1}. {token}")
    else:
        print(f"\n未从 {ecosystem_name} 生态系统文件中找到被标记的代币")
    
    return unique_tokens

def main():
    # 设置目录路径
    md_dir = Path("config/gateio_pairs_lists/markdown")
    output_dir = Path("config/gateio_pairs_lists/yaml")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 检查目录是否存在
    if not md_dir.exists():
        print(f"目录不存在: {md_dir}")
        return
    
    print(f"正在从目录 {md_dir} 中查找标记的文件")
    
    # 处理base生态系统
    base_files = ["base_ecosystem_1_ocr.md", "base_ecosystem_2_ocr.md"]
    process_ecosystem(md_dir, output_dir, "base", base_files)
    
    # 处理sol生态系统
    sol_files = ["sol_ecosystem_1_ocr.md", "sol_ecosystem_2_ocr.md", "sol_ecosystem_3_ocr.md", "sol_ecosystem_4_ocr.md"]
    process_ecosystem(md_dir, output_dir, "sol", sol_files)
    
    # 处理bsc生态系统
    bsc_files = ["bsc_ecosystem_1_ocr.md"]
    process_ecosystem(md_dir, output_dir, "bsc", bsc_files)

if __name__ == "__main__":
    main() 