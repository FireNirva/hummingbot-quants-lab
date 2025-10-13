# CEX-DEX 价差分析指南

## 📖 概述

本文档介绍如何使用 QuantsLab 的 CEX-DEX 价差分析系统进行套利机会评估。

### 核心理念

**问题**: DEX 数据稀疏（仅在有交易时有数据），直接对比 CEX-DEX 价格会导致图表中断和统计偏差。

**解决方案**: 双模式分析
1. **连续时间轴分析**（含补全）：宏观观测价差趋势
2. **事件时间分析**（仅实际交易）：评估真实可执行机会

---

## 🔧 数据补全机制

### Forward-Fill 策略

对于 DEX 数据缺失的时间点：
- **价格**: 使用前一根蜡烛的 `close` 填充 `open/high/low/close`
- **成交量**: 设为 `0`
- **标记**: 添加 `is_filled` 列标识补全数据

### 补全的合理性

✅ **优点**:
- 形成连续时间轴，便于趋势观测
- 可以计算持续性指标
- 便于绘制完整图表

⚠️ **注意事项**:
- 补全后的价差是"名义差值"
- DEX 无交易说明该价差无法即时套利
- **补全数据不应参与回测**
- 需要叠加流动性/成交量过滤

---

## 📊 分析模式对比

| 特性 | 模式1: 连续时间轴 | 模式2: 事件时间 |
|-----|------------------|---------------|
| **数据范围** | 全部时间点（含补全） | 仅 DEX 实际交易 |
| **用途** | 宏观趋势观测 | 评估真实机会 |
| **价差统计** | 名义套利空间 | 可执行套利机会 |
| **回测适用** | ❌ 不适用 | ✅ 适用 |
| **可视化** | 连续曲线 | 散点图 |

---

## 🚀 快速开始

### 1. 单交易对分析

```bash
# 分析 AERO-USDT 的价差
python scripts/analyze_cex_dex_spread.py \
  --pair AERO-USDT \
  --interval 1m \
  --volume-threshold 100
```

**输出**:
- 双模式统计对比
- 成交量过滤分析
- 时间分布分析
- 保存价差数据到 `app/data/processed/spread_analysis/spread_analysis_*.parquet`
- 保存图表到 `app/data/processed/plots/`

### 2. 多交易对对比

```bash
# 对比所有交易对的套利潜力
python scripts/analyze_cex_dex_spread.py --compare-all
```

**输出**:
- 覆盖率对比
- 平均价差对比
- 可执行机会数量
- 综合评分排序

### 3. 可视化（可选）

```bash
# 需要先安装 matplotlib
conda install -n quants-lab matplotlib

# 生成图表
python scripts/plot_spread_analysis.py \
  --pair AERO-USDT \
  --interval 1m
```

**生成图表**:
1. 价差时序图（双曲线 + 成交量）
2. 价差分布直方图（补全 vs 实际）
3. 流动性-价差散点图

**保存位置**: `app/data/processed/plots/`

---

## 📈 分析结果解读

### 示例: AERO-USDT (1m)

#### 模式 1: 连续时间轴（含补全）

```
数据点数: 14,697
平均价差: -0.11%
名义套利机会:
  CEX→DEX: 272 次 (1.85%)
  DEX→CEX: 1,627 次 (11.07%)
```

💡 **解读**: 
- 大部分时间 DEX 价格略低于 CEX (-0.11%)
- 名义上看，DEX→CEX 套利机会更多
- **但需要验证这些时刻 DEX 是否有实际流动性**

#### 模式 2: 事件时间（仅实际交易）

```
数据点数: 12,135 (实际交易)
平均价差: -0.09%
可执行套利机会:
  CEX→DEX: 248 次 (2.04%)
  DEX→CEX: 1,406 次 (11.59%)
```

💡 **解读**:
- 82.57% 的时间有实际交易
- 可执行机会比名义机会略少（排除了无交易时段）
- 这些才是真正可以执行的套利机会

#### 成交量过滤（阈值: $100）

```
满足成交量阈值: 5,513 / 12,135 次 (45.43%)
高流动性套利机会:
  CEX→DEX: 236 次
  DEX→CEX: 641 次
```

💡 **解读**:
- 只有 45% 的实际交易满足最低流动性要求
- 高流动性套利机会进一步减少
- **这些是最有价值的套利机会**

---

## 💡 套利策略建议

### 1. 筛选标准

**必须满足**:
- ✅ `is_filled == False` (有实际交易)
- ✅ `dex_volume >= threshold` (满足流动性)
- ✅ `abs(price_diff_pct) >= 0.5%` (价差足够)

**额外考虑**:
- Gas 费成本（Base 链较低，约 $0.05-0.2）
- 滑点影响（流动性越大越好）
- 执行延迟（1-2 分钟确认时间）

### 2. 交易对选择

基于综合评分:

| 排名 | 交易对 | 覆盖率 | 平均价差 | 可执行机会 | 总成交量 | 推荐度 |
|-----|-------|--------|----------|-----------|---------|-------|
| 1 | **VIRTUAL-USDT** | 21.1% | 1.16% | 1,791 | $4.7M | ⭐⭐⭐⭐⭐ |
| 2 | **AERO-USDT** | 82.6% | 0.36% | 1,654 | $108M | ⭐⭐⭐⭐⭐ |
| 3 | GPS-USDT | 3.2% | 2.65% | 401 | $36K | ⭐⭐⭐ |
| 4 | BRETT-USDT | 5.9% | 2.50% | 223 | $418K | ⭐⭐ |

**建议**:
- **主力**: AERO-USDT（流动性最高，稳定）
- **辅助**: VIRTUAL-USDT（价差大，但需要等待时机）
- **观察**: GPS, BRETT（流动性较低）

