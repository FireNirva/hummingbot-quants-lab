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

## 📚 相关文档

- [Base 套利完整指南](docs/BASE_ARBITRAGE_GUIDE.md)
- [数据收集指南](docs/DATA_COLLECTION_GUIDE.md)
- [快速上手](docs/QUICK_START_DATA_COLLECTION.md)
- [数据存储策略](docs/DATA_STORAGE_STRATEGY.md)

---

**快速访问**: 复制粘贴命令即可使用！⚡

