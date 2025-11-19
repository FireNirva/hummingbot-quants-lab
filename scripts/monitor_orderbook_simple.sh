#!/bin/bash

# 订单簿数据实时监控脚本 - 简化版
# 用途：每隔指定时间检查订单簿数据更新情况

# 配置
INTERVAL=${1:-30}  # 检查间隔（秒），默认30秒
PROJECT_DIR="/Users/alice/Dropbox/投资/量化交易/quants-lab"
DATA_DIR="${PROJECT_DIR}/app/data/raw/orderbook_snapshots"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 订单簿数据监控 - 每 ${INTERVAL} 秒刷新一次"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "按 Ctrl+C 停止监控"
echo ""

# 检查数据目录是否存在
if [ ! -d "$DATA_DIR" ]; then
    echo -e "${RED}❌ 数据目录不存在: $DATA_DIR${NC}"
    exit 1
fi

# 循环监控
while true; do
    # 清屏（可选，注释掉这行可以保留历史记录）
    # clear
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "🕐 检查时间: ${BLUE}$(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # 获取当前时间戳（秒）
    NOW=$(date +%s)
    
    # 统计文件数量
    GATE_COUNT=$(ls -1 "$DATA_DIR"/gate_io_*.parquet 2>/dev/null | wc -l | tr -d ' ')
    MEXC_COUNT=$(ls -1 "$DATA_DIR"/mexc_*.parquet 2>/dev/null | wc -l | tr -d ' ')
    
    echo -e "${BLUE}📂 数据文件统计:${NC}"
    echo "   Gate.io: $GATE_COUNT 个文件"
    echo "   MEXC:    $MEXC_COUNT 个文件"
    echo ""
    
    # 检查 Gate.io 文件
    if [ "$GATE_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✅ Gate.io 数据文件:${NC}"
        for file in "$DATA_DIR"/gate_io_*.parquet; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                pair=$(echo "$filename" | sed 's/gate_io_//' | sed 's/_[0-9]*.parquet//')
                filesize=$(du -h "$file" | cut -f1)
                
                # 获取文件修改时间
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    # macOS
                    mtime=$(stat -f %m "$file")
                    mtime_human=$(stat -f "%Sm" -t "%H:%M:%S" "$file")
                else
                    # Linux
                    mtime=$(stat -c %Y "$file")
                    mtime_human=$(stat -c "%y" "$file" | cut -d'.' -f1 | cut -d' ' -f2)
                fi
                
                # 计算距离现在多少秒
                age=$((NOW - mtime))
                
                # 根据时间差显示不同颜色
                if [ $age -lt 30 ]; then
                    status="${GREEN}✅ 刚刚更新 (${age}秒前)${NC}"
                elif [ $age -lt 300 ]; then
                    status="${YELLOW}⚠️  ${age}秒前${NC}"
                else
                    minutes=$((age / 60))
                    status="${RED}❌ ${minutes}分钟前${NC}"
                fi
                
                echo -e "   ${pair}: ${filesize} | 最新: ${mtime_human} | $status"
            fi
        done
        echo ""
    else
        echo -e "${RED}❌ 没有 Gate.io 数据文件${NC}"
        echo ""
    fi
    
    # 检查 MEXC 文件
    if [ "$MEXC_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✅ MEXC 数据文件:${NC}"
        for file in "$DATA_DIR"/mexc_*.parquet; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                pair=$(echo "$filename" | sed 's/mexc_//' | sed 's/_[0-9]*.parquet//')
                filesize=$(du -h "$file" | cut -f1)
                
                # 获取文件修改时间
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    # macOS
                    mtime=$(stat -f %m "$file")
                    mtime_human=$(stat -f "%Sm" -t "%H:%M:%S" "$file")
                else
                    # Linux
                    mtime=$(stat -c %Y "$file")
                    mtime_human=$(stat -c "%y" "$file" | cut -d'.' -f1 | cut -d' ' -f2)
                fi
                
                # 计算距离现在多少秒
                age=$((NOW - mtime))
                
                # 根据时间差显示不同颜色
                if [ $age -lt 30 ]; then
                    status="${GREEN}✅ 刚刚更新 (${age}秒前)${NC}"
                elif [ $age -lt 300 ]; then
                    status="${YELLOW}⚠️  ${age}秒前${NC}"
                else
                    minutes=$((age / 60))
                    status="${RED}❌ ${minutes}分钟前${NC}"
                fi
                
                echo -e "   ${pair}: ${filesize} | 最新: ${mtime_human} | $status"
            fi
        done
        echo ""
    else
        echo -e "${RED}❌ 没有 MEXC 数据文件${NC}"
        echo ""
    fi
    
    # 显示总数据大小
    TOTAL_SIZE=$(du -sh "$DATA_DIR" 2>/dev/null | cut -f1)
    echo -e "${BLUE}💾 总数据大小: ${TOTAL_SIZE}${NC}"
    echo ""
    
    # 等待指定时间
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏳ 等待 ${INTERVAL} 秒后下次检查..."
    echo ""
    
    sleep "$INTERVAL"
done

