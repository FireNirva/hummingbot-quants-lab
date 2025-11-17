# 🚀 QuantsLab 命令速查表

## 📊 Base 链套利池筛选

### 快速开始

```bash
# 进入项目目录
cd /Users/alice/Dropbox/投资/量化交易/quants-lab

# 验证配置文件
python cli.py validate-config --config base_arbitrage_pools_screener.yml

# 查看所有任务
python cli.py list-tasks --config base_arbitrage_pools_screener.yml

# 运行所有策略（推荐）
python cli.py run-tasks --config base_arbitrage_pools_screener.yml

# 后台运行
nohup python cli.py run-tasks --config base_arbitrage_pools_screener.yml > logs/base_arb.log 2>&1 &
```

### 单独运行策略

```bash
# 1. 高流动性稳定套利（大额）
python cli.py trigger-task --task base_high_liquidity_arb --config base_arbitrage_pools_screener.yml

# 2. 高交易量热门套利（高频）
python cli.py trigger-task --task base_hot_volume_arb --config base_arbitrage_pools_screener.yml

# 3. ETH 配对跨链套利
python cli.py trigger-task --task base_eth_pair_arb --config base_arbitrage_pools_screener.yml

# 4. 早期新池套利（高风险）
python cli.py trigger-task --task base_new_pools_arb --config base_arbitrage_pools_screener.yml

# 5. 均衡中等规模套利
python cli.py trigger-task --task base_balanced_arb --config base_arbitrage_pools_screener.yml
```

### 监控运行

```bash
# 查看实时日志
tail -f logs/base_arb.log

# 查看进程
ps aux | grep "python cli.py run-tasks"

# 停止后台任务
pkill -f "python cli.py run-tasks.*base_arbitrage"
```

---

## 🗄️ 数据库管理

```bash
# 启动数据库
make run-db

# 停止数据库
make stop-db

# 查看容器状态
docker ps

# 查看 MongoDB 日志
docker logs mongodb

# 访问 Mongo Express
open http://localhost:28081/
# 用户名: admin, 密码: changeme
```

---

## 📁 文件位置

```bash
# 配置文件
config/base_arbitrage_pools_screener.yml

# 文档
docs/BASE_ARBITRAGE_GUIDE.md

# K线数据
app/data/cache/candles/

# MongoDB 数据
# 数据库: quants_lab
# 集合: pools
```

---

## 🔍 数据查看

### Jupyter Notebook

```python
import pandas as pd
from core.database_manager import db_manager

# 连接 MongoDB
mongo = await db_manager.get_mongodb_client()

# 查询最新结果
results = await mongo.find_documents(
    "pools",
    {"network": "base"},
    sort=[("timestamp", -1)],
    limit=1
)

# 分析数据
pools_df = pd.DataFrame(results[0]['filtered_trending_pools'])
pools_df['arb_score'] = pools_df['volume_liquidity_ratio']
top = pools_df.nlargest(10, 'arb_score')
print(top[['name', 'volume_usd_h24', 'reserve_in_usd', 'arb_score']])
```

---

## ⚡ 5 大套利策略概览

| 策略 | 扫描频率 | 流动性 | 交易量 | 风险 | 适合资金 |
|------|---------|-------|--------|------|---------|
| 高流动性 | 30分钟 | $200K+ | $300K+ | 低 | $10K-$50K |
| 高交易量 | 15分钟 | $100K+ | $500K+ | 中 | $1K-$5K |
| ETH配对 | 30分钟 | $150K+ | $200K+ | 中 | $5K-$20K |
| 新池子 | 30分钟 | $50K+ | $100K+ | 高 | <$1K |
| 均衡 | 1小时 | $100K+ | $150K+ | 中 | $2K-$8K |

---

## 🛠️ 故障排查

```bash
# 配置验证
python cli.py validate-config --config base_arbitrage_pools_screener.yml

# 测试单个任务
python cli.py trigger-task --task base_high_liquidity_arb --config base_arbitrage_pools_screener.yml --timeout 600

# 检查环境
conda activate quants-lab
which python
python --version

# 检查 MongoDB
docker ps | grep mongodb
mongo mongodb://admin:admin@localhost:27017/quants_lab
```

---

## 📥 Freqtrade 历史数据导入

### 快速下载

```bash
# 下载 6 天的 1m 数据（Gate.io Base 生态代币）
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m

# 下载 7 天的 5m 数据（推荐）
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 7 \
  --timeframe 5m
```

### 增量添加历史数据

```bash
# 追加更早的历史数据（6天）
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 6 \
  --timeframe 1m \
  --prepend
```

