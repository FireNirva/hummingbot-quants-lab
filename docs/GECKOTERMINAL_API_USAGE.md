# GeckoTerminal API 使用指南

本文档说明项目中如何使用 GeckoTerminal API，以及如何扩展支持历史 OHLCV K线数据下载。

---

## 📊 当前使用的 API Endpoints

### Pool Screener 使用的 API

**文件：** `app/tasks/data_collection/pools_screener.py`

```python
# 第 113-114 行
top_pools = await self.gt.get_top_pools_by_network(self.network)
new_pools = await self.gt.get_new_pools_by_network(self.network)
```

#### 1. Get Top Pools

**API Endpoint:**
```
GET /networks/{network}/pools
```

**对应的 Python 方法:**
```python
await gt.get_top_pools_by_network("base")
```

**返回数据：**
- 返回指定网络上交易最活跃的池子（默认按 24h 交易笔数排序）
- 最多返回 20 个池子（每页）
- 包含完整的池子信息（价格、流动性、交易量等）

**排序选项：**
- `h24_tx_count_desc`（默认）- 按 24小时交易笔数降序
- `h24_volume_usd_desc` - 按 24小时交易量降序

#### 2. Get New Pools

**API Endpoint:**
```
GET /networks/{network}/new_pools
```

**对应的 Python 方法:**
```python
await gt.get_new_pools_by_network("base")
```

**返回数据：**
- 返回指定网络上最新创建的池子
- 最多返回 20 个池子（每页）
- 按创建时间降序排列

### 返回的池子数据结构

每个池子包含以下关键字段：

```json
{
  "id": "base_uniswap-v3_0x4c36388be6f416a29c8d8eee81c771ce6be14b18",
  "type": "pool",
  "name": "WETH / USDC 0.01%",
  "address": "0x4c36388be6f416a29c8d8eee81c771ce6be14b18",
  "base_token_price_usd": "3260.45",
  "quote_token_price_usd": "1.0",
  "reserve_in_usd": "8326274.123",
  "fdv_usd": "784144285.456",
  "volume_usd_h24": "158589434.234",
  "transactions_h24_buys": 12345,
  "transactions_h24_sells": 11234,
  "price_change_percentage_h1": 0.52,
  "price_change_percentage_h24": 2.34,
  "pool_created_at": "2023-08-15T10:30:00Z",
  "dex_id": "uniswap-v3-base"
}
```

---

## 📈 添加 OHLCV K线数据下载功能

### 需要使用的 API

**API Endpoint:**
```
GET /networks/{network}/pools/{pool_address}/ohlcv/{timeframe}
```

### API 详细参数

#### 必需参数

| 参数 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| `network` | string | 网络 ID | `base`, `eth`, `solana` |
| `pool_address` | string | 池子地址 | `0x4c36388be6f416a29c8d8eee81c771ce6be14b18` |
| `timeframe` | string | 时间框架 | `day`, `hour`, `minute` |

#### 可选参数

| 参数 | 类型 | 说明 | 可选值 | 默认值 |
|-----|------|------|-------|-------|
| `aggregate` | string | 聚合周期 | day: `1`<br>hour: `1`, `4`, `12`<br>minute: `1`, `5`, `15` | `1` |
| `before_timestamp` | string | 返回此时间戳之前的数据 | Unix 时间戳（秒） | 当前时间 |
| `limit` | string | 返回的 OHLCV 数量 | `1-1000` | `100` |
| `currency` | string | 返回价格的货币单位 | `usd`, `token` | `usd` |
| `token` | string | 返回的代币 | `base`, `quote`, 或代币地址 | `base` |

### API 限制

- ⏰ **历史数据范围**：最多 6 个月
- 📊 **单次最大返回**：1000 条 OHLCV 数据
- 🔄 **更新频率**：数据缓存 1 分钟
- 🚫 **不支持**：超过 2 个代币的池子（如 Balancer 池）

### 返回数据格式

