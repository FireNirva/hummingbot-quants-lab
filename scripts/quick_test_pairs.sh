#!/bin/bash
# 快速测试几个失败的币种，看是否真的在Gate.io上存在

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 快速测试失败的交易对（测试3个样本）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 测试3个代表性币种
test_pairs=("DEGEN/USDT" "CLANKER/USDT" "PAAL/USDT")
test_days=(7 5 3 1)

for pair in "${test_pairs[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 测试: $pair"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    for days in "${test_days[@]}"; do
        echo ""
        echo "⏱️  尝试下载 $days 天数据..."
        
        # 使用freqtrade环境测试
        if conda run -n freqtrade freqtrade download-data \
            --exchange gateio \
            --timeframe 1m \
            --days $days \
            --pairs "$pair" 2>&1 | grep -q "Downloading"; then
            
            echo "✅ 成功！$pair 可以下载 $days 天数据"
            break
        else
            echo "❌ 失败：$days 天太长或币种不存在"
        fi
    done
    echo ""
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 结论："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "如果上面的测试都失败了，说明这些币种："
echo "  1. ❌ 不在Gate.io现货市场（可能只在合约市场）"
echo "  2. ⏱️  上市时间太短（少于1天）"
echo "  3. 🔤 交易对名称不匹配"
echo ""
echo "如果有部分成功，建议："
echo "  • 减少下载天数（从7天改为3天或更少）"
echo "  • 或等待几天后再下载"
echo ""

