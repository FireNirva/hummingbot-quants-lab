#!/bin/bash
# 测试不需要 MongoDB 的订单簿采集

echo "================================"
echo "🧪 测试不需要 MongoDB 的任务运行"
echo "================================"
echo ""

# 临时取消 MONGO_URI 环境变量
unset MONGO_URI

echo "✅ 已取消 MONGO_URI 环境变量"
echo ""

# 运行订单簿采集任务
echo "🚀 运行订单簿采集任务（不使用MongoDB）..."
echo ""

conda run -n quants-lab python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml

echo ""
echo "================================"
echo "✅ 测试完成"
echo "================================"