```json
{
  "data": {
    "id": "base_uniswap-v3_0x4c36388be6f416a29c8d8eee81c771ce6be14b18",
    "type": "pool_ohlcv",
    "attributes": {
      "ohlcv_list": [
        [
          1708498800,      // Unix 时间戳（秒）
          2955.65,         // Open（开盘价）
          2955.65,         // High（最高价）
          2933.98,         // Low（最低价）
          2934.24,         // Close（收盘价）
          131664.76        // Volume（交易量）
        ],
        // ... 更多 K线数据
      ]
    }
  },
  "meta": {
    "base": {
      "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
      "name": "Wrapped Ether",
      "symbol": "WETH"
    },
    "quote": {
      "address": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
      "name": "USD Coin",
      "symbol": "USDC"
    }
  }
}
```

### OHLCV 数组格式

每个 OHLCV 数据是一个包含 6 个元素的数组：

```python
[
    timestamp,  # 0: Unix 时间戳（秒）
    open,       # 1: 开盘价
    high,       # 2: 最高价
    low,        # 3: 最低价
    close,      # 4: 收盘价
    volume      # 5: 交易量
]
```

---

## 🛠️ 实现建议

### 方案 1：创建新的 OHLCV 下载任务

**推荐理由：**
- ✅ 与现有的 candles_downloader_task.py 结构一致
- ✅ 可以复用任务系统的调度、重试、错误处理机制
- ✅ 数据存储在 Parquet 文件中（与 CLOB 数据一致）

**实现步骤：**

#### 1. 创建任务类

**文件位置：** `app/tasks/data_collection/dex_ohlcv_downloader.py`

