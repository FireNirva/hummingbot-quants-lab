#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from pathlib import Path

print("开始执行提取脚本...")

# 设置文件路径
base_ecosystem_1 = Path("config/gateio_pairs_lists/markdown/base_ecosystem_1_ocr.md")
base_ecosystem_2 = Path("config/gateio_pairs_lists/markdown/base_ecosystem_2_ocr.md")
output_file = Path("config/gateio_pairs_lists/yaml/base_ecosystem.yml")

# 确保输出目录存在
os.makedirs(output_file.parent, exist_ok=True)

all_tokens = []

# 尝试提取第一个文件中的代币
print(f"尝试读取文件: {base_ecosystem_1}")
if base_ecosystem_1.exists():
    try:
        with open(base_ecosystem_1, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"成功读取文件，长度: {len(content)} 字符")
            
            token_pattern = re.compile(r'\*([A-Z0-9]+)\*')
            matches = token_pattern.findall(content)
            
            print(f"在文件1中找到了 {len(matches)} 个标记的代币:")
            for token in matches:
                print(f" - {token}")
                all_tokens.append(token)
    except Exception as e:
        print(f"读取文件1时出错: {e}")
else:
    print(f"文件不存在: {base_ecosystem_1}")

# 尝试提取第二个文件中的代币
print(f"\n尝试读取文件: {base_ecosystem_2}")
if base_ecosystem_2.exists():
    try:
        with open(base_ecosystem_2, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"成功读取文件，长度: {len(content)} 字符")
            
            token_pattern = re.compile(r'\*([A-Z0-9]+)\*')
            matches = token_pattern.findall(content)
            
            print(f"在文件2中找到了 {len(matches)} 个标记的代币:")
            for token in matches:
                print(f" - {token}")
                all_tokens.append(token)
    except Exception as e:
        print(f"读取文件2时出错: {e}")
else:
    print(f"文件不存在: {base_ecosystem_2}")

# 去除重复
unique_tokens = list(dict.fromkeys(all_tokens))

# 保存为YAML
print(f"\n保存YAML文件: {output_file}")
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# base 生态系统交易对配置\n\n")
        f.write("base_ecosystem:\n")
        
        for token in unique_tokens:
            f.write(f"  - {token}-USDT\n")
        
        print(f"成功保存 {len(unique_tokens)} 个交易对到YAML文件")
except Exception as e:
    print(f"保存YAML文件时出错: {e}")

print("\nbase 生态系统代币列表:")
for i, token in enumerate(unique_tokens):
    print(f"{i+1}. {token}")

print("\n脚本执行完毕") 