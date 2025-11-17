#!/bin/bash
# 方案B：清理配置文件并重新开始

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧹 清理配置文件并重新开始"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 正在备份原配置文件..."
cp config/base_ecosystem_downloader_full.yml config/base_ecosystem_downloader_full.yml.backup
echo "✅ 备份完成: config/base_ecosystem_downloader_full.yml.backup"
echo ""

echo "📝 正在创建清理后的配置文件（仅包含Gate.io上架的24个币种）..."
cat > config/base_ecosystem_downloader_full.yml << 'EOFCONFIG'
# Gate.io Base 生态代币数据收集配置（清理版本）
# 仅包含在Gate.io上架的交易对
# 更新于：2025-01-12

tasks:
  gateio_base_ecosystem_downloader:
    enabled: true
    task_class: app.tasks.data_collection.simple_candles_downloader.SimpleCandlesDownloader
    
    schedule:
      type: frequency
      frequency_hours: 0.25
      timezone: UTC
    
    max_retries: 3
    retry_delay_seconds: 60
    timeout_seconds: 600
    
    config:
      connector_name: "gate_io"
      
      # 仅包含Gate.io上架的24个交易对
      trading_pairs:
        # 保留的高评分币种（Gate.io已上架）
        - "IRON-USDT"      # 评分299.1 ✅
        - "VIRTUAL-USDT"   # 评分233.6 ✅
        - "MIGGLES-USDT"   # 评分185.4 ✅
        - "BENJI-USDT"     # 评分138.0 ✅
        - "AERO-USDT"      # 高流动性 ✅
        
        # Gate.io已上架的币种
        - "AIXBT-USDT"
        - "BRETT-USDT"
        - "EDGE-USDT"
        - "FAI-USDT"
        - "HINT-USDT"
        - "UNITE-USDT"
        - "TALENT-USDT"
        
        # 额外发现的Gate.io上架币种
        - "SOL-USDT"
        - "MIRROR-USDT"
        - "SKOP-USDT"
        - "GMRT-USDT"
        - "GPS-USDT"
        - "XSWAP-USDT"
        - "ZORA-USDT"
        - "LVLY-USDT"
        - "COOKIE-USDT"
        - "TRC-USDT"
        - "ZAP-USDT"
        - "AWS-USDT"
      
      intervals:
        - "1m"
      
      days_data_retention: 0.6
    
    tags:
      - data_collection
      - candles
      - gate_io
      - base_ecosystem
EOFCONFIG

echo "✅ 配置文件已更新！（从31个减少到24个交易对）"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 开始完整流程（1-4步骤）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

bash run_complete_analysis.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 完成！配置文件已清理，分析已完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 注意："
echo "  - 原配置已备份到: config/base_ecosystem_downloader_full.yml.backup"
echo "  - 如需恢复: mv config/base_ecosystem_downloader_full.yml.backup config/base_ecosystem_downloader_full.yml"
echo ""

