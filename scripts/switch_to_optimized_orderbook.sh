#!/bin/bash
# 切换到优化版本的订单簿采集（只采集高流动性币种）

echo "🔄 切换到优化版本的订单簿采集..."
echo ""

# 1. 停止当前任务
echo "1️⃣ 停止当前任务..."
bash scripts/stop_all_orderbook.sh
echo ""

# 2. 等待进程完全停止
echo "2️⃣ 等待进程停止..."
sleep 3
echo ""

# 3. 启动优化版本
echo "3️⃣ 启动优化版本（只采集高流动性币种）..."
echo ""
echo "   采集币种:"
echo "   • VIRTUAL-USDT  (⭐⭐⭐⭐ 高流动性)"
echo "   • BNKR-USDT     (⭐⭐ 中高流动性)"
echo "   • MIGGLES-USDT  (⭐⭐ 中高流动性)"
echo ""

cd /Users/alice/Dropbox/投资/量化交易/quants-lab
python cli.py run-tasks --config config/orderbook_snapshot_gateio_optimized.yml &

# 4. 等待启动
sleep 5
echo ""

# 5. 验证
echo "4️⃣ 验证任务状态..."
bash scripts/status_orderbook_tasks.sh

echo ""
echo "✅ 切换完成！"
echo ""
echo "💡 预期效果:"
echo "   • 重复率从 30.4% 降低到 1.3%"
echo "   • 存储效率从 69.6% 提升到 98.7%"
echo "   • 数据质量显著提升"
echo ""
echo "📊 监控命令:"
echo "   python scripts/monitor_orderbook_liquidity.py"
echo ""