```python
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from typing import Dict, Any, List

from geckoterminal_py import GeckoTerminalAsyncClient
from core.tasks import BaseTask, TaskContext
from core.data_paths import DataPaths

class DexOhlcvDownloaderTask(BaseTask):
    """
    下载 DEX 池子的历史 OHLCV 数据
    
    配置参数：
    - network: 网络 ID（如 'base', 'ethereum', 'solana'）
    - pools: 池子地址列表
    - intervals: 时间间隔列表（如 ['1m', '5m', '15m', '1h', '4h', '1d']）
    - lookback_days: 回溯天数（最多 180 天）
    - save_to_parquet: 是否保存为 Parquet 文件（默认 True）
    """
    
    def __init__(self, config):
        super().__init__(config)
        self.gt = None
        
        # 配置参数
        self.network = self.config.config.get("network", "base")
        self.pools = self.config.config.get("pools", [])
        self.intervals = self.config.config.get("intervals", ["15m", "1h", "4h", "1d"])
        self.lookback_days = min(self.config.config.get("lookback_days", 30), 180)
        self.save_to_parquet = self.config.config.get("save_to_parquet", True)
        
        # 数据路径
        self.data_paths = DataPaths()
        
    async def setup(self, context: TaskContext) -> None:
        """初始化 GeckoTerminal 客户端"""
        await super().setup(context)
        self.gt = GeckoTerminalAsyncClient()
        logging.info(f"DexOhlcvDownloader setup for network: {self.network}")
    
    def _convert_interval_to_api_params(self, interval: str) -> tuple:
        """
        转换间隔格式为 GeckoTerminal API 参数
        
        Args:
            interval: 如 '15m', '1h', '4h', '1d'
            
        Returns:
            (timeframe, aggregate): 如 ('minute', '15'), ('hour', '4'), ('day', '1')
        """
        interval_map = {
            '1m': ('minute', '1'),
            '5m': ('minute', '5'),
            '15m': ('minute', '15'),
            '1h': ('hour', '1'),
            '4h': ('hour', '4'),
            '12h': ('hour', '12'),
            '1d': ('day', '1'),
        }
        
        if interval not in interval_map:
            raise ValueError(f"Unsupported interval: {interval}. Supported: {list(interval_map.keys())}")
        
        return interval_map[interval]
    
    async def _fetch_ohlcv_chunk(
        self, 
        pool_address: str, 
        timeframe: str, 
        aggregate: str,
        before_timestamp: int = None
    ) -> pd.DataFrame:
        """
        获取一个 chunk 的 OHLCV 数据（最多 1000 条）
        
        Returns:
            DataFrame with columns: [timestamp, open, high, low, close, volume]
        """
        try:
            # 调用 GeckoTerminal API
            # 注意：需要检查 geckoterminal_py 库是否支持此 API
            # 如果不支持，需要直接调用 HTTP API
            
            params = {
                'aggregate': aggregate,
                'limit': '1000',
                'currency': 'usd'
            }
            
            if before_timestamp:
                params['before_timestamp'] = str(before_timestamp)
            
            # 这里假设库支持此方法，如果不支持需要自己实现
            response = await self.gt.get_pool_ohlcv(
                network=self.network,
                pool_address=pool_address,
                timeframe=timeframe,
                **params
            )
            
            # 解析响应
            ohlcv_list = response['data']['attributes']['ohlcv_list']
            
            # 转换为 DataFrame
            df = pd.DataFrame(
                ohlcv_list,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            
            # 转换时间戳为 datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df['date'] = df['timestamp'].dt.date
            
            return df
            
        except Exception as e:
            logging.error(f"Error fetching OHLCV for {pool_address}: {e}")
            return pd.DataFrame()
    
    async def _fetch_full_ohlcv(
        self, 
        pool_address: str, 
        interval: str,
        lookback_days: int
    ) -> pd.DataFrame:
        """
        获取完整的历史 OHLCV 数据（可能需要多次请求）
        
        Args:
            pool_address: 池子地址
            interval: 时间间隔（如 '15m'）
            lookback_days: 回溯天数
            
        Returns:
            完整的 OHLCV DataFrame
        """
        timeframe, aggregate = self._convert_interval_to_api_params(interval)
        
        all_data = []
        before_timestamp = None
        target_timestamp = int((datetime.now() - timedelta(days=lookback_days)).timestamp())
        
        logging.info(f"Fetching {interval} OHLCV for {pool_address[:10]}... (last {lookback_days} days)")
        
        # 循环获取数据，直到达到目标时间或没有更多数据
        while True:
            df_chunk = await self._fetch_ohlcv_chunk(
                pool_address=pool_address,
                timeframe=timeframe,
                aggregate=aggregate,
                before_timestamp=before_timestamp
            )
            
            if df_chunk.empty:
                break
            
            all_data.append(df_chunk)
            
            # 获取最早的时间戳
            earliest_timestamp = int(df_chunk['timestamp'].min().timestamp())
            
            # 检查是否已达到目标时间
            if earliest_timestamp <= target_timestamp:
                break
            
            # 检查是否已获取所有可用数据（API 返回少于 1000 条）
            if len(df_chunk) < 1000:
                break
            
            # 设置下一次请求的时间戳
            before_timestamp = earliest_timestamp
            
            # 避免请求过快
            await asyncio.sleep(0.5)
        
        if not all_data:
            logging.warning(f"No OHLCV data found for {pool_address}")
            return pd.DataFrame()
        
        # 合并所有数据
        df_full = pd.concat(all_data, ignore_index=True)
        
        # 去重并排序
        df_full = df_full.drop_duplicates(subset=['timestamp']).sort_values('timestamp')
        
        # 过滤到目标时间范围
        df_full = df_full[df_full['timestamp'] >= pd.Timestamp(target_timestamp, unit='s')]
        
        logging.info(f"  ✓ Fetched {len(df_full)} {interval} candles")
        
        return df_full
    
    async def _save_to_parquet(
        self, 
        df: pd.DataFrame, 
        pool_address: str, 
        interval: str
    ):
        """保存数据到 Parquet 文件"""
        try:
            # 创建目录结构: data/dex_candles/{network}/{pool_address}/
            output_dir = self.data_paths.dex_candles / self.network / pool_address
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 文件名: {interval}.parquet
            output_file = output_dir / f"{interval}.parquet"
            
            # 如果文件已存在，合并数据
            if output_file.exists():
                df_existing = pd.read_parquet(output_file)
                df = pd.concat([df_existing, df], ignore_index=True)
                df = df.drop_duplicates(subset=['timestamp']).sort_values('timestamp')
            
            # 保存
            df.to_parquet(output_file, index=False)
            logging.info(f"  ✓ Saved to {output_file}")
            
        except Exception as e:
            logging.error(f"Error saving to Parquet: {e}")
    
    async def execute(self, context: TaskContext) -> Dict[str, Any]:
        """主执行逻辑"""
        results = {
            "network": self.network,
            "pools_processed": 0,
            "intervals": {},
            "total_candles": 0
        }
        
        for pool_address in self.pools:
            logging.info(f"\nProcessing pool: {pool_address}")
            
            for interval in self.intervals:
                try:
                    # 获取 OHLCV 数据
                    df = await self._fetch_full_ohlcv(
                        pool_address=pool_address,
                        interval=interval,
                        lookback_days=self.lookback_days
                    )
                    
                    if df.empty:
                        continue
                    
                    # 保存到 Parquet
                    if self.save_to_parquet:
                        await self._save_to_parquet(df, pool_address, interval)
                    
                    # 更新统计
                    if interval not in results["intervals"]:
                        results["intervals"][interval] = 0
                    results["intervals"][interval] += len(df)
                    results["total_candles"] += len(df)
                    
                except Exception as e:
                    logging.error(f"Error processing {pool_address} {interval}: {e}")
            
            results["pools_processed"] += 1
        
        logging.info(f"\n✓ Download completed: {results['total_candles']} candles from {results['pools_processed']} pools")
        
        return results
```

