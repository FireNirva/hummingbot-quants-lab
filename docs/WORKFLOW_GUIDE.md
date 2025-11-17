# 🚀 Base链CEX-DEX套利分析完整流程

最后更新：2025-01-12

## 📋 当前配置

**Base链交易对（14个）**：
- VIRTUAL-USDT, BRETT-USDT, AERO-USDT, AIXBT-USDT
- FAI-USDT, COOKIE-USDT, MIGGLES-USDT, MIRROR-USDT
- ZORA-USDT, EDGE-USDT, BENJI-USDT, HINT-USDT
- TALENT-USDT, IRON-USDT

**数据时间间隔**：1m, 5m

---

## 🎯 完整执行流程

### ✅ 步骤 1：下载CEX历史数据（约10天）

**为什么需要这一步？**
- QuantsLab单次只能下载0.6天（约14小时）
- Freqtrade可以一次性下载更长的历史数据
- 建议下载7-10天的数据用于分析

**命令**：
```bash
# 下载7天的1m和5m数据
conda run -n quants-lab python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 7 \
  --timeframe 1m

conda run -n quants-lab python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 7 \
  --timeframe 5m
```

**预计时间**：每个timeframe约2-3分钟

**输出位置**：
- Freqtrade原始数据：`user_data/data/gateio/`
- QuantsLab转换数据：`app/data/cache/candles/gate_io|{PAIR}|{INTERVAL}.parquet`

**验证**：
```bash
# 查看已下载的1m数据
ls -lh app/data/cache/candles/gate_io|*|1m.parquet | wc -l

# 查看已下载的5m数据
ls -lh app/data/cache/candles/gate_io|*|5m.parquet | wc -l
```

---

### ✅ 步骤 2：建立CEX-DEX Pool映射

**为什么需要这一步？**
- 需要知道每个CEX交易对对应哪个DEX池子
- 自动搜索Base链上流动性最高的池子

**命令**：
```bash
# 建立Pool映射（搜索Base链上的DEX池子）
conda run -n quants-lab python scripts/build_pool_mapping.py \
  --config config/base_ecosystem_downloader_full.yml \
  --network base \
  --top-n 3
```

**预计时间**：约1-2分钟（14个pairs × 2秒 = 28秒 + API响应）

**输出位置**：
- 搜索结果：`app/data/raw/geckoterminal/search_pools/base/{PAIR}.json`
- 映射文件：`app/data/processed/pool_mappings/base_gate_io_pool_map.parquet`

**验证**：
```bash
# 查看映射文件
ls -lh app/data/processed/pool_mappings/base_gate_io_pool_map.parquet

# 查看有多少个pools被映射
python -c "import pandas as pd; df = pd.read_parquet('app/data/processed/pool_mappings/base_gate_io_pool_map.parquet'); print(f'映射了 {len(df)} 个pools')"
```

---

### ✅ 步骤 3：下载DEX历史数据

**为什么需要这一步？**
- 下载DEX池子的OHLCV数据
- 自动与CEX数据时间对齐
- 支持1m和5m两种间隔

**命令**：
```bash
# 方法A：使用任务系统（推荐，支持断点续传）
conda run -n quants-lab python cli.py trigger-task \
  --task dex_candles_downloader \
  --config config/dex_candles_base.yml

# 方法B：使用脚本（适合一次性下载）
conda run -n quants-lab python scripts/download_dex_ohlcv.py \
  --network base \
  --connector gate_io \
  --intervals 1m 5m
```

**预计时间**：
- 1m数据：约10-15分钟（每个pair约100-200次API请求）
- 5m数据：约2-3分钟（每个pair约20-40次API请求）
- 总计：约15-20分钟

**输出位置**：
- DEX数据：`app/data/cache/candles/geckoterminal_base|{PAIR}|{INTERVAL}.parquet`

**验证**：
```bash
# 查看已下载的DEX 1m数据
ls -lh app/data/cache/candles/geckoterminal_base|*|1m.parquet | wc -l

# 查看已下载的DEX 5m数据
ls -lh app/data/cache/candles/geckoterminal_base|*|5m.parquet | wc -l

# 查看某个pair的数据量
python -c "import pandas as pd; df = pd.read_parquet('app/data/cache/candles/geckoterminal_base|VIRTUAL-USDT|1m.parquet'); print(f'VIRTUAL-USDT 1m: {len(df)} 条数据')"
```

---

### ✅ 步骤 4：运行价差分析

**为什么需要这一步？**
- 分析CEX和DEX之间的价差
- 计算套利机会和潜在收益
- 生成综合评分排名

**命令**：
```bash
# 分析所有交易对（1m数据）
conda run -n quants-lab python scripts/analyze_cex_dex_spread.py \
  --compare-all \
  --interval 1m \
  --config config/base_ecosystem_downloader_full.yml

# 分析所有交易对（5m数据）
conda run -n quants-lab python scripts/analyze_cex_dex_spread.py \
  --compare-all \
  --interval 5m \
  --config config/base_ecosystem_downloader_full.yml

# 分析单个交易对（详细分析）
conda run -n quants-lab python scripts/analyze_cex_dex_spread.py \
  --pair IRON-USDT \
  --interval 1m
```

**预计时间**：每个interval约5-10秒

**输出位置**：
- 分析结果：`app/data/processed/spread_analysis/spread_analysis_{PAIR}_{INTERVAL}.parquet`
- 屏幕输出：排名、评分、统计信息

**关键指标**：
- **综合评分**：score = (avg_spread × 10 + executable_ops / 10) × volume_multiplier
- **成交量阈值**：
  - < $100K: ×0（无法套利）
  - $100K - $500K: ×0.5-0.8（低流动性）
  - $500K - $10M: ×1.0（最佳区间）✅
  - $10M - $50M: ×0.8-0.5（竞争加剧）
  - > $50M: ×0.3（极度竞争）

