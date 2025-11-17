#!/bin/bash
# 一键停止所有订单簿采集任务（无需确认）

echo "🔍 查找正在运行的订单簿采集任务..."

# 查找所有相关进程
PIDS=$(ps aux | grep -E "cli.py run-tasks.*orderbook_snapshot" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "✅ 没有发现正在运行的订单簿采集任务"
    exit 0
fi

echo "🛑 正在停止 $(echo $PIDS | wc -w | tr -d ' ') 个任务..."
echo ""

for PID in $PIDS; do
    CMD=$(ps -p $PID -o command= 2>/dev/null | sed 's/python cli.py run-tasks --config //')
    echo "   • 停止 PID $PID: $CMD"
    kill $PID 2>/dev/null
done

# 等待进程结束
sleep 2

# 强制停止仍在运行的进程
for PID in $PIDS; do
    if ps -p $PID > /dev/null 2>&1; then
        echo "   • 强制停止 PID $PID"
        kill -9 $PID 2>/dev/null
    fi
done

echo ""
echo "✅ 所有订单簿采集任务已停止"

