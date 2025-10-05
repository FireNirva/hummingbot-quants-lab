# 📊 QuantsLab 数据收集系统完整指南

## 🏗️ 一、系统架构总览

### 核心组件关系图

```
┌─────────────────────────────────────────────────────────────────┐
│                    任务配置文件 (YAML)                            │
│  - 定义任务参数                                                    │
│  - 配置调度规则                                                    │
│  - 设置依赖关系                                                    │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TaskRunner (任务运行器)                        │
│  - 加载配置文件                                                    │
│  - 初始化任务实例                                                  │
│  - 管理 TaskOrchestrator                                         │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                 TaskOrchestrator (任务编排器)                     │
│  - 任务调度 (Cron/频率)                                           │
│  - 依赖管理                                                        │
│  - 并发控制                                                        │
│  - 重试机制                                                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BaseTask (任务基类)                             │
│  生命周期钩子：                                                    │
│  1. setup()      - 任务初始化                                     │
│  2. execute()    - 核心业务逻辑                                   │
│  3. cleanup()    - 资源清理                                       │
│  4. on_success() - 成功回调                                       │
│  5. on_failure() - 失败回调                                       │
│  6. on_retry()   - 重试回调                                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌──────────────────┐        ┌──────────────────┐
│ 数据收集任务      │        │   其他任务类型    │
│                  │        │                  │
│ - Candles下载    │        │ - 回测任务        │
│ - Pools筛选      │        │ - 优化任务        │
│ - 资金费率       │        │ - Notebook执行    │
│ - Trades数据     │        │ - 部署任务        │
└──────────────────┘        └──────────────────┘
```

---

## 📦 二、数据收集任务类型详解

### 1. CandlesDownloaderTask (K线数据下载)

**功能**: 从中心化交易所下载所有交易对的K线数据并缓存为 Parquet 文件

**核心代码位置**: `app/tasks/data_collection/candles_downloader_task.py`

**工作流程**:
```python
1. 初始化 CLOBDataSource
2. 获取交易所的所有交易规则 (get_trading_rules)
3. 遍历所有交易对和时间间隔
4. 调用 CLOB.get_candles() 获取数据
5. 自动缓存到 Parquet 文件
6. 返回统计信息
```

**配置参数**:
```yaml
config:
  connector_name: "binance_perpetual"  # 交易所名称
  quote_asset: "USDT"                  # 报价资产
  intervals: ["1m", "15m", "1h"]       # 时间间隔
  days_data_retention: 30              # 数据保留天数
  min_notional_size: 10                # 最小名义价值
```

**数据存储路径**: `app/data/cache/candles/`
- 文件命名格式: `{connector}|{pair}|{interval}.parquet`
- 例如: `binance_perpetual|BTC-USDT|15m.parquet`

---

### 2. SimpleCandlesDownloader (指定交易对K线下载)

**功能**: 只下载指定交易对的K线数据（更快速、更精确）

**核心代码位置**: `app/tasks/data_collection/simple_candles_downloader.py`

**与 CandlesDownloaderTask 的区别**:
- ✅ 不需要获取所有交易对
- ✅ 速度更快，适合特定策略
- ✅ 配置更简单

**配置参数**:
```yaml
config:
  connector_name: "binance_perpetual"
  trading_pairs: ["BTC-USDT", "ETH-USDT", "SOL-USDT"]  # 指定交易对
  intervals: ["15m", "1h"]
  days_data_retention: 7
```

---

### 3. PoolsScreenerTask (流动性池筛选)

**功能**: 从 GeckoTerminal 获取 DEX 池子数据并筛选

**核心代码位置**: `app/tasks/data_collection/pools_screener.py`

**工作流程**:
```python
1. 初始化 GeckoTerminalAsyncClient
2. 获取 Top Pools 和 New Pools
3. 清洗数据（计算流动性比率等）
4. 按条件筛选池子
5. 存储到 MongoDB
```

