#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用EasyOCR从PDF截图中提取交易对信息
这个脚本需要安装以下库：
pip install easyocr pdf2image
"""

import os
import sys
import re
from pathlib import Path
import tempfile
import shutil

try:
    import easyocr
    from pdf2image import convert_from_path
    from PIL import Image
except ImportError:
    print("请安装必要的库: pip install easyocr pdf2image")
    sys.exit(1)

def process_pdf_with_ocr(pdf_path, reader):
    """使用EasyOCR处理PDF"""
    try:
        # 将PDF转换为图像
        print(f"正在将PDF转换为图像: {pdf_path}")
        images = convert_from_path(pdf_path)
        
        # 合并所有文本
        all_text = ""
        
        # 对每个图像进行OCR
        for i, image in enumerate(images):
            print(f"正在OCR处理页面 {i+1}/{len(images)}...")
            
            # 保存临时图像文件
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_path = temp_file.name
                image.save(temp_path, 'JPEG')
            
            # 执行OCR
            result = reader.readtext(temp_path)
            
            # 提取文本
            page_text = ""
            for _, text, _ in result:
                page_text += text + " "
            
            all_text += page_text + "\n\n"
            
            # 删除临时文件
            os.unlink(temp_path)
            
        return all_text
    
    except Exception as e:
        print(f"处理PDF时出错: {e}")
        return ""

def extract_token_pairs(text):
    """从OCR文本中提取代币对信息"""
    # 打印提取到的部分文本进行检查
    print("提取到的文本样例（前300字符）:")
    print(text[:300] + "...")
    
    # 这个正则表达式需要根据实际情况调整
    # 找出符合"大写字母/数字短代码 + 更长的名称"模式的字符串
    token_pattern = re.compile(r'([A-Z0-9]{2,10})\s+([A-Za-z0-9\s]{2,30})')
    matches = token_pattern.findall(text)
    
    # 过滤无效匹配
    tokens = []
    for symbol, name in matches:
        # 确保符号是有效的加密货币符号（通常是2-6个字符）
        if 2 <= len(symbol) <= 10 and 2 <= len(name.strip()) <= 30:
            # 排除常见的无关文本
            if symbol not in ["USD", "GMT", "UTC", "AM", "PM", "ETH", "BTC"] or name.strip() in ["Ethereum", "Bitcoin"]:
                tokens.append((symbol, name.strip()))
    
    # 删除重复项，保持插入顺序
    unique_tokens = []
    seen = set()
    for token in tokens:
        if token[0] not in seen:
            seen.add(token[0])
            unique_tokens.append(token)
    
    return unique_tokens

def manual_input(ecosystem_name):
    """手动输入交易对信息"""
    print("\n自动提取失败或提取结果不理想。")
    print(f"请手动输入{ecosystem_name}生态系统的交易对信息")
    
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
        f.write("| 符号 | 名称 | 交易对 |\n")
        f.write("|------|------|-------|\n")
        
        for symbol, name in tokens:
            symbol = symbol.strip()
            name = name.strip()
            if symbol and name:  # 确保不为空
                trading_pair = f"{symbol}-USDT"
                f.write(f"| {symbol} | {name} | {trading_pair} |\n")

def save_to_yml(tokens, output_path, ecosystem_name):
    """保存为YAML配置文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {ecosystem_name} 生态系统交易对配置\n\n")
        f.write(f"{ecosystem_name}_ecosystem:\n")
        for symbol, _ in tokens:
            symbol = symbol.strip()
            if symbol:  # 确保不为空
                f.write(f"  - {symbol}-USDT\n")

def main():
    # 输入和输出目录
    input_dir = Path("config/gateio_pairs_lists/screenshot")
    output_dir = Path("config/gateio_pairs_lists/markdown")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化EasyOCR reader（仅支持英文以提高速度和准确性）
    print("初始化OCR引擎...")
    reader = easyocr.Reader(['en'])
    
    # 处理所有PDF文件
    for pdf_file in input_dir.glob("*.pdf"):
        print(f"\n正在处理: {pdf_file.name}")
        
        # 确定生态系统名称
        ecosystem_name = pdf_file.stem.split('_')[0]
        
        # 使用OCR处理PDF
        text = process_pdf_with_ocr(pdf_file, reader)
        
        # 提取代币对
        if text:
            tokens = extract_token_pairs(text)
            print(f"自动提取到 {len(tokens)} 个可能的代币对")
            
            # 显示提取结果
            if tokens:
                print("\n提取到的代币对:")
                for i, (symbol, name) in enumerate(tokens):
                    print(f"{i+1}. {symbol}: {name}")
            
            # 询问是否使用自动提取结果或手动输入
            if tokens:
                answer = input("\n是否使用上面的自动提取结果？(y/n): ")
                if answer.lower() != 'y':
                    tokens = manual_input(ecosystem_name)
            else:
                print("未能自动提取到有效的代币对信息")
                answer = input("是否手动输入代币对信息？(y/n): ")
                if answer.lower() == 'y':
                    tokens = manual_input(ecosystem_name)
                else:
                    print(f"跳过 {pdf_file.name}")
                    continue
        else:
            print("OCR处理未能提取到任何文本")
            answer = input("是否手动输入代币对信息？(y/n): ")
            if answer.lower() == 'y':
                tokens = manual_input(ecosystem_name)
            else:
                print(f"跳过 {pdf_file.name}")
                continue
        
        if tokens:
            # 保存为Markdown
            md_path = output_dir / f"{ecosystem_name}_ecosystem.md"
            save_to_markdown(tokens, md_path, ecosystem_name)
            print(f"已保存Markdown文件: {md_path} (包含 {len(tokens)} 个交易对)")
            
            # 保存为YAML配置
            yml_path = output_dir / f"{ecosystem_name}_ecosystem_config.yml"
            save_to_yml(tokens, yml_path, ecosystem_name)
            print(f"已保存YAML配置文件: {yml_path}")
        else:
            print(f"没有代币对信息可保存，跳过 {pdf_file.name}")

if __name__ == "__main__":
    main() 