#### 2. 添加数据路径定义

**文件：** `core/data_paths.py`

```python
# 在 DataPaths 类中添加
@property
def dex_candles(self) -> Path:
    """DEX OHLCV candles directory"""
    path = self.data_dir / "dex_candles"
    path.mkdir(parents=True, exist_ok=True)
    return path
```

#### 3. 创建配置文件

**文件：** `config/base_dex_candles_downloader.yml`

```yaml
tasks:
  base_weth_usdc_candles:
    enabled: true
    task_class: app.tasks.data_collection.dex_ohlcv_downloader.DexOhlcvDownloaderTask
    
    schedule:
      type: frequency
      frequency_hours: 1.0  # 每小时更新一次
      timezone: UTC
    
    max_retries: 3
    retry_delay_seconds: 180
    timeout_seconds: 1800  # 30 分钟超时
    
    config:
      network: "base"
      
      # 要下载的池子地址列表
      pools:
        # WETH/USDC 0.01% - Uniswap V3
        - "0x4c36388be6f416a29c8d8eee81c771ce6be14b18"
        # WETH/USDC 0.05% - Uniswap V3
        - "0xd0b53d9277642d899df5c87a3966a349a798f224"
        # cbBTC/USDC 0.01%
        - "0x7f0c8b83b935b7c6061235295c6240b8acb40076"
      
      # 时间间隔（支持：1m, 5m, 15m, 1h, 4h, 12h, 1d）
      intervals:
        - "15m"
        - "1h"
        - "4h"
        - "1d"
      
      # 回溯天数（最多 180 天，受 API 限制）
      lookback_days: 90
      
      # 保存为 Parquet 文件
      save_to_parquet: true
    
    tags:
      - data_collection
      - dex_candles
      - base
```

---

## 📝 使用示例

### 示例 1：下载单个池子的 K线数据