### 多交易所支持

```bash
# 从 Binance 下载（覆盖配置文件）
python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 30 \
  --timeframe 5m \
  --exchange binance
```

### 查看数据

```bash
# 查看所有已下载的数据
python scripts/view_parquet.py --all

# 查看特定交易对
python scripts/view_parquet.py "app/data/cache/candles/gate_io|VIRTUAL-USDT|1m.parquet"
```

---

## 🗺️ CEX-DEX 池子映射

### Token 名称映射（Wrapped Tokens）

```bash
# 编辑 token 映射配置（处理 wrapped tokens 等）
vim config/token_mapping.yml

# 添加映射示例：
# IRON: wIRON
# ETH: WETH
# BTC: WBTC

# 验证映射效果
python scripts/build_pool_mapping.py \
  --network base \
  --connector gate_io \
  --pairs IRON-USDT \
  --top-n 3

# 输出会显示:
# Token mapping: IRON -> wIRON
# Found 3 pools for IRON

# 查看详细文档
cat docs/TOKEN_MAPPING_GUIDE.md
```

### CLI 脚本方式

```bash
# 自动检测所有Gate.io交易对，映射到Base链
python scripts/build_pool_mapping.py --network base --connector gate_io

# 指定特定交易对
python scripts/build_pool_mapping.py \
  --network base \
  --pairs AERO-USDT,BRETT-USDT,VIRTUAL-USDT

# 保留top 5池子（默认3）
python scripts/build_pool_mapping.py \
  --network base \
  --connector gate_io \
  --top-n 5
```

### 任务系统方式

```bash
# 验证配置
python cli.py validate-config --config config/pool_mapping_base.yml

# 手动触发一次（测试）
python cli.py trigger-task \
  --task base_pool_mapping \
  --config config/pool_mapping_base.yml

# 调度运行（每24小时）
python cli.py run-tasks --config config/pool_mapping_base.yml

# 后台运行
nohup python cli.py run-tasks --config config/pool_mapping_base.yml > logs/pool_mapping.log 2>&1 &
```

### 查看映射数据

```bash
# 查看Parquet文件
python -c "
import pandas as pd
df = pd.read_parquet('app/data/processed/pool_mappings/base_gate_io_pool_map.parquet')
print(df[['trading_pair', 'dex_id', 'pool_address', 'reserve_usd', 'rank']].head(10))
"

# 查看原始JSON（某个交易对）
cat app/data/raw/geckoterminal/search_pools/base/AERO-USDT.json | python -m json.tool
```

---

## 📈 DEX OHLCV 数据下载

### CLI 脚本方式（手动下载）

```bash
# 快速开始：下载7天数据
python scripts/download_dex_ohlcv.py \
  --network base \
  --intervals 5m 15m 1h \
  --lookback-days 7

# 与CEX数据对齐时间范围
python scripts/download_dex_ohlcv.py \
  --network base \
  --connector gate_io \
  --align-with-cex

# 保存原始API响应（调试用）
python scripts/download_dex_ohlcv.py \
  --network base \
  --save-raw

# 限制请求数（避免超速）
python scripts/download_dex_ohlcv.py \
  --network base \
  --max-requests 50

# 指定特定交易对
python scripts/download_dex_ohlcv.py \
  --network base \
  --pairs AERO-USDT BRETT-USDT

# 自定义速率限制
python scripts/download_dex_ohlcv.py \
  --network base \
  --rate-limit 2.0  # 2秒间隔
```

### 任务系统方式（调度下载）

```bash
# 验证配置
python cli.py validate-config --config config/dex_candles_base.yml

# 手动触发一次（测试）
python cli.py trigger-task \
  --task dex_candles_downloader \
  --config config/dex_candles_base.yml

# 调度运行（每小时）
python cli.py run-tasks --config config/dex_candles_base.yml

# 后台运行
nohup python cli.py run-tasks --config config/dex_candles_base.yml > logs/dex_candles.log 2>&1 &
```

### 查看DEX数据

