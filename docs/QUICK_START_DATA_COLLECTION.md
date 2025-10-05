# 🚀 QuantsLab 数据收集 - 5分钟快速上手

## 📋 前置要求

✅ 已安装 QuantsLab (`./install.sh`)  
✅ 已启动 MongoDB (`make run-db` 或 `docker compose -f docker-compose-db.yml up -d`)  
✅ 已激活 conda 环境 (`conda activate quants-lab`)

---

## 🎯 快速测试（3步走）

### 步骤 1: 测试下载 BTC 数据

直接运行内置的测试命令：

```bash
cd /Users/alice/Dropbox/投资/量化交易/quants-lab

python cli.py run app.tasks.data_collection.simple_candles_downloader
```

这会下载 BTC-USDT 和 ETH-USDT 的 15 分钟 K线数据（使用内置默认配置）。

---

### 步骤 2: 检查下载的数据

```bash
# 查看生成的文件
ls -lh app/data/cache/candles/

# 应该看到类似这样的文件：
# binance_perpetual|BTC-USDT|15m.parquet
# binance_perpetual|ETH-USDT|15m.parquet
```

---

### 步骤 3: 在 Jupyter 中加载数据

```bash
# 启动 Jupyter Lab
jupyter lab
```

在 Notebook 中运行：

```python
import pandas as pd
from core.data_paths import data_paths

# 读取 BTC 数据
btc_candles = pd.read_parquet(
    data_paths.get_candles_path("binance_perpetual|BTC-USDT|15m.parquet")
)

# 查看数据
print(f"数据行数: {len(btc_candles)}")
print(f"时间范围: {btc_candles['timestamp'].min()} 到 {btc_candles['timestamp'].max()}")
btc_candles.head()
```

**恭喜！你已经成功下载并访问了第一批数据！** 🎉

---

## 🎨 实战示例

### 示例 1: 下载多个交易对的数据

创建配置文件 `config/my_first_download.yml`:

```yaml
tasks:
  my_downloader:
    enabled: true
    task_class: app.tasks.data_collection.simple_candles_downloader.SimpleCandlesDownloader
    
    schedule:
      type: frequency
      frequency_hours: 999  # 设置很大，避免自动重复
    
    config:
      connector_name: "binance_perpetual"
      trading_pairs:
        - "BTC-USDT"
        - "ETH-USDT"
        - "SOL-USDT"
        - "BNB-USDT"
      intervals: ["15m", "1h"]
      days_data_retention: 30
```

运行：
```bash
python cli.py trigger-task --task my_downloader --config my_first_download.yml
```

---

### 示例 2: 定期自动下载（每2小时）

修改配置中的 `schedule`:

```yaml
schedule:
  type: frequency
  frequency_hours: 2.0  # 每2小时运行一次
```

持续运行：
```bash
# 前台运行（可以看到日志）
python cli.py run-tasks --config my_first_download.yml

# 后台运行
nohup python cli.py run-tasks --config my_first_download.yml > logs/data_download.log 2>&1 &
```

---

### 示例 3: 使用 Cron 调度（每天凌晨2点）

```yaml
schedule:
  type: cron
  cron: "0 2 * * *"    # 每天 02:00 UTC
  timezone: "UTC"
```

---

### 示例 4: 下载 DEX 池子数据

创建 `config/solana_pools.yml`:

```yaml
tasks:
  solana_pools:
    enabled: true
    task_class: app.tasks.data_collection.pools_screener.PoolsScreenerTask
    
    schedule:
      type: frequency
      frequency_hours: 1.0  # 每小时
    
    config:
      network: "solana"
      quote_asset: "SOL"
      min_volume_24h: 100000
      min_liquidity: 50000
      min_transactions_24h: 200
```

运行：
```bash
python cli.py trigger-task --task solana_pools --config solana_pools.yml
```

查看结果（在 MongoDB）：
```python
from core.database_manager import db_manager
import asyncio

async def view_pools():
    mongo = await db_manager.get_mongodb_client()
    pools = await mongo.find_documents("pools", {}, limit=10)
    return pools

# 在 Jupyter 中运行
pools = await view_pools()
print(f"找到 {len(pools)} 个池子")
```

---

## 📊 数据分析示例

### 在 Notebook 中分析 K线数据