**配置参数**:
```yaml
config:
  network: "solana"              # 区块链网络
  quote_asset: "SOL"             # 报价资产
  min_pool_age_days: 2           # 最小池龄
  min_fdv: 70000                 # 最小 FDV
  max_fdv: 5000000               # 最大 FDV
  min_volume_24h: 150000         # 最小 24h 交易量
  min_liquidity: 50000           # 最小流动性
  min_transactions_24h: 300      # 最小 24h 交易数
```

**数据存储**: MongoDB `quants_lab.pools` 集合

---

## 🔧 三、核心数据源详解

### CLOBDataSource (中心化订单簿数据源)

**位置**: `core/data_sources/clob.py`

**核心功能**:
1. **自动缓存管理**: Parquet 文件读写
2. **智能数据合并**: 增量更新已有数据
3. **多交易所支持**: 支持所有 Hummingbot CLOB 连接器
4. **数据验证**: 自动过滤无效数据

**关键方法**:
```python
# 获取K线数据（自动缓存）
candles = await clob.get_candles(
    connector_name="binance_perpetual",
    trading_pair="BTC-USDT", 
    interval="15m",
    start_time=start_timestamp,
    end_time=end_timestamp
)

# 保存缓存到文件
clob.dump_candles_cache()

# 从缓存加载数据
candles = clob.get_candles_from_cache(
    connector_name="binance_perpetual",
    trading_pair="BTC-USDT",
    interval="15m"
)
```

**支持的交易所**:
- Binance / Binance Perpetual
- OKX / OKX Perpetual
- Bybit / Bybit Perpetual
- Gate.io
- 等等（排除部分不稳定连接器）

---

## ⚙️ 四、任务系统工作原理

### 任务生命周期

```python
┌─────────────┐
│  配置加载    │  TaskRunner 读取 YAML
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 任务初始化   │  创建 Task 实例
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 调度检查     │  Orchestrator 检查是否该运行
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ setup()     │  初始化资源（DB、API 客户端等）
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ execute()   │  执行核心业务逻辑
└──────┬──────┘
       │
       ├─ 成功 ──→ on_success()
       │
       ├─ 失败 ──→ on_failure() ──→ 重试？──→ on_retry()
       │
       ▼
┌─────────────┐
│ cleanup()   │  清理资源
└─────────────┘
```

### 调度机制

#### 1. 频率调度 (Frequency)
```yaml
schedule:
  type: frequency
  frequency_hours: 2.0  # 每 2 小时运行一次
```

#### 2. Cron 调度
```yaml
schedule:
  type: cron
  cron: "0 */6 * * *"   # 每 6 小时整点运行
  timezone: "UTC"
```

#### 3. 依赖触发
```yaml
dependencies:
  - task_name: "candles_downloader"
    on_completion: true      # 任意完成状态触发
    # on_success: true       # 仅成功时触发
    # on_failure: true       # 仅失败时触发
    delay_seconds: 300       # 延迟 5 分钟
```

---

## 📝 五、如何创建数据收集配置

### 示例 1: 基础 K线下载配置

```yaml
# config/my_candles_downloader.yml

tasks:
  btc_eth_candles:
    enabled: true
    task_class: app.tasks.data_collection.simple_candles_downloader.SimpleCandlesDownloader
    
    schedule:
      type: frequency
      frequency_hours: 1.0  # 每小时运行
    
    max_retries: 3
    retry_delay_seconds: 60
    timeout_seconds: 600
    
    config:
      connector_name: "binance_perpetual"
      trading_pairs:
        - "BTC-USDT"
        - "ETH-USDT"
        - "SOL-USDT"
      intervals: ["15m", "1h"]
      days_data_retention: 7
```

**运行命令**:
```bash
# 方法1: 持续运行（按调度）
python cli.py run-tasks --config my_candles_downloader.yml

# 方法2: 单次触发
python cli.py trigger-task --task btc_eth_candles --config my_candles_downloader.yml

# 方法3: 直接运行（使用内置默认配置）
python cli.py run app.tasks.data_collection.simple_candles_downloader
```

---

### 示例 2: 多数据源组合配置