### 3. 时间窗口优化

```
最活跃时段: 21:00 UTC (北京时间 5:00)
最大成交量时段: 21:00 UTC
平均价差最大: 21:00 UTC
```

💡 **策略**: 在活跃时段重点监控，成交量大且价差大的时刻执行。

---

## 🔬 高级分析

### 1. 读取价差数据

```python
import pandas as pd
from core.data_paths import data_paths

# 加载价差数据
spread_df = pd.read_parquet(
    data_paths.spread_analysis_dir / "spread_analysis_AERO-USDT_1m.parquet"
)

# 筛选可执行机会
executable = spread_df[
    (~spread_df['dex_is_filled']) &
    (spread_df['dex_volume'] >= 100) &
    (spread_df['price_diff_pct'].abs() >= 0.5)
]

print(f"可执行套利机会: {len(executable)} 次")
```

### 2. 回测示例

```python
# 仅使用实际交易数据
backtest_data = spread_df[~spread_df['dex_is_filled']].copy()

# 模拟套利策略
def simulate_arbitrage(row, gas_fee=0.1):
    """
    简单套利模拟
    
    Args:
        row: 价差数据行
        gas_fee: Gas 费成本 (USD)
    
    Returns:
        profit: 利润 (%)
    """
    spread_pct = abs(row['price_diff_pct'])
    
    # 扣除 Gas 费（假设交易 $1000）
    trade_size = 1000
    gas_cost_pct = (gas_fee / trade_size) * 100
    
    # 扣除滑点（假设 0.1%）
    slippage_pct = 0.1
    
    # 净利润
    net_profit = spread_pct - gas_cost_pct - slippage_pct
    
    return net_profit if net_profit > 0 else 0

backtest_data['profit'] = backtest_data.apply(simulate_arbitrage, axis=1)

total_profit = backtest_data['profit'].sum()
positive_trades = (backtest_data['profit'] > 0).sum()

print(f"总利润: {total_profit:.2f}%")
print(f"盈利交易: {positive_trades} / {len(backtest_data)}")
```

### 3. 价差持续性分析

```python
# 计算价差持续时长
def calculate_spread_duration(spread_df, threshold=0.5):
    """计算价差超过阈值的持续时长"""
    
    # 仅实际交易
    real = spread_df[~spread_df['dex_is_filled']].copy()
    
    # 标记超阈值
    real['above_threshold'] = real['price_diff_pct'].abs() >= threshold
    
    # 计算连续持续时长
    real['duration_group'] = (
        real['above_threshold'] != real['above_threshold'].shift()
    ).cumsum()
    
    durations = real[real['above_threshold']].groupby('duration_group').size()
    
    return durations

durations = calculate_spread_duration(spread_df)

print(f"平均持续时长: {durations.mean():.1f} 分钟")
print(f"最长持续: {durations.max()} 分钟")
```

---

## 📝 最佳实践

### ✅ DO

1. **始终区分补全数据和实际交易数据**
   - 使用 `is_filled` 列过滤
   - 回测时只用 `is_filled == False` 的数据

2. **应用成交量过滤**
   - 设置合理的流动性阈值
   - 考虑滑点影响

3. **双模式分析**
   - 连续时间轴：了解整体趋势
   - 事件时间：评估实际机会

4. **考虑交易成本**
   - Gas 费
   - 滑点
   - 延迟风险

### ❌ DON'T

1. **不要直接用补全数据回测**
   - 会高估套利机会
   - 会低估执行难度

2. **不要忽略流动性**
   - 价差大但无流动性 = 无法执行
   - 必须验证 `dex_volume > 0`

3. **不要假设所有价差都可套利**
   - 考虑确认时间（1-2分钟）
   - 价差可能瞬间消失

---

## 🛠️ 工具脚本

| 脚本 | 功能 | 用途 |
|-----|------|------|
| `analyze_cex_dex_spread.py` | 价差分析 | 统计、对比、筛选 |
| `plot_spread_analysis.py` | 可视化 | 生成图表 |
| `debug_dex_data.py` | 调试 | 检查原始数据 |
| `optimize_aero_download.py` | 优化下载 | 单币种优化 |

---

## 📚 相关文档

- [DEX OHLCV 下载系统](GECKOTERMINAL_API_USAGE.md)
- [数据存储策略](DATA_STORAGE_STRATEGY.md)
- [池子映射指南](POOL_MAPPING_GUIDE.md)

---

## 💬 常见问题

### Q: 为什么不能达到 100% 覆盖率？

**A**: DEX 只在有实际交易时产生 K 线数据。无交易时段自然没有数据，这是 DEX 的正常特性。

### Q: 补全数据可以用于回测吗？

**A**: **不可以**。补全数据代表"如果有交易，价格会是多少"，但实际上没有交易，无法执行套利。回测必须只用 `is_filled == False` 的数据。

### Q: 如何选择最佳套利标的？

**A**: 综合考虑：
1. 覆盖率（数据完整性）
2. 平均价差（利润空间）
3. 可执行机会数量（频率）
4. 总成交量（流动性）

AERO-USDT 和 VIRTUAL-USDT 是当前最优选择。

### Q: 价差分析显示负值是什么意思？

**A**: 
- **正值** (`price_diff_pct > 0`): DEX 价格高于 CEX → CEX 买入，DEX 卖出
- **负值** (`price_diff_pct < 0`): DEX 价格低于 CEX → DEX 买入，CEX 卖出

### Q: 成交量阈值应该设多少？

**A**: 取决于交易规模:
- 小额测试: $100-$500
- 中等规模: $1,000-$5,000
- 大额交易: $10,000+

建议从小额开始，逐步增加。

---

**更新时间**: 2025-10-13  
**版本**: 1.0

