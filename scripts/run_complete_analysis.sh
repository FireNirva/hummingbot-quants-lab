#!/bin/bash
# Base链CEX-DEX套利分析 - 完整流程一键执行脚本
# 使用方法: bash run_complete_analysis.sh
# 更新于：2025-01-12（支持32个交易对）

set -e  # 遇到错误立即退出

echo "🚀 开始Base链CEX-DEX套利分析完整流程"
echo "="*80
echo "📋 当前配置：32个Base链交易对"
echo "⏱️  预计总时间：40-50分钟"
echo "="*80

# 配置变量
DAYS=5
TIMEFRAME="1m"
CONFIG="config/base_ecosystem_downloader_full.yml"
NETWORK="base"

# 步骤 1：下载CEX历史数据
echo ""
echo "📥 步骤 1/4: 下载CEX历史数据 (${DAYS}天, ${TIMEFRAME}) - 强制刷新"
echo "-"*80
echo "⚠️  注意：此步骤需要在 freqtrade 环境中运行"
conda run -n freqtrade python scripts/import_freqtrade_data.py \
  --config ${CONFIG} \
  --days ${DAYS} \
  --timeframe ${TIMEFRAME} \
  --erase

echo ""
echo "✅ CEX数据下载完成"

# 步骤 2：建立Pool映射
echo ""
echo "🔗 步骤 2/4: 建立CEX-DEX Pool映射"
echo "-"*80
conda run -n quants-lab python scripts/build_pool_mapping.py \
  --network ${NETWORK} \
  --connector gate_io \
  --top-n 3

echo ""
echo "✅ Pool映射完成"

# 步骤 3：下载DEX数据
echo ""
echo "📥 步骤 3/4: 下载DEX历史数据"
echo "-"*80
conda run -n quants-lab python scripts/download_dex_ohlcv.py \
  --network ${NETWORK} \
  --connector gate_io \
  --intervals ${TIMEFRAME} \
  --align-with-cex

echo ""
echo "✅ DEX数据下载完成"

# 步骤 4：运行价差分析
echo ""
echo "📊 步骤 4/4: 运行价差分析"
echo "-"*80
conda run -n quants-lab python scripts/analyze_cex_dex_spread.py \
  --compare-all \
  --interval ${TIMEFRAME} \
  --config ${CONFIG}

echo ""
echo "="*80
echo "🎉 完整流程执行完毕！"
echo ""
echo "📁 数据位置："
echo "  - CEX数据: app/data/cache/candles/gate_io|*|${TIMEFRAME}.parquet"
echo "  - DEX数据: app/data/cache/candles/geckoterminal_base|*|${TIMEFRAME}.parquet"
echo "  - 分析结果: app/data/processed/spread_analysis/"
echo ""
echo "💡 下一步："
echo "  1. 查看分析结果（已在上方显示）"
echo "  2. 可视化分析: python scripts/plot_spread_analysis.py --plot-all --interval ${TIMEFRAME}"
echo "  3. 详细分析某个pair: python scripts/analyze_cex_dex_spread.py --pair IRON-USDT --interval ${TIMEFRAME}"
echo ""