```bash
# 查看下载的DEX数据
python -c "
import pandas as pd
df = pd.read_parquet('app/data/cache/candles/geckoterminal_base|AERO-USDT|5m.parquet')
print(df.tail(10))
print(f'\n总计: {len(df)} 条K线')
print(f'时间范围: {df.index.min()} 到 {df.index.max()}')
"

# 查看所有DEX数据文件
ls -lh app/data/cache/candles/geckoterminal_*

# 比较CEX vs DEX数据
python -c "
import pandas as pd

# 读取CEX和DEX数据
cex_df = pd.read_parquet('app/data/cache/candles/gate_io|AERO-USDT|5m.parquet')
dex_df = pd.read_parquet('app/data/cache/candles/geckoterminal_base|AERO-USDT|5m.parquet')

print(f'CEX: {len(cex_df)} 条K线')
print(f'DEX: {len(dex_df)} 条K线')
print(f'\nCEX价格范围: {cex_df[\"close\"].min():.4f} - {cex_df[\"close\"].max():.4f}')
print(f'DEX价格范围: {dex_df[\"close\"].min():.4f} - {dex_df[\"close\"].max():.4f}')

# 计算重叠时间段的价差
merged = cex_df.join(dex_df, how='inner', rsuffix='_dex')
merged['spread'] = (merged['close_dex'] - merged['close']) / merged['close'] * 100
print(f'\n平均价差: {merged[\"spread\"].mean():.2f}%')
"
```

### 数据验证

```bash
# 验证数据质量
python -c "
import pandas as pd

df = pd.read_parquet('app/data/cache/candles/geckoterminal_base|AERO-USDT|5m.parquet')

# 检查重复
assert df.index.is_unique, '发现重复时间戳'

# 检查NaN
assert not df.isnull().any().any(), '发现NaN值'

# 检查时间连续性
time_diff = df.index.to_series().diff()
expected_diff = pd.Timedelta(minutes=5)
gaps = time_diff[time_diff > expected_diff * 1.5]
print(f'数据连续性: {len(gaps)} 个间隙')

print('✓ 数据验证通过')
"
```

---

## 📊 CEX-DEX 价差分析与可视化

### 价差分析

```bash
# 单交易对详细分析
python scripts/analyze_cex_dex_spread.py --pair AERO-USDT --interval 1m

# 指定成交量阈值
python scripts/analyze_cex_dex_spread.py --pair AERO-USDT --volume-threshold 500

# 多交易对对比（从配置文件读取交易对列表，使用优化后的评分公式）
python scripts/analyze_cex_dex_spread.py --compare-all

# 指定其他配置文件
python scripts/analyze_cex_dex_spread.py --compare-all --config config/your_config.yml
```

**📊 综合评分公式（最终优化版 V4）**:
```
score = (avg_spread × 10 + executable_ops / 10) × volume_multiplier
```

**核心理念**：抓住本质 + 成交量倒U型优化
- ✅ **价差×10** - 决定每次能赚多少（最重要！）
- ✅ **机会数/10** - 决定能赚多少次（很重要！）
- ✅ **成交量系数** - 倒U型曲线（太低或太高都降低排名）

**成交量阈值（倒U型）**:
- < $100K: 评分×0 ❌（无法套利，直接归零）
- $100K - $500K: 评分×0.5-0.8（低流动性）
- $500K - $10M: 评分×1.0 ✅（最佳区间）
- $10M - $50M: 评分×0.8-0.5（竞争加剧）
- > $50M: 评分×0.3（极度竞争）

**为什么加入成交量阈值？**
1. 太低（<$100K）→ 完全无法套利，直接归零 ❌
2. 适中（$500K-$10M）→ 流动性充足，竞争适中 ✅
3. 太高（>$50M）→ 市场高度有效，价差被抹平

**详细说明**: [评分公式优化文档](./SCORING_FORMULA_OPTIMIZATION.md)

### 可视化图表生成

```bash
# 生成价差分析图表（需要先安装 matplotlib）
python scripts/plot_spread_analysis.py --pair AERO-USDT --interval 1m

# 其他交易对
python scripts/plot_spread_analysis.py --pair VIRTUAL-USDT --interval 1m
```

**生成的图表**:
- `spread_timeseries_{pair}_{interval}.png` - 价差时序图（双曲线）
- `spread_distribution_{pair}_{interval}.png` - 价差分布直方图
- `liquidity_spread_{pair}_{interval}.png` - 流动性-价差散点图

**保存位置**: `app/data/processed/plots/`

### 查看分析结果

```bash
# 查看价差数据
python scripts/view_parquet.py app/data/processed/spread_analysis/spread_analysis_AERO-USDT_1m.parquet

# 查看生成的图表
open app/data/processed/plots/spread_timeseries_AERO-USDT_1m.png

# 查看所有图表和数据
ls -lh app/data/processed/plots/
ls -lh app/data/processed/spread_analysis/
```

💡 **说明**: 价差分析支持双模式（连续时间轴 vs 事件时间），详见 [CEX-DEX 价差分析指南](docs/CEX_DEX_SPREAD_ANALYSIS.md)

---

## 💰 资金需求评估

### 单个交易对分析

