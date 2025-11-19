#!/bin/bash
# 演示无 MongoDB 模式的订单簿采集

cat << 'EOF'

================================================================================
🎯 无 MongoDB 模式演示
================================================================================

本演示将展示如何在不需要 MongoDB 的情况下运行订单簿采集任务。

EOF

echo "1️⃣  检查当前环境"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -z "$MONGO_URI" ]; then
    echo "✅ MONGO_URI: 未设置 (将使用 NoOpTaskStorage)"
else
    echo "📌 MONGO_URI: $MONGO_URI"
    echo "   如需测试无 MongoDB 模式，请运行: unset MONGO_URI"
fi

echo ""
echo "2️⃣  准备运行任务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "配置文件: config/orderbook_snapshot_gateio.yml"
echo "任务类型: OrderBookSnapshotTask"
echo "数据输出: app/data/raw/orderbook_snapshots/"
echo ""

cat << 'EOF'
3️⃣  运行选项
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

选项 A: 无 MongoDB 模式 (推荐用于本地开发)
   unset MONGO_URI
   python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml

选项 B: 有 MongoDB 模式 (推荐用于生产环境)
   export MONGO_URI="mongodb://admin:admin@localhost:27017"
   python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml

选项 C: Docker 模式 (自动使用 MongoDB)
   make run-tasks config=orderbook_snapshot_gateio.yml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 提示:
   - 无 MongoDB 模式不会记录任务执行历史
   - 但数据采集功能完全正常
   - Parquet 文件照常写入
   - 适合本地开发和测试

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

要查看更多信息，请参阅: docs/NO_MONGODB_MODE.md

================================================================================

EOF

