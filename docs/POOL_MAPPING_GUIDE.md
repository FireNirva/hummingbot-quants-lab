# 🗺️ CEX-DEX池子映射系统使用指南

## 📖 一、系统概述

### 功能说明

CEX-DEX池子映射系统自动将中心化交易所(CEX)的交易对映射到去中心化交易所(DEX)的高流动性池子。

**核心功能:**
- 🔍 自动从candles数据目录检测交易对
- 🌐 使用GeckoTerminal API搜索对应的DEX池子
- 📊 按流动性排序，保留top N个最优池子
- 💾 保存原始API响应和处理后的映射数据
- ♻️  支持增量更新和定时刷新

**支持网络:**
- Base Chain（主要支持）
- Solana
- Ethereum
- 其他GeckoTerminal支持的网络

### 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│ 1. 读取Candles文件                                           │
│    app/data/cache/candles/gate_io|*|*.parquet              │
│    → 提取唯一交易对列表                                       │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. 搜索DEX池子                                               │
│    • 提取base token（如AERO-USDT → AERO）                   │
│    • 调用GeckoTerminal API搜索池子                           │
│    • 按流动性（reserve_usd）排序                             │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. 保存映射数据                                              │
│    • 原始JSON: app/data/raw/geckoterminal/search_pools/     │
│    • 处理后Parquet: app/data/processed/pool_mappings/       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Token 名称映射（重要！）

### 问题场景

某些 token 在 CEX 和 DEX 上使用不同的名称，导致无法找到对应的池子：

| CEX Token | DEX Token | 原因 |
|-----------|-----------|------|
| **IRON** | **wIRON** | Wrapped version ⚠️ |
| ETH | WETH | Wrapped Ether |
| BTC | WBTC | Wrapped Bitcoin |

### 解决方案

编辑 `config/token_mapping.yml` 添加映射：

```yaml
# CEX-DEX Token 名称映射
IRON: wIRON
ETH: WETH
BTC: WBTC
```

系统会自动：
1. ✅ 读取映射配置
2. ✅ 使用 DEX token 名称（wIRON）搜索
3. ✅ 保持 CEX 名称（IRON-USDT）在结果中

**详细文档**: [Token Mapping Guide](TOKEN_MAPPING_GUIDE.md)

---

## 🚀 二、快速开始

### Phase 1: CLI脚本方式

#### 前置条件

1. **Python环境**: quants-lab conda环境
2. **依赖包**: geckoterminal_py已安装
3. **数据**: 至少有一些CEX candles数据
4. **Token映射** (可选): 如有 wrapped tokens，配置 `config/token_mapping.yml`

#### 1. 基础用法

**自动检测所有交易对:**

```bash
# 激活环境
conda activate quants-lab

# 自动检测gate_io的所有交易对，映射到Base链
python scripts/build_pool_mapping.py --network base --connector gate_io
```

**输出示例:**
```
================================================================================
🗺️  CEX-DEX池子映射构建工具
================================================================================

📋 配置信息:
  - 网络: base
  - 连接器: gate_io
  - Top N: 3
  - Candles目录: /path/to/app/data/cache/candles

🔍 从 /path/to/app/data/cache/candles 自动检测交易对...
✓ 检测到 20 个交易对:
   - AERO-USDT
   - AIXBT-USDT
   - AWS-USDT
   ...

🔄 开始构建池子映射（这可能需要一些时间）...
   预计耗时: ~10秒 (20个交易对 × 0.5秒/个)
```

#### 2. 高级用法

**指定特定交易对:**

```bash
# 只处理3个交易对
python scripts/build_pool_mapping.py \
  --network base \
  --pairs AERO-USDT,BRETT-USDT,VIRTUAL-USDT
```

**调整保留池子数量:**

```bash
# 每个交易对保留top 5个池子
python scripts/build_pool_mapping.py \
  --network base \
  --connector gate_io \
  --top-n 5
```

**自定义目录:**

```bash
# 使用自定义candles目录
python scripts/build_pool_mapping.py \
  --network base \
  --candles-dir /custom/path/to/candles \
  --output-dir /custom/path/to/output
```

**查看帮助信息:**

```bash
python scripts/build_pool_mapping.py --help
```

---

## 📊 三、输出数据说明