---

### ✅ 步骤 5：可视化分析（可选）

**为什么需要这一步？**
- 直观查看价差趋势
- 分析套利时机
- 生成报告图表

**命令**：
```bash
# 生成单个交易对的价差图表
conda run -n quants-lab python scripts/plot_spread_analysis.py \
  --pair IRON-USDT \
  --interval 1m

# 批量生成所有交易对的图表
conda run -n quants-lab python scripts/plot_spread_analysis.py \
  --plot-all \
  --interval 1m
```

**预计时间**：每个pair约2-3秒

**输出位置**：
- 图表：`app/data/processed/plots/spread_analysis_{PAIR}_{INTERVAL}.png`

---

### ✅ 步骤 6：资金需求分析（可选，用于大额交易）

**为什么需要这一步？**
- 评估需要多少资金才能执行套利
- 计算滑点影响
- 确定最优交易规模

**命令**：
```bash
# 分析单个交易对的资金需求
conda run -n quants-lab python scripts/analyze_liquidity_and_capital.py \
  --pair IRON-USDT \
  --interval 1m
```

**输出**：
- 流动性深度分析
- 滑点计算
- 建议资金规模

---

## 🔄 日常更新流程（推荐）

如果您想持续追踪数据，可以设置定期更新：

### 方案A：手动更新（每天一次）

```bash
# 1. 更新CEX数据（下载最新1天）
conda run -n quants-lab python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 1 \
  --timeframe 1m

# 2. 更新DEX数据
conda run -n quants-lab python cli.py trigger-task \
  --task dex_candles_downloader \
  --config config/dex_candles_base.yml

# 3. 运行分析
conda run -n quants-lab python scripts/analyze_cex_dex_spread.py \
  --compare-all \
  --interval 1m
```

### 方案B：自动更新（后台运行）

```bash
# CEX数据：每15分钟更新一次（后台）
nohup conda run -n quants-lab python cli.py run-tasks \
  --config config/base_ecosystem_downloader_full.yml \
  > logs/cex_download.log 2>&1 &

# DEX数据：每1小时更新一次（后台）
nohup conda run -n quants-lab python cli.py run-tasks \
  --config config/dex_candles_base.yml \
  > logs/dex_download.log 2>&1 &

# 查看后台任务
ps aux | grep "cli.py run-tasks" | grep -v grep

# 停止后台任务
pkill -f "cli.py run-tasks"
```

---

## 🔍 故障排查

### 问题1：没有找到Pool映射

**症状**：DEX下载失败，提示找不到pool_address

**解决**：
```bash
# 重新生成Pool映射
python scripts/build_pool_mapping.py \
  --config config/base_ecosystem_downloader_full.yml \
  --network base
```

### 问题2：DEX数据覆盖率很低

**症状**：分析结果显示覆盖率<5%

**原因**：DEX交易稀疏，这是正常现象

**解决**：
- 使用5m或更大的时间间隔
- 关注"可执行机会数"而不是覆盖率

### 问题3：某些币种下载失败

**症状**：Freqtrade报错"pair not found"

**原因**：Gate.io不支持该交易对

**解决**：
- 从配置文件中移除该交易对
- 或手动检查Gate.io是否有该交易对

### 问题4：后台任务重复运行

**症状**：多个相同任务在运行

**解决**：
```bash
# 查看所有后台任务
ps aux | grep "cli.py run-tasks"

# 终止所有任务
pkill -f "cli.py run-tasks"
```

---

## 📊 预期结果示例

运行完成后，您应该看到类似的排名：

```
💡 推荐排序（综合评分 - 最终优化版 V4）:
   1. IRON-USDT       ⭐⭐⭐⭐⭐  (评分: 299.1)
   2. VIRTUAL-USDT    ⭐⭐⭐⭐⭐  (评分: 233.6)
   3. MIGGLES-USDT    ⭐⭐⭐⭐⭐  (评分: 185.4)
   4. EDGE-USDT       ⭐⭐⭐⭐⭐  (评分: 138.6)
   5. BENJI-USDT      ⭐⭐⭐⭐⭐  (评分: 138.0)
   ...
```

**关键指标解读**：
- **评分>200**：优秀套利机会，优先考虑
- **评分100-200**：良好机会，可以尝试
- **评分<100**：谨慎评估，可能流动性不足或竞争激烈
- **评分=0**：无法套利（成交量<$100K）

---

## 🎯 快速开始（5分钟版）

如果您只想快速看结果：

```bash
# 1. 下载3天CEX数据（1m）
conda run -n quants-lab python scripts/import_freqtrade_data.py \
  --config config/base_ecosystem_downloader_full.yml \
  --days 3 \
  --timeframe 1m

# 2. 建立Pool映射
conda run -n quants-lab python scripts/build_pool_mapping.py \
  --config config/base_ecosystem_downloader_full.yml \
  --network base

# 3. 下载DEX数据
conda run -n quants-lab python cli.py trigger-task \
  --task dex_candles_downloader \
  --config config/dex_candles_base.yml

# 4. 运行分析
conda run -n quants-lab python scripts/analyze_cex_dex_spread.py \
  --compare-all \
  --interval 1m
```

---

## 📚 相关文档

- [评分公式详解](./docs/SCORING_FORMULA_OPTIMIZATION.md)
- [资金需求分析](./docs/CAPITAL_REQUIREMENT_ANALYSIS.md)
- [命令速查表](./docs/COMMANDS_CHEATSHEET.md)
- [GeckoTerminal API使用](./docs/GECKOTERMINAL_API_USAGE.md)

---

**🎉 祝您交易顺利！如有问题，随时查阅本指南或咨询技术支持。**