```yaml
# config/multi_source_data.yml

tasks:
  # 任务1: 下载K线
  candles_downloader:
    enabled: true
    task_class: app.tasks.data_collection.candles_downloader_task.CandlesDownloaderTask
    
    schedule:
      type: frequency
      frequency_hours: 2.0
    
    config:
      connector_name: "binance_perpetual"
      quote_asset: "USDT"
      intervals: ["15m", "1h"]
      days_data_retention: 14
    
    tags:
      - data_collection
      - candles

  # 任务2: 筛选池子（独立运行）
  solana_pools:
    enabled: true
    task_class: app.tasks.data_collection.pools_screener.PoolsScreenerTask
    
    schedule:
      type: frequency
      frequency_hours: 1.0
    
    config:
      network: "solana"
      quote_asset: "SOL"
      min_volume_24h: 100000
      min_liquidity: 50000
    
    tags:
      - data_collection
      - pools
```

---

### 示例 3: 带依赖关系的配置

```yaml
# config/candles_with_analysis.yml

tasks:
  # 主任务: 下载数据
  download_candles:
    enabled: true
    task_class: app.tasks.data_collection.simple_candles_downloader.SimpleCandlesDownloader
    
    schedule:
      type: frequency
      frequency_hours: 4.0  # 每4小时
    
    config:
      connector_name: "binance_perpetual"
      trading_pairs: ["BTC-USDT", "ETH-USDT"]
      intervals: ["15m"]
      days_data_retention: 30
    
    tags:
      - data_collection

  # 依赖任务: 数据下载完成后自动运行分析
  analyze_volatility:
    enabled: true
    task_class: app.tasks.screeners.volume_volatility_screener_task.VolumeVolatilityScreenerTask
    
    # 不设置 schedule，仅通过依赖触发
    dependencies:
      - task_name: "download_candles"
        on_success: true       # 仅在成功时触发
        delay_seconds: 60      # 等待1分钟
    
    config:
      connector_name: "binance_perpetual"
      interval: "15m"
      days: 30
    
    tags:
      - analysis
```

---

## 🚀 六、实战演练

### 场景1: 快速下载 BTC 和 ETH 数据

**步骤1**: 创建配置文件
```bash
cat > config/quick_btc_eth.yml << 'EOF'
tasks:
  quick_download:
    enabled: true
    task_class: app.tasks.data_collection.simple_candles_downloader.SimpleCandlesDownloader
    
    schedule:
      type: frequency
      frequency_hours: 999  # 设置很大避免自动重复
    
    config:
      connector_name: "binance_perpetual"
      trading_pairs: ["BTC-USDT", "ETH-USDT"]
      intervals: ["15m", "1h", "4h"]
      days_data_retention: 30
EOF
```

**步骤2**: 运行任务
```bash
python cli.py trigger-task --task quick_download --config quick_btc_eth.yml
```

**步骤3**: 检查数据
```bash
ls -lh app/data/cache/candles/ | grep "BTC-USDT\|ETH-USDT"
```

---

### 场景2: 每日自动收集多交易所数据

**配置文件**: `config/daily_multi_exchange.yml`
```yaml
tasks:
  binance_daily:
    enabled: true
    task_class: app.tasks.data_collection.candles_downloader_task.CandlesDownloaderTask
    
    schedule:
      type: cron
      cron: "0 0 * * *"  # 每天 UTC 00:00
      timezone: "UTC"
    
    config:
      connector_name: "binance_perpetual"
      quote_asset: "USDT"
      intervals: ["1d"]
      days_data_retention: 365
    
    tags:
      - daily
      - binance

  okx_daily:
    enabled: true
    task_class: app.tasks.data_collection.candles_downloader_task.CandlesDownloaderTask
    
    schedule:
      type: cron
      cron: "0 1 * * *"  # 每天 UTC 01:00 (错开时间)
      timezone: "UTC"
    
    config:
      connector_name: "okx_perpetual"
      quote_asset: "USDT"
      intervals: ["1d"]
      days_data_retention: 365
    
    tags:
      - daily
      - okx
```

**运行**:
```bash
# 后台持续运行
nohup python cli.py run-tasks --config daily_multi_exchange.yml > logs/daily.log 2>&1 &
```

---

## 💡 七、常见问题与最佳实践

### Q1: 数据存储在哪里？

