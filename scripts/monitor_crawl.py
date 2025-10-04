#!/usr/bin/env python3
"""
监控OKX文档爬取进度
"""

import time
import json
from pathlib import Path
import os

def monitor_crawl():
    """监控爬取进度"""
    output_dir = Path("data/okx_docs")
    stats_file = output_dir / "crawl_stats.json"
    
    print("🔍 监控OKX文档爬取进度...")
    print(f"📁 输出目录: {output_dir}")
    print("=" * 60)
    
    last_count = 0
    start_time = time.time()
    
    while True:
        try:
            # 统计已生成的文件
            if output_dir.exists():
                md_files = list(output_dir.rglob("*.md"))
                json_files = list(output_dir.rglob("*.json"))
                
                current_count = len(md_files)
                
                # 显示进度
                elapsed = time.time() - start_time
                if current_count > last_count:
                    print(f"⏰ {time.strftime('%H:%M:%S')} | 📄 已爬取: {current_count} 页面 | ⏱️ 用时: {elapsed:.0f}秒")
                    last_count = current_count
                
                # 显示最新文件
                if md_files:
                    latest_file = max(md_files, key=lambda f: f.stat().st_mtime)
                    print(f"📝 最新文件: {latest_file.name}")
                
                # 检查统计文件
                if stats_file.exists():
                    try:
                        with open(stats_file, 'r', encoding='utf-8') as f:
                            stats = json.load(f)
                        
                        print(f"📊 统计信息:")
                        print(f"   - 成功: {stats.get('total_crawled', 0)} 页面")
                        print(f"   - 失败: {stats.get('total_failed', 0)} 页面")
                        print(f"   - 成功率: {stats.get('success_rate', 0):.1f}%")
                        
                        if stats.get('total_crawled', 0) > 0:
                            print("🎉 爬取已完成!")
                            break
                            
                    except Exception as e:
                        print(f"⚠️ 读取统计文件失败: {e}")
                
            else:
                print("📁 等待输出目录创建...")
                
        except KeyboardInterrupt:
            print("\n⏹️ 监控已停止")
            break
        except Exception as e:
            print(f"❌ 监控出错: {e}")
            
        time.sleep(10)  # 每10秒检查一次
    
    # 显示最终结果
    if output_dir.exists():
        md_files = list(output_dir.rglob("*.md"))
        print(f"\n📋 最终结果:")
        print(f"   - 总文件数: {len(md_files)}")
        print(f"   - 输出目录: {output_dir}")
        
        # 显示文件列表
        if md_files:
            print(f"\n📄 生成的文档:")
            for i, file in enumerate(md_files[:10], 1):  # 显示前10个
                size = file.stat().st_size
                print(f"   {i:2d}. {file.name} ({size} bytes)")
            
            if len(md_files) > 10:
                print(f"   ... 还有 {len(md_files) - 10} 个文件")

if __name__ == "__main__":
    monitor_crawl() 