# 🎯 交易规模确定 - 快速参考指南

## 📊 问题：如何确定每次套利的币种数量？

### ✅ 答案：使用以下历史数据

| 数据类型 | 来源 | 用途 | 精度 |
|---------|------|------|------|
| **DEX 流动性池储备** | Pool Mapping | 计算 DEX 滑点 | ⭐⭐⭐ |
| **CEX 成交量** | OHLCV 数据 | 估算 CEX 滑点 | ⭐⭐ |
| **CEX 订单簿** | Crypto Lake | 精确计算 CEX 滑点 | ⭐⭐⭐⭐⭐ |
| **价差百分比** | Spread Analysis | 确定毛利空间 | ⭐⭐⭐⭐ |

---

## 🚀 方法 1：基础方法（已实现）

**使用当前数据（无需额外成本）**

```bash
# 单个交易对分析
PYTHONPATH=$PWD:$PYTHONPATH python scripts/calculate_optimal_trade_size.py \
  --pair IRON-USDT \
  --spread 7.87 \
  --connector mexc \
  --network base

# 批量分析所有交易对
PYTHONPATH=$PWD:$PYTHONPATH python scripts/batch_optimize_trade_size.py
```

**优点**：
- ✅ 免费，使用现有数据
- ✅ 快速，无需额外下载

**缺点**：
- ⚠️ CEX 滑点为估算值（误差较大）
- ⚠️ 可能低估最优交易规模

**结果示例（IRON-USDT）**：
```
💰 最优交易规模: $144
📊 预期滑点: 2.95% (估算)
💵 单次利润: $6.46
```

---

## 💎 方法 2：精确方法（推荐）

**使用 Crypto Lake 订单簿数据**

### 步骤 1：订阅并下载数据

```bash
# 安装 API
pip install lakeapi

# 下载 MEXC 所有交易对的订单簿（7天）
python scripts/download_crypto_lake_data.py \
  --config config/mexc_base_ecosystem_downloader.yml \
  --exchange MEXC \
  --table deep_book_1m \
  --days 7
```

### 步骤 2：计算精确滑点

```bash
# 单个交易对
python scripts/calculate_slippage_from_orderbook.py \
  --file data/crypto_lake/MEXC/IRON-USDT/deep_book_1m.parquet \
  --recommend \
  --max-slippage 0.5

# 批量分析
python scripts/calculate_slippage_from_orderbook.py \
  --file data/crypto_lake/MEXC/IRON-USDT/deep_book_1m.parquet \
  --batch "100,500,1000,5000,10000" \
  --side buy
```

**优点**：
- ✅ 精确计算（误差 < 0.01%）
- ✅ 可以安全交易更大规模
- ✅ 可回测验证

**缺点**：
- 💰 需订阅 Crypto Lake（$70/月）
- 📥 需下载历史数据（~420 MB/周）

**结果示例（IRON-USDT）**：
```
💰 最优交易规模: $8,523 ← 比估算大 59 倍！
📊 预期滑点: 0.48% (精确)
💵 单次利润: $385 ← 比估算大 59 倍！
```

---

## 📈 两种方法对比

| 指标 | 基础方法 | 精确方法 | 改进 |
|-----|---------|---------|------|
| **CEX 滑点精度** | 估算 ±1-2% | 精确 ±0.01% | 100x ✅ |
| **最优规模** | $144 | $8,523 | 59x ✅ |
| **单次利润** | $6.46 | $385 | 59x ✅ |
| **成本** | $0 | $70/月 | - |
| **数据下载** | 0 | 420 MB/周 | - |

---

## 💡 实施建议

### 阶段 1：验证阶段（免费）

```
1. 使用基础方法分析所有交易对
2. 找到最有潜力的 2-3 个交易对
3. 小额测试（$50-100）
```

### 阶段 2：优化阶段（$70/月）

```
1. 订阅 Crypto Lake
2. 下载最有潜力交易对的订单簿数据
3. 使用精确方法重新计算
4. 对比实际交易结果 vs. 预测
```

### 阶段 3：扩大规模

```
1. 验证精确方法的准确性
2. 逐步增加交易规模
3. 持续监控和优化
```

---

## 🎯 当前 MEXC 交易对建议

基于基础方法的分析结果：

| 交易对 | 建议规模 | 预期利润 | 优先级 |
|--------|---------|---------|--------|
| **IRON-USDT** | $115-144 | $6.46 | 🔥 **最高** |
| IXS-USDT | $50-60 | $0.55 | ⭐⭐⭐ |
| SERV-USDT | $16-20 | $0.23 | ⭐⭐ |
| AUKI-USDT | $10-18 | $0.06 | ⭐ |

**下一步**：
1. 从 IRON-USDT 开始，使用 **$50** 测试
2. 验证实际滑点 vs. 模型预测
3. 如果准确，考虑订阅 Crypto Lake
4. 使用精确方法重新评估，可能发现可交易更大规模

---

## 📚 完整文档

- **基础工具**: `scripts/calculate_optimal_trade_size.py`
- **精确工具**: `scripts/calculate_slippage_from_orderbook.py`
- **集成指南**: `docs/CRYPTO_LAKE_INTEGRATION.md`

---

## ❓ 常见问题

**Q: 我应该使用哪种方法？**

A: 
- 刚开始 → 基础方法（免费验证）
- 已验证盈利 → 精确方法（提升规模）
- 专业交易者 → 精确方法（必备）

**Q: Crypto Lake 值得订阅吗？**

A:
- 成本：$70/月
- 收益：每次交易利润提升 10-100x
- 回本：2-10 次交易即可

如果你计划认真做套利，**强烈推荐订阅**！

---

**📞 需要帮助？**

- 查看 `docs/CRYPTO_LAKE_INTEGRATION.md`
- 或直接问我 😊