**K线数据**: `app/data/cache/candles/`
- 格式: Parquet 文件
- 命名: `{connector}|{pair}|{interval}.parquet`

**池子数据**: MongoDB `quants_lab.pools` 集合

**回测结果**: `app/data/processed/backtesting/`

### Q2: 如何避免重复下载数据？

CLOBDataSource 自动处理缓存：
1. 检查本地 Parquet 文件
2. 如果数据存在且时间范围覆盖，直接读取
3. 如果需要更新，只下载缺失部分
4. 自动合并新旧数据

### Q3: 任务失败后会怎样？

```yaml
max_retries: 3              # 最多重试3次
retry_delay_seconds: 60     # 每次重试间隔60秒
```

任务会：
1. 调用 `on_failure()` 钩子
2. 等待 `retry_delay_seconds`
3. 调用 `on_retry()` 钩子
4. 重新执行 `execute()`
5. 重复直到成功或达到 `max_retries`

### Q4: 如何监控任务运行状态？

**方法1**: 查看日志
```bash
tail -f logs/task_runner.log
```

**方法2**: 使用 API（如果启用）
```bash
# 启用 API
python cli.py serve --config my_config.yml --port 8000

# 查询任务状态
curl http://localhost:8000/tasks
curl http://localhost:8000/tasks/candles_downloader
```

**方法3**: 查询 MongoDB
```python
from core.database_manager import db_manager
mongo = await db_manager.get_mongodb_client()
tasks = await mongo.find_documents("task_executions", {})
```

### Q5: 如何优化下载速度？

1. **使用 SimpleCandlesDownloader** 而不是 CandlesDownloaderTask（针对特定交易对）
2. **减少时间间隔数量** （只下载需要的，如 ["1h"]）
3. **减少数据保留天数** （从 365 改为 30）
4. **增加并发数**:
   ```yaml
   max_concurrent_tasks: 5  # 在 config 顶层设置
   ```

---

## 🔍 八、调试技巧

### 1. 测试单个任务

任务文件底部都有 `main()` 函数，可以直接运行：
```bash
cd /path/to/quants-lab
python -m app.tasks.data_collection.simple_candles_downloader
```

### 2. 验证配置文件

```bash
python cli.py validate-config --config my_config.yml
```

### 3. 列出所有任务

```bash
python cli.py list-tasks --config my_config.yml
```

### 4. 查看可用连接器

```bash
python list_connectors.py
```

---

## 📚 九、参考资料

### 关键文件路径

```
核心任务系统:
├── core/tasks/base.py           # BaseTask 基类
├── core/tasks/orchestrator.py   # 任务编排器
├── core/tasks/runner.py         # 任务运行器
└── core/tasks/storage.py        # 任务状态存储

数据收集任务:
├── app/tasks/data_collection/
│   ├── candles_downloader_task.py       # 全量K线下载
│   ├── simple_candles_downloader.py     # 指定交易对K线
│   ├── pools_screener.py                # 池子筛选
│   ├── funding_rates_task.py            # 资金费率
│   └── trades_downloader_task.py        # 交易数据

数据源:
├── core/data_sources/clob.py            # CLOB数据源
└── core/services/okx_dex_api.py         # OKX DEX API

配置示例:
├── config/template_1_candles_optimization.yml
├── config/template_2_candles_pools_screener.yml
└── config/template_3_periodic_reports.yml
```

### 环境变量配置 (.env)

```bash
# MongoDB (用于存储池子数据和任务状态)
MONGO_URI=mongodb://admin:admin@localhost:27017
MONGO_DATABASE=quants_lab

# 任务系统 API
TASK_API_ENABLED=false
TASK_API_HOST=0.0.0.0
TASK_API_PORT=8000

# 通知系统
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## 🎯 十、下一步行动

1. ✅ 创建你的第一个配置文件
2. ✅ 运行一个简单的数据下载任务
3. ✅ 检查生成的 Parquet 文件
4. ✅ 在 Jupyter Notebook 中加载和分析数据
5. ✅ 创建自己的自定义数据收集任务

**祝你数据收集愉快！📊✨**

