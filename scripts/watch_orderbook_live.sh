#!/bin/bash

# 订单簿数据实时监控 - 清屏版本
# 用途：持续监控订单簿数据，自动刷新显示

# 配置
INTERVAL=${1:-5}  # 刷新间隔（秒），默认5秒
PROJECT_DIR="/Users/alice/Dropbox/投资/量化交易/quants-lab"
DATA_DIR="${PROJECT_DIR}/app/data/raw/orderbook_snapshots"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 检查数据目录
if [ ! -d "$DATA_DIR" ]; then
    echo -e "${RED}❌ 数据目录不存在: $DATA_DIR${NC}"
    exit 1
fi

# 循环监控
while true; do
    # 清屏
    clear
    
    # 标题
    echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}         📊 订单簿数据实时监控 - 每 ${INTERVAL} 秒刷新         ${NC}"
    echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "🕐 当前时间: ${BLUE}$(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo -e "📂 数据目录: ${DATA_DIR}"
    echo ""
    
    # 获取当前时间戳
    NOW=$(date +%s)
    
    # 统计文件
    GATE_COUNT=$(ls -1 "$DATA_DIR"/gate_io_*.parquet 2>/dev/null | wc -l | tr -d ' ')
    MEXC_COUNT=$(ls -1 "$DATA_DIR"/mexc_*.parquet 2>/dev/null | wc -l | tr -d ' ')
    TOTAL_COUNT=$((GATE_COUNT + MEXC_COUNT))
    
    echo -e "${BOLD}📊 数据统计${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "%-15s %d 个文件\n" "Gate.io:" "$GATE_COUNT"
    printf "%-15s %d 个文件\n" "MEXC:" "$MEXC_COUNT"
    printf "%-15s %d 个文件\n" "总计:" "$TOTAL_COUNT"
    
    # 总数据大小
    TOTAL_SIZE=$(du -sh "$DATA_DIR" 2>/dev/null | cut -f1)
    printf "%-15s %s\n" "总大小:" "$TOTAL_SIZE"
    echo ""
    
    # Gate.io 数据
    if [ "$GATE_COUNT" -gt 0 ]; then
        echo -e "${BOLD}${GREEN}✅ Gate.io 数据${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        printf "%-20s %-10s %-12s %s\n" "交易对" "大小" "最新时间" "状态"
        echo "────────────────────────────────────────────────────────────"
        
        for file in "$DATA_DIR"/gate_io_*.parquet; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                pair=$(echo "$filename" | sed 's/gate_io_//' | sed 's/_[0-9]*.parquet//')
                filesize=$(du -h "$file" | cut -f1)
                
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    mtime=$(stat -f %m "$file")
                    mtime_human=$(stat -f "%Sm" -t "%H:%M:%S" "$file")
                else
                    mtime=$(stat -c %Y "$file")
                    mtime_human=$(stat -c "%y" "$file" | cut -d'.' -f1 | cut -d' ' -f2)
                fi
                
                age=$((NOW - mtime))
                
                if [ $age -lt 30 ]; then
                    status="${GREEN}✅ ${age}s 前${NC}"
                elif [ $age -lt 300 ]; then
                    status="${YELLOW}⚠️  ${age}s 前${NC}"
                else
                    minutes=$((age / 60))
                    status="${RED}❌ ${minutes}m 前${NC}"
                fi
                
                printf "%-20s %-10s %-12s " "$pair" "$filesize" "$mtime_human"
                echo -e "$status"
            fi
        done
        echo ""
    fi
    
    # MEXC 数据
    if [ "$MEXC_COUNT" -gt 0 ]; then
        echo -e "${BOLD}${GREEN}✅ MEXC 数据${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        printf "%-20s %-10s %-12s %s\n" "交易对" "大小" "最新时间" "状态"
        echo "────────────────────────────────────────────────────────────"
        
        for file in "$DATA_DIR"/mexc_*.parquet; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                pair=$(echo "$filename" | sed 's/mexc_//' | sed 's/_[0-9]*.parquet//')
                filesize=$(du -h "$file" | cut -f1)
                
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    mtime=$(stat -f %m "$file")
                    mtime_human=$(stat -f "%Sm" -t "%H:%M:%S" "$file")
                else
                    mtime=$(stat -c %Y "$file")
                    mtime_human=$(stat -c "%y" "$file" | cut -d'.' -f1 | cut -d' ' -f2)
                fi
                
                age=$((NOW - mtime))
                
                if [ $age -lt 30 ]; then
                    status="${GREEN}✅ ${age}s 前${NC}"
                elif [ $age -lt 300 ]; then
                    status="${YELLOW}⚠️  ${age}s 前${NC}"
                else
                    minutes=$((age / 60))
                    status="${RED}❌ ${minutes}m 前${NC}"
                fi
                
                printf "%-20s %-10s %-12s " "$pair" "$filesize" "$mtime_human"
                echo -e "$status"
            fi
        done
        echo ""
    fi
    
    # 底部提示
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${YELLOW}提示: 按 Ctrl+C 停止监控 | 刷新间隔: ${INTERVAL} 秒${NC}"
    echo ""
    
    sleep "$INTERVAL"
done

