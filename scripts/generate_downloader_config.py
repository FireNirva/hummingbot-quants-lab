#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成下载器配置YAML文件
这个脚本读取生态系统的交易对YAML文件，然后生成完整的下载器配置YAML文件，
不使用!include指令
"""

import os
import sys
import yaml
from pathlib import Path

def load_ecosystem_trading_pairs(ecosystem_file):
    """加载生态系统交易对列表"""
    try:
        with open(ecosystem_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
            # 检查YAML文件格式
            key = f"{Path(ecosystem_file).stem.split('_')[0]}_ecosystem"
            if key in data and isinstance(data[key], list):
                return data[key]
            else:
                print(f"错误: 在 {ecosystem_file} 中未找到有效的 {key} 列表")
                return []
    except Exception as e:
        print(f"加载 {ecosystem_file} 时出错: {e}")
        return []

def generate_downloader_config(ecosystem_name, trading_pairs, output_file):
    """生成下载器配置文件"""
    config = {
        'tasks': {
            f'gateio_{ecosystem_name}_ecosystem_downloader': {
                'enabled': True,
                'task_class': 'tasks.data_collection.simple_candles_downloader.SimpleCandlesDownloader',
                'frequency_hours': 24,
                'config': {
                    'connector_name': 'gateio',
                    'trading_pairs': trading_pairs,
                    'intervals': ['1h'],
                    'days_data_retention': 30,
                    'timescale_config': {
                        'db_host': 'timescaledb',
                        'db_port': 5432,
                        'db_user': 'admin',
                        'db_password': 'admin',
                        'db_name': 'timescaledb'
                    }
                }
            }
        }
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # 使用safe_dump而不是dump，可以避免一些不必要的YAML格式和样式问题
            yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"成功生成配置文件: {output_file}")
    except Exception as e:
        print(f"保存配置文件时出错: {e}")

def generate_multi_ecosystem_config(ecosystems, output_file):
    """生成多生态系统下载器配置文件"""
    tasks = {}
    
    for ecosystem_name, trading_pairs in ecosystems.items():
        if trading_pairs:
            tasks[f'gateio_{ecosystem_name}_ecosystem_downloader'] = {
                'enabled': True,
                'task_class': 'tasks.data_collection.simple_candles_downloader.SimpleCandlesDownloader',
                'frequency_hours': 24,
                'config': {
                    'connector_name': 'gateio',
                    'trading_pairs': trading_pairs,
                    'intervals': ['1h'],
                    'days_data_retention': 30,
                    'timescale_config': {
                        'db_host': 'timescaledb',
                        'db_port': 5432,
                        'db_user': 'admin',
                        'db_password': 'admin',
                        'db_name': 'timescaledb'
                    }
                }
            }
    
    config = {'tasks': tasks}
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"成功生成多生态系统配置文件: {output_file}")
    except Exception as e:
        print(f"保存配置文件时出错: {e}")

def main():
    # 设置目录和文件路径
    yaml_dir = Path('config/gateio_pairs_lists/yaml')
    config_dir = Path('config')
    
    # 确保输出目录存在
    os.makedirs(config_dir, exist_ok=True)
    
    # 生成单个生态系统配置
    ecosystems = ['base', 'sol', 'bsc']
    all_ecosystems = {}
    
    for ecosystem in ecosystems:
        ecosystem_file = yaml_dir / f'{ecosystem}_ecosystem.yml'
        if ecosystem_file.exists():
            print(f"处理 {ecosystem} 生态系统...")
            trading_pairs = load_ecosystem_trading_pairs(ecosystem_file)
            
            if trading_pairs:
                # 保存单个生态系统配置
                output_file = config_dir / f'{ecosystem}_ecosystem_downloader_full.yml'
                generate_downloader_config(ecosystem, trading_pairs, output_file)
                
                # 添加到多生态系统配置中
                all_ecosystems[ecosystem] = trading_pairs
            else:
                print(f"跳过 {ecosystem} 生态系统，未找到交易对")
        else:
            print(f"跳过 {ecosystem} 生态系统，文件不存在: {ecosystem_file}")
    
    # 生成多生态系统配置
    if all_ecosystems:
        multi_output_file = config_dir / 'multi_ecosystem_downloader_full.yml'
        generate_multi_ecosystem_config(all_ecosystems, multi_output_file)
    else:
        print("未找到任何生态系统数据，无法生成多生态系统配置")

if __name__ == '__main__':
    main() 