### 1. 原始JSON文件

**位置:** `app/data/raw/geckoterminal/search_pools/{network}/`

**格式:** 每个交易对一个JSON文件

**示例文件名:** `AERO-USDT.json`

**内容结构:**
```json
{
  "query": "AERO",
  "network": "base",
  "pools_found": 3,
  "pools": [
    {
      "pool_address": "0x...",
      "name": "AERO / USDC",
      "dex_id": "aerodrome-base",
      "reserve_usd": 1250000.50,
      "volume_usd_h24": 850000.25,
      "pool_created_at": "2024-01-15T10:30:00Z",
      "base_token_address": "0x...",
      "quote_token_address": "0x..."
    }
  ],
  "timestamp": "2025-10-12T10:30:00Z"
}
```

**用途:**
- API响应追溯
- 调试问题
- 分析趋势变化

### 2. 处理后的Parquet文件

**位置:** `app/data/processed/pool_mappings/`

**格式:** `{network}_{connector}_pool_map.parquet`

**示例文件名:** `base_gate_io_pool_map.parquet`

**Schema:**

| 列名 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `connector` | str | CEX连接器 | gate_io |
| `trading_pair` | str | 交易对 | AERO-USDT |
| `network_id` | str | 网络ID | base |
| `dex_id` | str | DEX标识 | aerodrome-base |
| `pool_address` | str | 池子地址 | 0x4c36... |
| `base_token_address` | str | 基础代币地址 | 0x940... |
| `quote_token_address` | str | 报价代币地址 | 0x833... |
| `reserve_usd` | float | 流动性(USD) | 1250000.50 |
| `volume_usd_h24` | float | 24h交易量(USD) | 850000.25 |
| `pool_created_at` | str | 创建时间 | 2024-01-15T10:30:00Z |
| `rank` | int | 排名（1=最高流动性） | 1 |
| `updated_at` | datetime | 更新时间 | 2025-10-12 10:30:00 |

**读取示例:**

```python
import pandas as pd

# 读取映射数据
df = pd.read_parquet('app/data/processed/pool_mappings/base_gate_io_pool_map.parquet')

# 查看特定交易对的池子
aero_pools = df[df['trading_pair'] == 'AERO-USDT']
print(aero_pools[['dex_id', 'reserve_usd', 'rank']])

# 获取所有交易对的top1池子
top_pools = df[df['rank'] == 1]
```

---

## ⚙️ 四、配置参数详解

### 命令行参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--network` | str | base | 网络ID（base/solana/eth等） |
| `--connector` | str | gate_io | CEX连接器名称 |
| `--candles-dir` | Path | data_paths.candles_dir | Candles数据目录 |
| `--output-dir` | Path | data_paths.processed_dir | 输出目录 |
| `--top-n` | int | 3 | 每个交易对保留的池子数 |
| `--pairs` | str | None | 逗号分隔的交易对列表 |

### 参数详细说明

**--network**
- 必须是GeckoTerminal支持的网络ID
- 常用值: `base`, `eth`, `bsc`, `polygon`, `arbitrum`, `optimism`, `solana`
- 不区分大小写

**--connector**
- 必须与candles文件名中的connector部分匹配
- 示例: `gate_io`, `binance_perpetual`, `okx`

**--top-n**
- 建议值: 3-5
- 过多会增加数据量，过少可能漏掉好的备选池子

**--pairs**
- 覆盖自动检测
- 格式: `PAIR1-USDT,PAIR2-USDT,PAIR3-USDT`
- 不要有空格

---

## 🔧 五、故障排除

### 常见问题

#### 1. API限流

**症状:**
```
Error searching pools for AERO: Rate limit exceeded
```

**原因:** GeckoTerminal API有速率限制

**解决方案:**
- 脚本已内置0.5秒延迟，通常足够
- 如果仍遇到限流，可手动修改`pool_mapping.py`中的延迟时间
- 分批处理交易对（使用`--pairs`参数）

#### 2. 交易对搜索无结果

**症状:**
```
⚠️  No pools found for NEWTOKEN-USDT
```

**原因:**
- 代币在目标网络上没有池子
- 代币名称在GeckoTerminal中不同
- 代币太新，尚未被GeckoTerminal索引

