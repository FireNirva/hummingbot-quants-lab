#!/bin/bash
# MEXC 交易所 Base 生态代币 CEX-DEX 套利分析完整流程
# 用于下载和分析在 Gate.io 不可用但在 MEXC 可交易的交易对

set -e  # 遇到错误立即退出

# ============================================================================
# 配置参数
# ============================================================================
NETWORK="base"
CONNECTOR="mexc"
DAYS=5  # MEXC 数据下载天数
TIMEFRAME="1m"
CONFIG_FILE="config/mexc_base_ecosystem_downloader.yml"

# ============================================================================
# 颜色输出
# ============================================================================
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  MEXC 交易所 Base 生态代币 CEX-DEX 套利分析"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${NC}"

echo -e "${GREEN}📋 配置信息：${NC}"
echo "  • 交易所: ${CONNECTOR}"
echo "  • 网络: ${NETWORK}"
echo "  • 时间周期: ${TIMEFRAME}"
echo "  • 下载天数: ${DAYS}"
echo "  • 配置文件: ${CONFIG_FILE}"
echo ""

# ============================================================================
# 步骤 1: 检查 Freqtrade 对 MEXC 的支持
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}步骤 1/5: 检查 Freqtrade 对 MEXC 的支持${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 先尝试激活 freqtrade 环境并测试
echo -e "${YELLOW}⚠️  请确保已激活 freqtrade 环境：${NC}"
echo "   conda activate freqtrade"
echo ""
read -p "是否已激活 freqtrade 环境？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ 请先激活 freqtrade 环境，然后重新运行此脚本${NC}"
    exit 1
fi

python scripts/test_mexc_support.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ MEXC 支持检查失败，请查看上述错误信息${NC}"
    read -p "是否继续执行（可能会失败）？(y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# ============================================================================
# 步骤 2: 下载 CEX 数据 (MEXC)
# ============================================================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}步骤 2/5: 下载 MEXC CEX 数据${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo "正在下载 ${DAYS} 天的 ${TIMEFRAME} 数据..."
python scripts/import_freqtrade_data.py \
    --config ${CONFIG_FILE} \
    --days ${DAYS} \
    --timeframe ${TIMEFRAME} \
    --erase

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ CEX 数据下载失败${NC}"
    exit 1
fi

echo -e "${GREEN}✅ CEX 数据下载完成${NC}"

# ============================================================================
# 步骤 3: 切换到 quants-lab 环境
# ============================================================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}步骤 3/5: 切换环境并生成池子映射${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${YELLOW}⚠️  现在需要切换到 quants-lab 环境${NC}"
echo "   请退出当前脚本，运行以下命令："
echo ""
echo -e "${BLUE}   conda activate quants-lab${NC}"
echo -e "${BLUE}   bash run_mexc_analysis.sh${NC}"
echo ""
echo "或者，如果已在 quants-lab 环境中，按 y 继续..."
read -p "是否已在 quants-lab 环境？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}请切换环境后重新运行此脚本${NC}"
    exit 0
fi

# ============================================================================
# 步骤 4: 生成池子映射
# ============================================================================
echo "正在生成 DEX 池子映射..."
python scripts/build_pool_mapping.py \
    --network ${NETWORK} \
    --connector ${CONNECTOR}

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 池子映射生成失败${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 池子映射生成完成${NC}"

# ============================================================================
# 步骤 5: 下载 DEX 数据
# ============================================================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}步骤 4/5: 下载 DEX 数据${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo "正在下载 DEX OHLCV 数据..."
python scripts/download_dex_ohlcv.py \
    --network ${NETWORK} \
    --connector ${CONNECTOR} \
    --intervals ${TIMEFRAME} \
    --align-with-cex

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ DEX 数据下载失败${NC}"
    exit 1
fi

echo -e "${GREEN}✅ DEX 数据下载完成${NC}"

# ============================================================================
# 步骤 6: 运行价差分析
# ============================================================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}步骤 5/5: 运行价差分析${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo "正在分析 CEX-DEX 价差..."
python scripts/analyze_cex_dex_spread.py \
    --network ${NETWORK} \
    --connector ${CONNECTOR} \
    --interval ${TIMEFRAME}

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 价差分析失败${NC}"
    exit 1
fi

# ============================================================================
# 完成
# ============================================================================
echo ""
echo -e "${GREEN}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ MEXC 数据下载和分析完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${NC}"

echo "📊 分析结果已保存到："
echo "  • CEX 数据: app/data/raw/candles/${CONNECTOR}/"
echo "  • DEX 数据: app/data/raw/candles/geckoterminal/"
echo "  • 价差分析: app/data/processed/spread_analysis/"
echo ""

