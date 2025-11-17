#!/bin/bash
# 查看订单簿采集任务状态

echo "🔍 订单簿采集任务状态"
echo "=" * 80
echo ""

# 查找所有相关进程
PIDS=$(ps aux | grep -E "cli.py run-tasks.*orderbook_snapshot" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "❌ 没有运行中的订单簿采集任务"
    echo ""
    echo "💡 启动方法："
    echo "   # Gate.io"
    echo "   python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &"
    echo ""
    echo "   # MEXC"
    echo "   python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml &"
    echo ""
    exit 0
fi

# 显示运行中的任务
echo "✅ 找到 $(echo $PIDS | wc -w | tr -d ' ') 个运行中的任务："
echo ""

ps aux | grep -E "cli.py run-tasks.*orderbook_snapshot" | grep -v grep | while read line; do
    PID=$(echo $line | awk '{print $2}')
    CPU=$(echo $line | awk '{print $3}')
    MEM=$(echo $line | awk '{print $4}')
    TIME=$(echo $line | awk '{print $10}')
    CMD=$(echo $line | awk '{for(i=11;i<=NF;i++) printf "%s ", $i; print ""}')
    
    # 提取配置文件名
    CONFIG=$(echo $CMD | sed -n 's/.*--config \([^ ]*\).*/\1/p')
    
    echo "📋 任务详情："
    echo "   PID:    $PID"
    echo "   CPU:    $CPU%"
    echo "   内存:   $MEM%"
    echo "   运行时长: $TIME"
    echo "   配置:   $CONFIG"
    echo ""
done

echo "=" * 80
echo ""
echo "💡 管理命令："
echo "   • 查看数据: python scripts/check_realtime_orderbook.py"
echo "   • 停止任务: bash scripts/stop_all_orderbook.sh"
echo "   • 重启任务: bash scripts/restart_orderbook_gateio.sh"
echo ""