**解决方案:**
- 检查代币是否真的在该网络上存在
- 手动在GeckoTerminal网站搜索验证
- 等待一段时间后重试（新币需要时间索引）

#### 3. 网络ID错误

**症状:**
```
Error: Network 'base-chain' not found
```

**原因:** 网络ID格式不正确

**解决方案:**
- 使用正确的网络ID: `base`（不是`base-chain`或`Base`）
- 参考GeckoTerminal API文档获取正确的网络ID

#### 4. Candles目录为空

**症状:**
```
❌ 错误: 未找到 gate_io 的交易对
```

**原因:** 指定connector的candles文件不存在

**解决方案:**
- 确认candles目录路径正确
- 确认已有CEX数据下载
- 检查connector名称拼写（如`gate_io`不是`gateio`）

#### 5. 导入错误

**症状:**
```
ModuleNotFoundError: No module named 'geckoterminal_py'
```

**原因:** 依赖包未安装

**解决方案:**
```bash
conda activate quants-lab
pip install geckoterminal-py
```

---

## 📈 六、最佳实践

### 1. 定期更新映射

**为什么需要更新:**
- 流动性会随时间变化
- 新池子不断创建
- 旧池子可能关闭或流动性枯竭

**推荐频率:**
- 生产环境: 每天一次
- 开发/测试: 每周一次
- 手动调整: 根据需要

### 2. 数据验证

**运行后检查:**
```python
import pandas as pd

df = pd.read_parquet('app/data/processed/pool_mappings/base_gate_io_pool_map.parquet')

# 检查覆盖率
print(f"映射了 {df['trading_pair'].nunique()} 个交易对")
print(f"总共 {len(df)} 个池子记录")

# 检查流动性
print(f"平均流动性: ${df['reserve_usd'].mean():,.0f}")
print(f"中位数流动性: ${df['reserve_usd'].median():,.0f}")

# 找出低流动性池子
low_liquidity = df[df['reserve_usd'] < 10000]
if not low_liquidity.empty:
    print(f"\n⚠️  {len(low_liquidity)} 个池子流动性低于$10K:")
    print(low_liquidity[['trading_pair', 'reserve_usd', 'dex_id']])
```

### 3. 与下游任务集成

**在DEX数据下载任务中使用:**

```python
# 读取池子映射
mapping_df = pd.read_parquet('app/data/processed/pool_mappings/base_gate_io_pool_map.parquet')

# 获取AERO-USDT的top1池子
aero_pool = mapping_df[
    (mapping_df['trading_pair'] == 'AERO-USDT') & 
    (mapping_df['rank'] == 1)
].iloc[0]

pool_address = aero_pool['pool_address']
network_id = aero_pool['network_id']

# 使用pool_address下载DEX数据
# ...
```

---

## 🔄 Phase 2: 任务系统集成

### 一、配置任务

创建或编辑 `config/pool_mapping_base.yml`:

```yaml
# Base链池子映射配置
# 用途: 将Gate.io交易对映射到Base链DEX池子

tasks:
  base_pool_mapping:
    enabled: true
    task_class: app.tasks.data_collection.pool_mapping_task.PoolMappingTask
    
    # 调度配置：每24小时运行一次
    schedule:
      type: frequency
      frequency_hours: 24.0
      timezone: UTC
    
    # 重试配置
    max_retries: 3
    retry_delay_seconds: 300    # 5分钟
    timeout_seconds: 1800        # 30分钟
    
    # 任务特定配置
    config:
      network: "base"
      connector: "gate_io"
      top_n: 3                   # 每个交易对保留top 3池子
      # trading_pairs: []         # 留空表示自动检测
    
    # 标签（用于分类和筛选）
    tags:
      - pool_mapping
      - base
      - gate_io
      - data_collection
```

**配置说明:**

- `enabled: true`: 启用任务
- `schedule.frequency_hours`: 运行频率（24.0 = 每天一次）
- `config.network`: 目标网络
- `config.connector`: CEX连接器
- `config.top_n`: 保留池子数量
- `config.trading_pairs`: 留空=自动检测，或指定列表

### 二、运行方式

#### 1. 手动触发（测试）

```bash
# 激活环境
conda activate quants-lab

# 手动触发一次
python cli.py trigger-task \
  --task base_pool_mapping \
  --config config/pool_mapping_base.yml
```

