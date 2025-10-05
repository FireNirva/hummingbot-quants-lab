# GeckoTerminal API 完整参考文档

> **官方文档：** https://www.geckoterminal.com/dex-api  
> **Base URL：** `https://api.geckoterminal.com/api/v2`  
> **版本：** v2 (Beta)

---

## 📋 目录

1. [快速开始](#快速开始)
2. [认证和限制](#认证和限制)
3. [API 概览](#api-概览)
4. [Simple - 代币价格](#1-simple---代币价格)
5. [Networks - 网络列表](#2-networks---网络列表)
6. [DEXes - 交易所列表](#3-dexes---交易所列表)
7. [Pools - 流动性池](#4-pools---流动性池)
8. [Tokens - 代币信息](#5-tokens---代币信息)
9. [OHLCV - K线数据](#6-ohlcv---k线数据)
10. [Trades - 交易记录](#7-trades---交易记录)

---

## 快速开始

### 基本信息

- **Base URL**: `https://api.geckoterminal.com/api/v2`
- **数据更新**: 2-3 秒（链上确认后）
- **数据缓存**: 1 分钟
- **免费限制**: 30 次/分钟
- **付费限制**: 500 次/分钟

### 版本控制

推荐在请求头中设置 API 版本：

```http
Accept: application/json;version=20230302
```

### 快速示例

```bash
# 获取以太坊网络上的支持的 DEX 列表
curl "https://api.geckoterminal.com/api/v2/networks/eth/dexes"

# 获取 Base 链的热门池子
curl "https://api.geckoterminal.com/api/v2/networks/base/trending_pools"

# 获取特定代币价格
curl "https://api.geckoterminal.com/api/v2/simple/networks/eth/token_price/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
```

---

## 认证和限制

### 速率限制

| 类型 | 限制 | 说明 |
|-----|------|------|
| 免费 API | 30 次/分钟 | 无需注册 |
| 付费 API | 500 次/分钟 | 订阅 CoinGecko 付费计划 |

### 错误代码

| 状态码 | 说明 |
|-------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 422 | 无法处理的请求（如不支持的池类型）|
| 429 | 超过速率限制 |

---

## API 概览

### 按功能分类

| 类别 | 用途 | 主要 Endpoints |
|-----|------|---------------|
| **Simple** | 快速获取代币价格 | `/simple/networks/{network}/token_price/{addresses}` |
| **Networks** | 获取支持的区块链网络 | `/networks` |
| **DEXes** | 获取支持的 DEX 列表 | `/networks/{network}/dexes` |
| **Pools** | 池子信息和搜索 | `/networks/{network}/pools` |
| **Tokens** | 代币详细信息 | `/networks/{network}/tokens/{address}` |
| **OHLCV** | 历史 K线数据 | `/networks/{network}/pools/{address}/ohlcv/{timeframe}` |
| **Trades** | 最近交易记录 | `/networks/{network}/pools/{address}/trades` |

---

## 1. Simple - 代币价格

### 1.1 获取多个代币的价格

快速获取一个或多个代币的 USD 价格。

**Endpoint:**
```
GET /simple/networks/{network}/token_price/{addresses}
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `network` | string | ✅ | 网络 ID（如 `eth`, `base`, `solana`）|
| `addresses` | string | ✅ | 逗号分隔的代币地址列表（最多 30 个）|
| `include_market_cap` | boolean | ❌ | 包含市值（默认：false）|
| `include_24hr_vol` | boolean | ❌ | 包含 24h 交易量（默认：false）|
| `include_24hr_price_change` | boolean | ❌ | 包含 24h 价格变化（默认：false）|
| `include_total_reserve_in_usd` | boolean | ❌ | 包含总流动性（默认：false）|

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/simple/networks/eth/token_price/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48?include_24hr_vol=true"
```

**响应示例:**

```json
{
  "data": [
    {
      "id": "eth",
      "type": "simple_token_price",
      "attributes": {
        "token_prices": {
          "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "0.996586",
          "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "1822.49"
        }
      }
    }
  ]
}
```

**Python 示例:**

```python
import httpx

async def get_token_prices(network: str, addresses: list[str]):
    base_url = "https://api.geckoterminal.com/api/v2"
    addresses_str = ",".join(addresses)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/simple/networks/{network}/token_price/{addresses_str}",
            params={"include_24hr_vol": "true"}
        )
        return response.json()

# 使用示例
prices = await get_token_prices("eth", [
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # WETH
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"   # USDC
])
```

---

## 2. Networks - 网络列表

### 2.1 获取支持的网络

获取 GeckoTerminal 支持的所有区块链网络。

**Endpoint:**
```
GET /networks
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `page` | integer | ❌ | 页码（默认：1）|

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks?page=1"
```

**响应示例:**

```json
{
  "data": [
    {
      "id": "eth",
      "type": "network",
      "attributes": {
        "name": "Ethereum"
      }
    },
    {
      "id": "base",
      "type": "network",
      "attributes": {
        "name": "Base"
      }
    },
    {
      "id": "solana",
      "type": "network",
      "attributes": {
        "name": "Solana"
      }
    }
  ]
}
```

**常用网络 ID:**

| Network ID | 名称 | 说明 |
|-----------|------|------|
| `eth` | Ethereum | 以太坊主网 |
| `base` | Base | Coinbase L2 |
| `solana` | Solana | Solana 主网 |
| `bsc` | BSC | 币安智能链 |
| `polygon` | Polygon | Polygon PoS |
| `arbitrum` | Arbitrum | Arbitrum One |
| `optimism` | Optimism | Optimism 主网 |
| `avalanche` | Avalanche | Avalanche C-Chain |

---

## 3. DEXes - 交易所列表

### 3.1 获取网络上的 DEX 列表

获取指定网络支持的所有 DEX。

**Endpoint:**
```
GET /networks/{network}/dexes
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `network` | string | ✅ | 网络 ID |
| `page` | integer | ❌ | 页码（默认：1）|

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/base/dexes"
```

**响应示例:**

```json
{
  "data": [
    {
      "id": "uniswap-v3-base",
      "type": "dex",
      "attributes": {
        "name": "Uniswap V3"
      }
    },
    {
      "id": "aerodrome-base",
      "type": "dex",
      "attributes": {
        "name": "Aerodrome"
      }
    }
  ]
}
```

**常用 DEX（Base 链）:**

| DEX ID | 名称 |
|--------|------|
| `uniswap-v3-base` | Uniswap V3 |
| `aerodrome-base` | Aerodrome |
| `baseswap` | BaseSwap |
| `alienbase` | AlienBase |
| `sushiswap-base` | SushiSwap |
| `pancakeswap-v3-base` | PancakeSwap V3 |

---

## 4. Pools - 流动性池

### 4.1 获取热门池子（全网络）

获取所有网络中最热门的池子。

**Endpoint:**
```
GET /networks/trending_pools
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `include` | string | ❌ | 包含相关资源：`base_token`, `quote_token`, `dex`, `network` |
| `page` | integer | ❌ | 页码（1-10）|
| `duration` | string | ❌ | 时间范围：`5m`, `1h`, `6h`, `24h` |

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/trending_pools?duration=1h&page=1"
```

### 4.2 获取特定网络的热门池子

**Endpoint:**
```
GET /networks/{network}/trending_pools
```

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/base/trending_pools?include=base_token,quote_token"
```

### 4.3 获取网络的 Top 池子

按交易笔数或交易量获取顶级池子。

**Endpoint:**
```
GET /networks/{network}/pools
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `network` | string | ✅ | 网络 ID |
| `include` | string | ❌ | 包含：`base_token`, `quote_token`, `dex` |
| `page` | integer | ❌ | 页码（1-10）|
| `sort` | string | ❌ | 排序：`h24_tx_count_desc`, `h24_volume_usd_desc` |

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/base/pools?sort=h24_volume_usd_desc"
```

### 4.4 获取特定 DEX 的池子

**Endpoint:**
```
GET /networks/{network}/dexes/{dex}/pools
```

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/base/dexes/uniswap-v3-base/pools"
```

### 4.5 获取新创建的池子

**Endpoint:**
```
GET /networks/{network}/new_pools
```

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/base/new_pools"
```

### 4.6 获取特定池子信息

**Endpoint:**
```
GET /networks/{network}/pools/{address}
```

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/eth/pools/0x60594a405d53811d3bc4766596efd80fd545a270"
```

### 4.7 获取多个池子信息

**Endpoint:**
```
GET /networks/{network}/pools/multi/{addresses}
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `addresses` | string | ✅ | 逗号分隔的池子地址（最多 30 个）|

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/eth/pools/multi/0x60594a405d53811d3bc4766596efd80fd545a270,0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
```

### 4.8 搜索池子

**Endpoint:**
```
GET /search/pools
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `query` | string | ✅ | 搜索关键词（池子地址、代币地址或符号）|
| `network` | string | ❌ | 限制搜索的网络 |
| `page` | integer | ❌ | 页码（1-10）|

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/search/pools?query=ETH&network=base"
```

### 池子数据结构

```json
{
  "id": "base_uniswap-v3_0x4c36388be6f416a29c8d8eee81c771ce6be14b18",
  "type": "pool",
  "attributes": {
    "name": "WETH / USDC 0.01%",
    "address": "0x4c36388be6f416a29c8d8eee81c771ce6be14b18",
    "base_token_price_usd": "3260.45",
    "quote_token_price_usd": "1.0",
    "base_token_price_native_currency": "1.0",
    "quote_token_price_native_currency": "0.000306748",
    "pool_created_at": "2023-08-15T10:30:00Z",
    "reserve_in_usd": "8326274.12",
    "fdv_usd": "784144285.46",
    "market_cap_usd": "784144285.46",
    "price_change_percentage": {
      "h1": "0.52",
      "h24": "2.34"
    },
    "transactions": {
      "h1": {
        "buys": 523,
        "sells": 498
      },
      "h24": {
        "buys": 12345,
        "sells": 11234
      }
    },
    "volume_usd": {
      "h1": "6621823.45",
      "h24": "158589434.23"
    }
  }
}
```

---

## 5. Tokens - 代币信息

### 5.1 获取代币信息

**Endpoint:**
```
GET /networks/{network}/tokens/{address}
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `network` | string | ✅ | 网络 ID |
| `address` | string | ✅ | 代币地址 |
| `include` | string | ❌ | 包含：`top_pools` |

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/eth/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2?include=top_pools"
```

**响应示例:**

```json
{
  "data": {
    "id": "eth_0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "type": "token",
    "attributes": {
      "name": "Wrapped Ether",
      "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
      "symbol": "WETH",
      "decimals": 18,
      "total_supply": "3251438.482",
      "coingecko_coin_id": "weth",
      "price_usd": "3260.45",
      "fdv_usd": "10605000000",
      "total_reserve_in_usd": "8500000000",
      "volume_usd": {
        "h24": "2400000000"
      },
      "market_cap_usd": "10605000000"
    }
  }
}
```

### 5.2 获取多个代币信息

**Endpoint:**
```
GET /networks/{network}/tokens/multi/{addresses}
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `addresses` | string | ✅ | 逗号分隔的代币地址（最多 30 个）|

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/eth/tokens/multi/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
```

### 5.3 获取代币的池子列表

**Endpoint:**
```
GET /networks/{network}/tokens/{token_address}/pools
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `page` | integer | ❌ | 页码（1-10）|
| `sort` | string | ❌ | 排序：`h24_volume_usd_liquidity_desc`, `h24_tx_count_desc`, `h24_volume_usd_desc` |

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/eth/tokens/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48/pools?sort=h24_volume_usd_desc"
```

### 5.4 获取代币详细信息

包含社交媒体、网站等信息。

**Endpoint:**
```
GET /networks/{network}/tokens/{address}/info
```

**示例请求:**

```bash
curl "https://api.geckoterminal.com/api/v2/networks/eth/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2/info"
```

**响应示例:**

```json
{
  "data": {
    "id": "eth_0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "type": "token_info",
    "attributes": {
      "name": "Wrapped Ether",
      "symbol": "WETH",
      "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
      "image_url": "https://...",
      "websites": ["https://weth.io"],
      "description": "WETH is wrapped ETH",
      "discord_url": null,
      "telegram_handle": null,
      "twitter_handle": "weth",
      "coingecko_coin_id": "weth",
      "gt_score": 95
    }
  }
}
```

### 5.5 获取池子的代币信息

**Endpoint:**
```
GET /networks/{network}/pools/{pool_address}/info
```

返回池子中两个代币的详细信息。

---

## 6. OHLCV - K线数据

### 6.1 获取池子的 OHLCV 数据

获取池子的历史 K线数据（最多 6 个月）。

**Endpoint:**
```
GET /networks/{network}/pools/{pool_address}/ohlcv/{timeframe}
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `network` | string | ✅ | 网络 ID |
| `pool_address` | string | ✅ | 池子地址 |
| `timeframe` | string | ✅ | 时间框架：`day`, `hour`, `minute` |
| `aggregate` | string | ❌ | 聚合周期（见下表）|
| `before_timestamp` | string | ❌ | 获取此时间戳之前的数据 |
| `limit` | string | ❌ | 返回数量（默认 100，最大 1000）|
| `currency` | string | ❌ | 货币单位：`usd`, `token`（默认 usd）|
| `token` | string | ❌ | 基准代币：`base`, `quote`（默认 base）|

**聚合周期选项:**

| Timeframe | 可用的 aggregate 值 |
|-----------|-------------------|
| `day` | `1` |
| `hour` | `1`, `4`, `12` |
| `minute` | `1`, `5`, `15` |

**示例请求:**

```bash
# 获取 1 小时 K线
curl "https://api.geckoterminal.com/api/v2/networks/eth/pools/0x60594a405d53811d3bc4766596efd80fd545a270/ohlcv/hour?aggregate=1&limit=100"

# 获取 15 分钟 K线
curl "https://api.geckoterminal.com/api/v2/networks/base/pools/0x4c36388be6f416a29c8d8eee81c771ce6be14b18/ohlcv/minute?aggregate=15&limit=500"

# 获取 4 小时 K线
curl "https://api.geckoterminal.com/api/v2/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/ohlcv/hour?aggregate=4"
```

**响应示例:**

```json
{
  "data": {
    "id": "eth_0x60594a405d53811d3bc4766596efd80fd545a270",
    "type": "pool_ohlcv",
    "attributes": {
      "ohlcv_list": [
        [1708498800, 2955.65, 2955.65, 2933.98, 2934.24, 131664.76],
        [1708495200, 2934.24, 2955.65, 2930.12, 2940.56, 145823.45],
        [1708491600, 2940.56, 2945.78, 2925.34, 2934.24, 152341.23]
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
      "address": "0x6b175474e89094c44da98b954eedeac495271d0f",
      "name": "Dai Stablecoin",
      "symbol": "DAI"
    }
  }
}
```

**OHLCV 数组格式:**

```
[timestamp, open, high, low, close, volume]
```

| 索引 | 字段 | 说明 |
|-----|------|------|
| 0 | timestamp | Unix 时间戳（秒）|
| 1 | open | 开盘价 |
| 2 | high | 最高价 |
| 3 | low | 最低价 |
| 4 | close | 收盘价 |
| 5 | volume | 交易量 |

**Python 示例:**

```python
import httpx
import pandas as pd
from datetime import datetime

async def get_ohlcv(
    network: str,
    pool_address: str,
    timeframe: str = "hour",
    aggregate: str = "1",
    limit: int = 100
):
    base_url = "https://api.geckoterminal.com/api/v2"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/networks/{network}/pools/{pool_address}/ohlcv/{timeframe}",
            params={
                "aggregate": aggregate,
                "limit": str(limit),
                "currency": "usd"
            }
        )
        data = response.json()
        
        # 转换为 DataFrame
        ohlcv_list = data['data']['attributes']['ohlcv_list']
        df = pd.DataFrame(
            ohlcv_list,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        return df

# 使用示例
df = await get_ohlcv(
    network="base",
    pool_address="0x4c36388be6f416a29c8d8eee81c771ce6be14b18",
    timeframe="hour",
    aggregate="1",
    limit=100
)

print(df.head())
```

**限制和注意事项:**

- ⏰ 历史数据最多 6 个月
- 📊 单次请求最多 1000 条
- 🔄 数据缓存 1 分钟
- 🚫 不支持超过 2 个代币的池子

---

## 7. Trades - 交易记录

### 7.1 获取池子的最近交易

获取过去 24 小时内的最近 300 笔交易。

**Endpoint:**
```
GET /networks/{network}/pools/{pool_address}/trades
```

**参数:**

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `network` | string | ✅ | 网络 ID |
| `pool_address` | string | ✅ | 池子地址 |
| `trade_volume_in_usd_greater_than` | number | ❌ | 筛选交易量（USD）|
| `token` | string | ❌ | 基准代币：`base`, `quote` 或代币地址 |

**示例请求:**

```bash
# 获取所有交易
curl "https://api.geckoterminal.com/api/v2/networks/eth/pools/0x60594a405d53811d3bc4766596efd80fd545a270/trades"

# 只获取大于 10万 USD 的交易
curl "https://api.geckoterminal.com/api/v2/networks/eth/pools/0x60594a405d53811d3bc4766596efd80fd545a270/trades?trade_volume_in_usd_greater_than=100000"
```

**响应示例:**

```json
{
  "data": [
    {
      "id": "...",
      "type": "trade",
      "attributes": {
        "block_number": 18934567,
        "block_timestamp": "2024-01-15T10:30:45Z",
        "tx_hash": "0x1234...",
        "tx_from_address": "0xabcd...",
        "from_token_amount": "1.5",
        "to_token_amount": "4891.234",
        "price_from_in_currency_token": "3260.82",
        "price_to_in_currency_token": "1.0",
        "price_from_in_usd": "3260.82",
        "price_to_in_usd": "1.0",
        "kind": "buy",
        "volume_in_usd": "4891.234",
        "from_token_address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        "to_token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
      }
    }
  ]
}
```

**交易字段说明:**

| 字段 | 说明 |
|-----|------|
| `block_number` | 区块高度 |
| `block_timestamp` | 交易时间 |
| `tx_hash` | 交易哈希 |
| `tx_from_address` | 交易发起地址 |
| `from_token_amount` | 卖出数量 |
| `to_token_amount` | 买入数量 |
| `price_from_in_usd` | 卖出代币价格（USD）|
| `price_to_in_usd` | 买入代币价格（USD）|
| `kind` | 交易类型：`buy` 或 `sell` |
| `volume_in_usd` | 交易量（USD）|

**Python 示例:**

```python
async def get_recent_trades(
    network: str,
    pool_address: str,
    min_volume_usd: float = 0
):
    base_url = "https://api.geckoterminal.com/api/v2"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/networks/{network}/pools/{pool_address}/trades",
            params={
                "trade_volume_in_usd_greater_than": str(min_volume_usd)
            }
        )
        return response.json()

# 使用示例：获取大于 1万 USD 的交易
trades = await get_recent_trades(
    network="base",
    pool_address="0x4c36388be6f416a29c8d8eee81c771ce6be14b18",
    min_volume_usd=10000
)

for trade in trades['data']:
    attrs = trade['attributes']
    print(f"{attrs['kind'].upper()}: ${attrs['volume_in_usd']} at {attrs['block_timestamp']}")
```

---

## 📚 完整使用示例

### Python 异步客户端封装

```python
import httpx
import asyncio
from typing import Optional, Dict, Any, List

class GeckoTerminalClient:
    """GeckoTerminal API 异步客户端"""
    
    def __init__(self):
        self.base_url = "https://api.geckoterminal.com/api/v2"
        self.headers = {
            "Accept": "application/json;version=20230302"
        }
    
    async def _request(self, endpoint: str, params: Optional[Dict] = None):
        """发送 HTTP 请求"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=params or {}
            )
            response.raise_for_status()
            return response.json()
    
    # Networks
    async def get_networks(self, page: int = 1):
        """获取支持的网络列表"""
        return await self._request("/networks", {"page": page})
    
    async def get_dexes(self, network: str, page: int = 1):
        """获取网络上的 DEX 列表"""
        return await self._request(f"/networks/{network}/dexes", {"page": page})
    
    # Pools
    async def get_trending_pools(
        self,
        network: str,
        duration: str = "1h",
        page: int = 1,
        include: Optional[str] = None
    ):
        """获取热门池子"""
        params = {"duration": duration, "page": page}
        if include:
            params["include"] = include
        return await self._request(f"/networks/{network}/trending_pools", params)
    
    async def get_top_pools(
        self,
        network: str,
        page: int = 1,
        sort: str = "h24_tx_count_desc"
    ):
        """获取 Top 池子"""
        return await self._request(
            f"/networks/{network}/pools",
            {"page": page, "sort": sort}
        )
    
    async def get_new_pools(self, network: str, page: int = 1):
        """获取新池子"""
        return await self._request(f"/networks/{network}/new_pools", {"page": page})
    
    async def get_pool(
        self,
        network: str,
        pool_address: str,
        include: Optional[str] = None
    ):
        """获取特定池子信息"""
        params = {}
        if include:
            params["include"] = include
        return await self._request(f"/networks/{network}/pools/{pool_address}", params)
    
    async def search_pools(
        self,
        query: str,
        network: Optional[str] = None,
        page: int = 1
    ):
        """搜索池子"""
        params = {"query": query, "page": page}
        if network:
            params["network"] = network
        return await self._request("/search/pools", params)
    
    # Tokens
    async def get_token(
        self,
        network: str,
        token_address: str,
        include: Optional[str] = None
    ):
        """获取代币信息"""
        params = {}
        if include:
            params["include"] = include
        return await self._request(f"/networks/{network}/tokens/{token_address}", params)
    
    async def get_token_pools(
        self,
        network: str,
        token_address: str,
        page: int = 1,
        sort: str = "h24_volume_usd_liquidity_desc"
    ):
        """获取代币的池子列表"""
        return await self._request(
            f"/networks/{network}/tokens/{token_address}/pools",
            {"page": page, "sort": sort}
        )
    
    async def get_token_price(
        self,
        network: str,
        addresses: List[str],
        include_24hr_vol: bool = False,
        include_market_cap: bool = False
    ):
        """获取代币价格"""
        addresses_str = ",".join(addresses)
        params = {}
        if include_24hr_vol:
            params["include_24hr_vol"] = "true"
        if include_market_cap:
            params["include_market_cap"] = "true"
        return await self._request(
            f"/simple/networks/{network}/token_price/{addresses_str}",
            params
        )
    
    # OHLCV
    async def get_ohlcv(
        self,
        network: str,
        pool_address: str,
        timeframe: str = "hour",
        aggregate: str = "1",
        limit: int = 100,
        before_timestamp: Optional[int] = None,
        currency: str = "usd"
    ):
        """获取 OHLCV K线数据"""
        params = {
            "aggregate": aggregate,
            "limit": str(limit),
            "currency": currency
        }
        if before_timestamp:
            params["before_timestamp"] = str(before_timestamp)
        return await self._request(
            f"/networks/{network}/pools/{pool_address}/ohlcv/{timeframe}",
            params
        )
    
    # Trades
    async def get_trades(
        self,
        network: str,
        pool_address: str,
        min_volume_usd: float = 0
    ):
        """获取最近交易"""
        params = {}
        if min_volume_usd > 0:
            params["trade_volume_in_usd_greater_than"] = str(min_volume_usd)
        return await self._request(
            f"/networks/{network}/pools/{pool_address}/trades",
            params
        )


# 使用示例
async def main():
    client = GeckoTerminalClient()
    
    # 获取 Base 链的热门池子
    trending = await client.get_trending_pools("base", duration="1h")
    print(f"热门池子数量: {len(trending['data'])}")
    
    # 获取特定代币价格
    prices = await client.get_token_price(
        "eth",
        [
            "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # WETH
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"   # USDC
        ],
        include_24hr_vol=True
    )
    print(f"代币价格: {prices}")
    
    # 获取 K线数据
    ohlcv = await client.get_ohlcv(
        "base",
        "0x4c36388be6f416a29c8d8eee81c771ce6be14b18",
        timeframe="hour",
        aggregate="1",
        limit=100
    )
    print(f"K线数据条数: {len(ohlcv['data']['attributes']['ohlcv_list'])}")
    
    # 搜索池子
    search_results = await client.search_pools("WETH", network="base")
    print(f"搜索结果: {len(search_results['data'])} 个池子")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🔧 最佳实践

### 1. 速率限制处理

```python
import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    """速率限制器"""
    
    def __init__(self, calls_per_minute: int = 30):
        self.calls_per_minute = calls_per_minute
        self.call_times = []
    
    async def wait_if_needed(self):
        """等待直到可以发送请求"""
        now = datetime.now()
        
        # 清理 1 分钟前的记录
        self.call_times = [
            t for t in self.call_times
            if now - t < timedelta(minutes=1)
        ]
        
        # 如果超过限制，等待
        if len(self.call_times) >= self.calls_per_minute:
            oldest = min(self.call_times)
            wait_time = 60 - (now - oldest).total_seconds()
            if wait_time > 0:
                print(f"⏳ 速率限制：等待 {wait_time:.1f} 秒")
                await asyncio.sleep(wait_time)
        
        self.call_times.append(now)

# 使用示例
limiter = RateLimiter(calls_per_minute=25)  # 留点余地

async def fetch_with_limit(client, *args, **kwargs):
    await limiter.wait_if_needed()
    return await client.get_trending_pools(*args, **kwargs)
```

### 2. 错误处理和重试

```python
import asyncio
from typing import Optional

async def fetch_with_retry(
    func,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    backoff_factor: float = 2.0
):
    """带重试的请求"""
    for attempt in range(max_retries):
        try:
            return await func()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:  # 速率限制
                wait_time = retry_delay * (backoff_factor ** attempt)
                print(f"⚠️  速率限制，等待 {wait_time}秒 (尝试 {attempt + 1}/{max_retries})")
                await asyncio.sleep(wait_time)
            elif e.response.status_code >= 500:  # 服务器错误
                wait_time = retry_delay * (backoff_factor ** attempt)
                print(f"⚠️  服务器错误，等待 {wait_time}秒 (尝试 {attempt + 1}/{max_retries})")
                await asyncio.sleep(wait_time)
            else:
                raise
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = retry_delay * (backoff_factor ** attempt)
            print(f"⚠️  请求失败: {e}，等待 {wait_time}秒 (尝试 {attempt + 1}/{max_retries})")
            await asyncio.sleep(wait_time)
    
    raise Exception(f"请求失败，已重试 {max_retries} 次")
```

### 3. 数据缓存

```python
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class SimpleCache:
    """简单的内存缓存"""
    
    def __init__(self, ttl_seconds: int = 60):
        self.cache: Dict[str, tuple[Any, datetime]] = {}
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存"""
        self.cache[key] = (value, datetime.now())
    
    def clear(self):
        """清除所有缓存"""
        self.cache.clear()

# 使用示例
cache = SimpleCache(ttl_seconds=60)

async def get_pools_with_cache(client, network: str):
    cache_key = f"pools_{network}"
    
    # 尝试从缓存获取
    cached = cache.get(cache_key)
    if cached:
        print("✅ 使用缓存数据")
        return cached
    
    # 从 API 获取
    print("🌐 从 API 获取数据")
    data = await client.get_top_pools(network)
    cache.set(cache_key, data)
    return data
```

### 4. 批量请求

```python
async def fetch_multiple_pools(
    client: GeckoTerminalClient,
    network: str,
    pool_addresses: List[str],
    batch_size: int = 30  # API 限制最多 30 个
):
    """批量获取池子信息"""
    results = []
    
    for i in range(0, len(pool_addresses), batch_size):
        batch = pool_addresses[i:i + batch_size]
        addresses_str = ",".join(batch)
        
        data = await client._request(
            f"/networks/{network}/pools/multi/{addresses_str}"
        )
        results.extend(data['data'])
        
        # 避免速率限制
        if i + batch_size < len(pool_addresses):
            await asyncio.sleep(0.5)
    
    return results
```

---

## 📖 相关资源

- **官方文档**: https://www.geckoterminal.com/dex-api
- **项目使用文档**: [GECKOTERMINAL_API_USAGE.md](./GECKOTERMINAL_API_USAGE.md)
- **Pool Screener 实现**: `app/tasks/data_collection/pools_screener.py`
- **MongoDB 数据存储**: [MONGODB_POOL_STORAGE.md](./MONGODB_POOL_STORAGE.md)

---

## ⚠️ 重要提示

1. **API 状态**: Beta 版本，可能随时变更
2. **速率限制**: 免费 30 次/分钟，付费 500 次/分钟
3. **数据缓存**: 所有数据缓存 1 分钟
4. **历史数据**: OHLCV 最多 6 个月
5. **池子限制**: OHLCV 不支持超过 2 个代币的池子

---

**最后更新**: 2025-10-05  
**维护者**: Alice  
**版本**: 1.0