```python
import pandas as pd
import plotly.graph_objects as go
from core.data_paths import data_paths

# 1. 加载数据
btc_df = pd.read_parquet(
    data_paths.get_candles_path("binance_perpetual|BTC-USDT|1h.parquet")
)

# 2. 转换时间戳
btc_df['datetime'] = pd.to_datetime(btc_df['timestamp'], unit='s')
btc_df.set_index('datetime', inplace=True)

# 3. 计算简单移动平均线
btc_df['SMA_20'] = btc_df['close'].rolling(window=20).mean()
btc_df['SMA_50'] = btc_df['close'].rolling(window=50).mean()

# 4. 绘制蜡烛图
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=btc_df.index,
    open=btc_df['open'],
    high=btc_df['high'],
    low=btc_df['low'],
    close=btc_df['close'],
    name='BTC-USDT'
))

fig.add_trace(go.Scatter(
    x=btc_df.index,
    y=btc_df['SMA_20'],
    name='SMA 20',
    line=dict(color='orange', width=1)
))

fig.add_trace(go.Scatter(
    x=btc_df.index,
    y=btc_df['SMA_50'],
    name='SMA 50',
    line=dict(color='blue', width=1)
))

fig.update_layout(
    title='BTC-USDT 价格走势',
    yaxis_title='价格 (USDT)',
    xaxis_title='时间',
    height=600
)

fig.show()

# 5. 基本统计
print("\n基本统计信息:")
print(f"数据点数: {len(btc_df)}")
print(f"时间范围: {btc_df.index.min()} 到 {btc_df.index.max()}")
print(f"最高价: ${btc_df['high'].max():,.2f}")
print(f"最低价: ${btc_df['low'].min():,.2f}")
print(f"平均价: ${btc_df['close'].mean():,.2f}")
print(f"总交易量: {btc_df['volume'].sum():,.2f} BTC")
```

---

## 🔧 常用命令速查

### 任务管理

```bash
# 列出配置中的所有任务
python cli.py list-tasks --config my_config.yml

# 验证配置文件
python cli.py validate-config --config my_config.yml

# 单次触发任务
python cli.py trigger-task --task task_name --config my_config.yml

# 持续运行任务（按调度）
python cli.py run-tasks --config my_config.yml
```

### 数据检查

```bash
# 查看已下载的数据文件
ls -lh app/data/cache/candles/

# 统计文件数量
ls app/data/cache/candles/ | wc -l

# 查看最新下载的文件
ls -lt app/data/cache/candles/ | head -10

# 检查文件大小
du -sh app/data/cache/candles/
```

### Docker 数据库管理

```bash
# 启动数据库
make run-db
# 或
docker compose -f docker-compose-db.yml up -d

# 停止数据库
make stop-db

# 查看容器状态
docker ps

# 查看 MongoDB 日志
docker logs mongodb
```

---

## 🐛 故障排查

### 问题 1: 找不到交易对
```
KeyError: 'BTC-USDT'
```

**解决方案**: 检查交易对格式，不同交易所格式可能不同
```python
# 查看可用的交易对
from core.data_sources import CLOBDataSource
clob = CLOBDataSource()
rules = await clob.get_trading_rules("binance_perpetual")
print(rules.get_all_trading_pairs()[:10])
```

### 问题 2: MongoDB 连接失败
```
MongoDB connection error
```

**解决方案**:
```bash
# 1. 确认 MongoDB 正在运行
docker ps | grep mongodb

# 2. 检查环境变量
cat .env | grep MONGO

# 3. 测试连接
python -c "from core.database_manager import db_manager; import asyncio; asyncio.run(db_manager.get_mongodb_client())"
```

### 问题 3: 数据文件不存在
```
FileNotFoundError: app/data/cache/candles/...
```

**解决方案**:
```bash
# 确保目录存在
mkdir -p app/data/cache/candles

# 重新下载数据
python cli.py trigger-task --task your_task --config your_config.yml
```

---

## 📚 下一步学习

- ✅ [完整数据收集指南](./DATA_COLLECTION_GUIDE.md) - 深入理解所有功能
- ✅ [数据流程详解](./DATA_COLLECTION_FLOW.md) - 了解内部工作原理
- ✅ [回测引擎使用](../README.md#research--development) - 使用数据进行策略回测
- ✅ [策略开发教程](../research_notebooks/) - 查看示例 Notebooks

---

## 💡 小技巧

### 技巧 1: 使用别名简化命令
在 `~/.zshrc` 或 `~/.bashrc` 中添加:
```bash
alias ql-run='python /path/to/quants-lab/cli.py run-tasks --config'
alias ql-trigger='python /path/to/quants-lab/cli.py trigger-task --config'
alias ql-list='python /path/to/quants-lab/cli.py list-tasks --config'
```

### 技巧 2: 创建测试脚本
```python
# test_download.py
import asyncio
from app.tasks.data_collection.simple_candles_downloader import SimpleCandlesDownloader
from core.tasks.base import TaskConfig, ScheduleConfig

async def main():
    config = TaskConfig(
        name="test",
        task_class="...",
        schedule=ScheduleConfig(type="frequency", frequency_hours=1.0),
        config={
            "connector_name": "binance_perpetual",
            "trading_pairs": ["BTC-USDT"],
            "intervals": ["15m"],
            "days_data_retention": 7
        }
    )
    
    task = SimpleCandlesDownloader(config)
    result = await task.run()
    print(result)

asyncio.run(main())
```

### 技巧 3: 监控任务运行
```bash
# 实时查看日志
tail -f logs/task_runner.log

# 监控文件变化
watch -n 5 'ls -lh app/data/cache/candles/ | tail -10'
```

---

**Happy Data Collecting! 📊✨**

如有问题，请查看 [完整文档](./DATA_COLLECTION_GUIDE.md) 或提交 GitHub Issue。

