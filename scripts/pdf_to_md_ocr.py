#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用EasyOCR将PDF截图直接转换为Markdown文档
这个脚本需要安装以下库：
pip install easyocr pdf2image
"""

import os
import sys
from pathlib import Path
import tempfile

try:
    import easyocr
    from pdf2image import convert_from_path
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
        all_text = []
        
        # 对每个图像进行OCR
        for i, image in enumerate(images):
            print(f"正在OCR处理页面 {i+1}/{len(images)}...")
            
            # 保存临时图像文件
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_path = temp_file.name
                image.save(temp_path, 'JPEG')
            
            # 执行OCR
            result = reader.readtext(temp_path)
            
            # 提取文本并保持结构
            page_text = f"## 页面 {i+1}\n\n"
            for _, text, _ in result:
                page_text += text + "\n"
            
            all_text.append(page_text)
            
            # 删除临时文件
            os.unlink(temp_path)
            
        return all_text
    
    except Exception as e:
        print(f"处理PDF时出错: {e}")
        return []

def save_to_markdown(text_pages, output_path, source_file):
    """保存OCR结果为Markdown格式"""
    with open(output_path, 'w', encoding='utf-8') as f:
        # 文档标题
        filename = Path(source_file).stem
        f.write(f"# {filename} OCR结果\n\n")
        f.write(f"源文件: {source_file}\n\n")
        f.write("---\n\n")
        
        # 添加每页内容
        for page in text_pages:
            f.write(page)
            f.write("\n---\n\n")

def main():
    # 输入和输出目录
    input_dir = Path("config/gateio_pairs_lists/screenshot")
    output_dir = Path("config/gateio_pairs_lists/markdown")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化EasyOCR reader（支持英文和中文）
    print("初始化OCR引擎...")
    reader = easyocr.Reader(['en', 'ch_sim'])
    
    # 处理所有PDF文件
    for pdf_file in input_dir.glob("*.pdf"):
        print(f"\n正在处理: {pdf_file.name}")
        
        # 使用OCR处理PDF
        text_pages = process_pdf_with_ocr(pdf_file, reader)
        
        if text_pages:
            # 保存为Markdown
            md_path = output_dir / f"{pdf_file.stem}_ocr.md"
            save_to_markdown(text_pages, md_path, pdf_file)
            print(f"已保存Markdown文件: {md_path} (包含 {len(text_pages)} 页OCR文本)")
        else:
            print(f"未能提取到任何文本，跳过 {pdf_file.name}")

if __name__ == "__main__":
    main() 