```python
import asyncio
from geckoterminal_py import GeckoTerminalAsyncClient

async def download_ohlcv():
    gt = GeckoTerminalAsyncClient()
    
    # 参数
    network = "base"
    pool_address = "0x4c36388be6f416a29c8d8eee81c771ce6be14b18"  # WETH/USDC 0.01%
    
    # 获取 1 小时 K线数据
    response = await gt.get_pool_ohlcv(
        network=network,
        pool_address=pool_address,
        timeframe="hour",
        aggregate="1",
        limit="1000"
    )
    
    ohlcv_list = response['data']['attributes']['ohlcv_list']
    
    # 打印前 5 条
    for candle in ohlcv_list[:5]:
        timestamp, open_price, high, low, close, volume = candle
        print(f"Time: {timestamp}, O: {open_price}, H: {high}, L: {low}, C: {close}, V: {volume}")

asyncio.run(download_ohlcv())
```

### 示例 2：获取不同时间间隔的数据

```python
intervals = {
    '15m': ('minute', '15'),
    '1h': ('hour', '1'),
    '4h': ('hour', '4'),
    '1d': ('day', '1')
}

for interval_name, (timeframe, aggregate) in intervals.items():
    response = await gt.get_pool_ohlcv(
        network="base",
        pool_address=pool_address,
        timeframe=timeframe,
        aggregate=aggregate,
        limit="100"
    )
    
    count = len(response['data']['attributes']['ohlcv_list'])
    print(f"{interval_name}: {count} candles")
```

### 示例 3：获取历史数据（分页）

```python
async def fetch_historical_data(days_back=30):
    """获取过去 N 天的数据"""
    all_candles = []
    before_timestamp = None
    target_timestamp = int((datetime.now() - timedelta(days=days_back)).timestamp())
    
    while True:
        params = {
            'network': 'base',
            'pool_address': pool_address,
            'timeframe': 'hour',
            'aggregate': '1',
            'limit': '1000'
        }
        
        if before_timestamp:
            params['before_timestamp'] = str(before_timestamp)
        
        response = await gt.get_pool_ohlcv(**params)
        candles = response['data']['attributes']['ohlcv_list']
        
        if not candles:
            break
        
        all_candles.extend(candles)
        
        # 检查是否已达到目标时间
        earliest_timestamp = candles[-1][0]  # 最后一条的时间戳
        if earliest_timestamp <= target_timestamp:
            break
        
        before_timestamp = earliest_timestamp
        await asyncio.sleep(0.5)  # 避免请求过快
    
    return all_candles
```

---

## ⚠️ 重要注意事项

### API 限制

1. **速率限制**：
   - 免费 API：30 次/分钟
   - 付费 API：500 次/分钟
   - 建议在请求之间添加延迟（0.5-1 秒）

2. **历史数据限制**：
   - 最多 6 个月的历史数据
   - 如需更长时间，需要定期增量下载

3. **数据缓存**：
   - API 数据缓存 1 分钟
   - 频繁请求相同数据不会获得实时更新

### 数据质量

1. **数据完整性**：
   - DEX 数据可能存在缺失或不连续
   - 建议验证时间戳的连续性

2. **价格准确性**：
   - DEX 价格可能与 CEX 存在偏差
   - 低流动性池的价格可能不准确

3. **交易量**：
   - 24小时交易量是滚动计算的
   - 不同时间查询可能得到不同的结果

---

## 🔗 相关文档

- [GeckoTerminal API 完整文档](./geckoterminal_api.md)
- [MongoDB 池子数据存储](./MONGODB_POOL_STORAGE.md)
- [数据存储策略](./DATA_STORAGE_STRATEGY.md)
- [Pool Screener 配置](../config/base_pools_production.yml)

---

## 📞 需要帮助？

如果在实现过程中遇到问题：

1. 检查 `geckoterminal_py` 库是否支持 OHLCV API
2. 如果不支持，可以使用 `httpx` 或 `aiohttp` 直接调用 HTTP API
3. 参考 `core/data_sources/clob.py` 中的 CLOB 数据下载实现

---

**最后更新：** 2025-10-05  
**维护者：** Alice


