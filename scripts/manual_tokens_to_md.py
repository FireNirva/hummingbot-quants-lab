#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
手动输入代币对信息并保存为Markdown格式
这个脚本不依赖任何第三方库
"""

import os
from pathlib import Path

def save_to_markdown(tokens, output_path, ecosystem_name):
    """保存为Markdown格式"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {ecosystem_name} 生态系统代币\n\n")
        f.write("| 符号 | 名称 | 交易对 |\n")
        f.write("|------|------|-------|\n")
        
        for symbol, name in tokens:
            symbol = symbol.strip()
            name = name.strip()
            if symbol and name:  # 确保不为空
                trading_pair = f"{symbol}-USDT"
                f.write(f"| {symbol} | {name} | {trading_pair} |\n")

def manual_input(ecosystem_name):
    """手动输入交易对信息"""
    tokens = []
    print(f"\n开始为 {ecosystem_name} 生态系统输入代币信息")
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

def main():
    # 创建输出目录
    output_dir = Path("config/gateio_pairs_lists/markdown")
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的生态系统
    ecosystems = ["base", "sol", "bsc", "eth"]
    
    for ecosystem in ecosystems:
        # 询问是否输入该生态系统的代币
        answer = input(f"是否输入 {ecosystem} 生态系统的代币信息？(y/n): ")
        if answer.lower() != 'y':
            continue
            
        # 手动输入代币信息
        tokens = manual_input(ecosystem)
        
        if tokens:
            # 保存为Markdown
            output_path = output_dir / f"{ecosystem}_ecosystem.md"
            save_to_markdown(tokens, output_path, ecosystem)
            print(f"已保存: {output_path} (包含 {len(tokens)} 个交易对)")
            
            # 生成交易对列表的配置片段
            config_path = output_dir / f"{ecosystem}_ecosystem_config.yml"
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(f"# {ecosystem} 生态系统交易对配置\n\n")
                f.write(f"{ecosystem}_ecosystem:\n")
                for symbol, _ in tokens:
                    f.write(f"  - {symbol}-USDT\n")
            print(f"已生成配置文件: {config_path}")
        else:
            print(f"未输入任何 {ecosystem} 生态系统的代币信息")

if __name__ == "__main__":
    main() 