```bash
# 分析IRON-USDT的资金需求（流动性、滑点、利润）
python scripts/analyze_liquidity_and_capital.py --pair IRON-USDT

# 分析其他交易对
python scripts/analyze_liquidity_and_capital.py --pair AERO-USDT
python scripts/analyze_liquidity_and_capital.py --pair BRETT-USDT
```

**输出内容**:
- 💧 流动性信息（DEX池子TVL）
- 📊 价差信息（平均价差、可执行机会）
- 💹 滑点分析（不同交易金额的滑点和利润）
- 🎯 最优交易金额（1%和0.5%滑点限制）
- 💰 建议交易金额和预期收益
- 📈 月度ROI预估

**示例输出**:
```
💰 IRON-USDT 资金需求分析

流动性: $196,315
平均价差: 7.97%

滑点与利润分析:
  $100:   滑点0.05%, 净利润$7.61  (7.61% ROI) ✓ 推荐
  $1,000: 滑点0.51%, 净利润$71.55 (7.15% ROI) ✓ 推荐
  $5,000: 滑点2.58%, 净利润$254  (5.09% ROI) ⚠️ 滑点大

建议交易金额: $1,000
单次预期利润: $71.55
机会频率: 328次/天

建议总资金: $2,000（可滚动操作）
月度ROI: 35216%（理论值，实际需打折）
```

### 多交易对对比

```bash
# 对比所有交易对的资金需求
python scripts/analyze_liquidity_and_capital.py --compare-all
```

**输出对比表**:
```
交易对          | 流动性         | 平均价差 | 最优金额    | 单次利润 | 利润率
IRON-USDT      | $196,315      | 7.97%   | $1,953     | $130.21 | 6.67%
BRETT-USDT     | $4,531,761    | 2.50%   | $45,091    | $541.38 | 1.20%
AERO-USDT      | $51,335,914   | 0.34%   | $510,792   | -$4879  | -0.96% ✗
```

### 前置准备

确保已运行：
```bash
# 1. 生成pool mapping（如果还没有）
python scripts/build_pool_mapping.py --network base --connector gate_io --top-n 1

# 2. 生成价差分析数据（每个要分析的交易对）
python scripts/analyze_cex_dex_spread.py --pair IRON-USDT
```

### 关键指标说明

- **流动性（TVL）**: DEX池子总锁仓量，决定可承载的交易规模
- **滑点**: 大额交易的价格冲击（公式: `1 - sqrt(1 - amount/reserve)`）
- **净利润**: `价差 - 滑点 - 手续费(0.3%) - Gas费($0.01)`
- **最优金额**: 1%滑点限制下的最大交易金额
- **利润率**: 单次净利润 / 交易金额 × 100%

### 资金配置建议

| 策略 | 资金规模 | 适合交易对 | 预期月度ROI |
|-----|---------|-----------|------------|
| 小资金高频 | $2K-$5K | IRON, GPS | 50% |
| 中等稳健 | $20K-$100K | BRETT, VIRTUAL | 20% |
| 大资金分散 | $100K+ | 多交易对组合 | 15% |

💡 **重要提示**: 
- 理论ROI需打折50%-70%（考虑竞争、延迟、失败率）
- 建议从小额测试开始（$100-$1K）
- 持续监控流动性变化和价差趋势

详细指南: [资金需求分析指南](./CAPITAL_REQUIREMENT_ANALYSIS.md)

---

## 📚 相关文档

- [💰 资金需求分析指南](docs/CAPITAL_REQUIREMENT_ANALYSIS.md) ⭐ 最新
- [📊 CEX-DEX 价差分析指南](docs/CEX_DEX_SPREAD_ANALYSIS.md)
- [🔢 评分公式优化说明](docs/SCORING_FORMULA_OPTIMIZATION.md)
- [🗺️ CEX-DEX 池子映射指南](docs/POOL_MAPPING_GUIDE.md)
- [🔀 Token 映射指南](docs/TOKEN_MAPPING_GUIDE.md)
- [Base 套利完整指南](docs/BASE_ARBITRAGE_GUIDE.md)
- [GeckoTerminal API 使用指南](docs/GECKOTERMINAL_API_USAGE.md)
- [Freqtrade 数据导入指南](docs/FREQTRADE_IMPORT.md)
- [数据收集指南](docs/DATA_COLLECTION_GUIDE.md)
- [快速上手](docs/QUICK_START_DATA_COLLECTION.md)
- [数据存储策略](docs/DATA_STORAGE_STRATEGY.md)

---

**快速访问**: 复制粘贴命令即可使用！⚡