#### 2. 调度运行（生产）

```bash
# 前台运行（查看日志）
python cli.py run-tasks --config config/pool_mapping_base.yml

# 后台运行
nohup python cli.py run-tasks --config config/pool_mapping_base.yml > logs/pool_mapping.log 2>&1 &

# 查看后台进程
ps aux | grep "pool_mapping"

# 查看日志
tail -f logs/pool_mapping.log
```

### 三、调度选项

#### 1. 频率模式（推荐）

适用于固定间隔运行：

```yaml
schedule:
  type: frequency
  frequency_hours: 24.0  # 每天
  timezone: UTC
```

**常用频率:**
- `24.0`: 每天一次
- `12.0`: 每12小时一次
- `168.0`: 每周一次

#### 2. Cron模式

适用于固定时间运行：

```yaml
schedule:
  type: cron
  cron: "0 2 * * *"  # 每天凌晨2点（UTC）
  timezone: UTC
```

**常用Cron表达式:**
- `"0 2 * * *"`: 每天凌晨2点
- `"0 */6 * * *"`: 每6小时
- `"0 0 * * 0"`: 每周日午夜

### 四、监控和日志

#### 查看任务状态

```bash
# 查看运行中的任务
ps aux | grep "cli.py run-tasks"

# 查看日志
tail -f logs/pool_mapping.log

# 搜索错误
grep "ERROR" logs/pool_mapping.log

# 搜索成功完成
grep "✓ PoolMappingTask succeeded" logs/pool_mapping.log
```

#### 日志输出示例

```
2025-10-12 10:30:00 - INFO - Starting pool mapping for gate_io on base
2025-10-12 10:30:00 - INFO - Auto-detected pairs: 20 pairs
2025-10-12 10:30:15 - INFO - Found 3 pools for AERO (total: 5)
2025-10-12 10:30:20 - INFO - Pool mapping completed: {'pairs_total': 20, ...}
2025-10-12 10:30:20 - INFO - ✓ PoolMappingTask succeeded in 20.50s
2025-10-12 10:30:20 - INFO -   - Pairs: 18/20
2025-10-12 10:30:20 - INFO -   - Pools found: 54
```

### 五、与其他任务集成

#### 1. 作为前置依赖

如果DEX数据下载任务依赖池子映射：

```yaml
tasks:
  base_pool_mapping:
    # ... 池子映射配置
    
  base_dex_downloader:
    enabled: true
    task_class: app.tasks.data_collection.dex_candles_downloader.DEXCandlesDownloader
    
    # 依赖池子映射任务
    dependencies:
      - task_name: base_pool_mapping
        on_success: true  # 只在池子映射成功后运行
    
    config:
      # 从映射文件读取池子地址
      mapping_file: "app/data/processed/pool_mappings/base_gate_io_pool_map.parquet"
```

#### 2. 读取映射数据

在下游任务中使用映射：

```python
from core.data_paths import data_paths
import pandas as pd

class DEXCandlesDownloader(BaseTask):
    async def execute(self, context):
        # 读取池子映射
        mapping_file = data_paths.processed_dir / 'pool_mappings' / 'base_gate_io_pool_map.parquet'
        mapping_df = pd.read_parquet(mapping_file)
        
        # 获取所有rank=1的池子
        top_pools = mapping_df[mapping_df['rank'] == 1]
        
        # 下载这些池子的数据
        for _, pool in top_pools.iterrows():
            await self.download_pool_data(
                pool['pool_address'],
                pool['network_id']
            )
```

---

## 📚 七、相关资源

### 文档链接

- [GeckoTerminal API参考](GECKOTERMINAL_API_REFERENCE.md)
- [GeckoTerminal API使用指南](GECKOTERMINAL_API_USAGE.md)
- [数据收集系统指南](DATA_COLLECTION_GUIDE.md)

### API文档

- [GeckoTerminal官方文档](https://www.geckoterminal.com/dex-api)
- [geckoterminal-py GitHub](https://github.com/dineshpinto/geckoterminal-py)

### 支持

遇到问题？
1. 查看本文档的故障排除章节
2. 检查`logs/pool_mapping.log`日志
3. 查看原始JSON响应文件分析问题

---

**最后更新:** 2025-10-12

