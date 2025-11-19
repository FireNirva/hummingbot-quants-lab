# 🔍 Docker 日志记录与错误排查指南

## 📋 快速诊断

### 1. 检查容器状态

```bash
# 查看所有容器（包括已停止的）
docker ps -a

# 查看最近停止的容器
docker ps -a --filter "status=exited" --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}"

# 查看容器详细信息
docker inspect <container_id>
```

### 2. 查看容器日志

```bash
# 查看最近的日志（最后100行）
docker logs --tail 100 <container_id>

# 实时查看日志
docker logs -f <container_id>

# 查看带时间戳的日志
docker logs -t <container_id>

# 查看某个时间段的日志
docker logs --since "2024-11-18T14:00:00" <container_id>
```

### 3. 查看容器退出原因

```bash
# 查看容器退出代码
docker inspect <container_id> --format='{{.State.ExitCode}}'

# 查看容器状态详情
docker inspect <container_id> --format='{{json .State}}' | jq
```

**常见退出代码：**
- `0` - 正常退出
- `1` - 应用错误
- `137` - 被 SIGKILL 杀死（通常是内存不足）
- `139` - 段错误（Segmentation Fault）
- `143` - 被 SIGTERM 终止（手动停止）

---

## 🗂️ 日志持久化策略

### 问题：`--rm` 参数导致日志丢失

当前 `Makefile` 使用 `--rm` 参数，容器停止后会自动删除，**日志也会丢失**。

#### 解决方案 1: 移除 `--rm` 参数（不推荐）

**优点：** 可以查看历史日志
**缺点：** 容器会堆积，需要手动清理

#### 解决方案 2: 使用日志文件（推荐）

将容器日志重定向到文件：

```bash
# 运行时指定日志文件
docker run -d \
  --name quants-lab-orderbook \
  --log-driver json-file \
  --log-opt max-size=100m \
  --log-opt max-file=5 \
  ...其他参数... \
  hummingbot/quants-lab > /tmp/docker-run.log 2>&1
```

#### 解决方案 3: 应用层日志（最佳实践）

在应用内部记录日志到文件系统，通过 volume 挂载持久化。

---

## 📝 应用层日志配置

### 当前日志系统

QuantsLab 使用 Python 的 `logging` 模块：

```python
# core/tasks/runner.py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

**默认行为：**
- ✅ 日志输出到 stdout（Docker 可以捕获）
- ❌ 不写入日志文件
- ❌ 容器删除后日志丢失

### 改进方案：添加文件日志

**步骤 1: 创建日志配置文件**

创建 `config/logging_config.yml`：

```yaml
version: 1
disable_existing_loggers: False

formatters:
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    datefmt: '%Y-%m-%d %H:%M:%S'
  
  simple:
    format: '%(levelname)s - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple
    stream: ext://sys.stdout
  
  file:
    class: logging.handlers.RotatingFileHandler
    level: INFO
    formatter: detailed
    filename: /quants-lab/logs/quants-lab.log
    maxBytes: 104857600  # 100MB
    backupCount: 10
    encoding: utf8
  
  error_file:
    class: logging.handlers.RotatingFileHandler
    level: ERROR
    formatter: detailed
    filename: /quants-lab/logs/error.log
    maxBytes: 104857600  # 100MB
    backupCount: 5
    encoding: utf8

root:
  level: INFO
  handlers: [console, file, error_file]
```

**步骤 2: 修改 Makefile 挂载日志目录**

```makefile
run-tasks:
	docker run -d --rm \
		-v $(PWD)/logs:/quants-lab/logs \  # 新增：挂载日志目录
		-v $(PWD)/app/outputs:/quants-lab/app/outputs \
		...其他挂载...
		hummingbot/quants-lab
```

---

## 🔧 实用错误排查脚本

### 脚本 1: 容器健康检查

创建 `scripts/check_docker_health.sh`：

```bash
#!/bin/bash
# 检查 Docker 容器健康状态

CONTAINER_NAME="quants-lab-orderbook"
IMAGE_NAME="hummingbot/quants-lab"

echo "================================"
echo "🔍 Docker 容器健康检查"
echo "================================"
echo ""

# 查找运行中的容器
CONTAINER_ID=$(docker ps -q --filter ancestor=$IMAGE_NAME)

if [ -z "$CONTAINER_ID" ]; then
    echo "❌ 容器未运行"
    echo ""
    
    # 查找最近停止的容器
    LAST_CONTAINER=$(docker ps -aq --filter ancestor=$IMAGE_NAME --latest)
    
    if [ -n "$LAST_CONTAINER" ]; then
        echo "📋 最近停止的容器: $LAST_CONTAINER"
        echo ""
        
        # 查看退出代码
        EXIT_CODE=$(docker inspect $LAST_CONTAINER --format='{{.State.ExitCode}}')
        echo "退出代码: $EXIT_CODE"
        
        # 解释退出代码
        case $EXIT_CODE in
            0)
                echo "含义: 正常退出"
                ;;
            1)
                echo "含义: 应用错误"
                ;;
            137)
                echo "含义: 被 SIGKILL 杀死（可能是内存不足）"
                ;;
            139)
                echo "含义: 段错误"
                ;;
            143)
                echo "含义: 被 SIGTERM 终止（手动停止）"
                ;;
            *)
                echo "含义: 未知错误"
                ;;
        esac
        echo ""
        
        # 显示最后 50 行日志
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📜 最后 50 行日志:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        docker logs --tail 50 $LAST_CONTAINER
        echo ""
        
        # 检查是否有错误关键词
        ERROR_COUNT=$(docker logs $LAST_CONTAINER 2>&1 | grep -i "error\|exception\|failed" | wc -l)
        echo "⚠️  发现 $ERROR_COUNT 个错误/异常信息"
    else
        echo "❌ 未找到任何历史容器"
    fi
else
    echo "✅ 容器运行中: $CONTAINER_ID"
    echo ""
    
    # 显示容器信息
    docker ps --filter id=$CONTAINER_ID --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"
    echo ""
    
    # 检查资源使用
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 资源使用情况:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    docker stats $CONTAINER_ID --no-stream
    echo ""
    
    # 显示最近日志
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📜 最近 20 行日志:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    docker logs --tail 20 $CONTAINER_ID
fi

echo ""
echo "================================"
```

### 脚本 2: 自动重启监控

创建 `scripts/monitor_and_restart.sh`：

```bash
#!/bin/bash
# 监控容器状态，异常时自动重启

IMAGE_NAME="hummingbot/quants-lab"
CONFIG="config/orderbook_snapshot_gateio.yml"
CHECK_INTERVAL=60  # 检查间隔（秒）
MAX_RESTARTS=5     # 最大重启次数
RESTART_COUNT=0

echo "🔄 启动容器监控和自动重启服务"
echo "检查间隔: ${CHECK_INTERVAL}秒"
echo "最大重启次数: ${MAX_RESTARTS}"
echo ""

while true; do
    # 检查容器是否运行
    CONTAINER_ID=$(docker ps -q --filter ancestor=$IMAGE_NAME)
    
    if [ -z "$CONTAINER_ID" ]; then
        echo "⚠️  [$(date)] 容器未运行"
        
        # 检查最近停止的容器
        LAST_CONTAINER=$(docker ps -aq --filter ancestor=$IMAGE_NAME --latest)
        
        if [ -n "$LAST_CONTAINER" ]; then
            # 记录退出代码
            EXIT_CODE=$(docker inspect $LAST_CONTAINER --format='{{.State.ExitCode}}')
            echo "   退出代码: $EXIT_CODE"
            
            # 保存错误日志
            mkdir -p logs/crash_logs
            LOG_FILE="logs/crash_logs/crash_$(date +%Y%m%d_%H%M%S).log"
            docker logs $LAST_CONTAINER > "$LOG_FILE" 2>&1
            echo "   错误日志已保存: $LOG_FILE"
        fi
        
        # 检查重启次数
        if [ $RESTART_COUNT -ge $MAX_RESTARTS ]; then
            echo "❌ 已达到最大重启次数 ($MAX_RESTARTS)，停止监控"
            echo "   请手动检查问题！"
            exit 1
        fi
        
        # 重启容器
        RESTART_COUNT=$((RESTART_COUNT + 1))
        echo "🔄 尝试重启容器 (第 ${RESTART_COUNT}/${MAX_RESTARTS} 次)"
        
        make run-tasks config=$CONFIG
        
        # 等待容器启动
        sleep 10
        
        # 验证启动成功
        NEW_CONTAINER=$(docker ps -q --filter ancestor=$IMAGE_NAME)
        if [ -n "$NEW_CONTAINER" ]; then
            echo "✅ 容器重启成功: $NEW_CONTAINER"
            RESTART_COUNT=0  # 重置计数器
        else
            echo "❌ 容器重启失败"
        fi
    else
        # 容器正常运行，重置计数器
        if [ $RESTART_COUNT -gt 0 ]; then
            echo "✅ [$(date)] 容器恢复正常运行"
            RESTART_COUNT=0
        fi
    fi
    
    # 等待下次检查
    sleep $CHECK_INTERVAL
done
```

---

## 📊 完整错误排查流程

### 步骤 1: 确认问题

```bash
# 运行健康检查脚本
chmod +x scripts/check_docker_health.sh
./scripts/check_docker_health.sh
```

### 步骤 2: 查看详细日志

```bash
# 如果容器还在（未使用 --rm）
docker logs --tail 200 <container_id> | less

# 如果容器已删除，检查应用日志（需要配置文件日志）
tail -200 logs/quants-lab.log
tail -50 logs/error.log
```

### 步骤 3: 检查系统资源

```bash
# 查看 Docker 整体资源使用
docker stats --no-stream

# 查看主机内存
free -h

# 查看磁盘空间
df -h
```

### 步骤 4: 检查 MongoDB 连接

```bash
# 测试 MongoDB 连接
docker exec -it mongodb mongosh -u admin -p admin --eval "db.adminCommand('ping')"

# 或者使用 Python 测试
python -c "
from pymongo import MongoClient
client = MongoClient('mongodb://admin:admin@localhost:27017')
print('MongoDB 连接成功!' if client.admin.command('ping') else '连接失败')
"
```

### 步骤 5: 检查网络

```bash
# 测试 Gate.io API
curl -I https://api.gateio.ws/api/v4/spot/tickers

# 检查 DNS
nslookup api.gateio.ws
```

### 步骤 6: 手动复现

```bash
# 本地运行（更容易调试）
unset MONGO_URI
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml

# 观察输出
```

---

## 🎯 最佳实践建议

### 1. 启用文件日志

**修改 `core/tasks/runner.py` 添加文件日志：**

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 创建日志目录
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 配置文件日志
file_handler = RotatingFileHandler(
    log_dir / "quants-lab.log",
    maxBytes=100*1024*1024,  # 100MB
    backupCount=10
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

# 配置错误日志
error_handler = RotatingFileHandler(
    log_dir / "error.log",
    maxBytes=100*1024*1024,  # 100MB
    backupCount=5
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

# 应用配置
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # 控制台
        file_handler,             # 文件
        error_handler            # 错误文件
    ]
)
```

### 2. 使用 Docker Compose（推荐）

创建 `docker-compose-orderbook.yml`：

```yaml
version: '3.8'

services:
  orderbook-gateio:
    image: hummingbot/quants-lab
    container_name: quants-lab-orderbook-gateio
    command: conda run --no-capture-output -n quants-lab python3 cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
    volumes:
      - ./logs:/quants-lab/logs
      - ./app/data:/quants-lab/app/data
      - ./app/outputs:/quants-lab/app/outputs
      - ./config:/quants-lab/config
    env_file:
      - .env
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"
    depends_on:
      - mongodb
  
  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

volumes:
  mongodb_data:
```

**使用方式：**

```bash
# 启动
docker-compose -f docker-compose-orderbook.yml up -d

# 查看日志
docker-compose -f docker-compose-orderbook.yml logs -f orderbook-gateio

# 重启
docker-compose -f docker-compose-orderbook.yml restart orderbook-gateio

# 停止
docker-compose -f docker-compose-orderbook.yml down
```

**优势：**
- ✅ 自动重启（`restart: unless-stopped`）
- ✅ 日志持久化
- ✅ 依赖管理（MongoDB）
- ✅ 易于管理

### 3. 添加健康检查

在 Docker Compose 中添加：

```yaml
services:
  orderbook-gateio:
    # ...其他配置...
    healthcheck:
      test: ["CMD", "python", "-c", "import os; exit(0 if os.path.exists('app/data/raw/orderbook_snapshots') else 1)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

## 🚨 常见问题排查

### 问题 1: 容器启动后立即退出

**可能原因：**
- MongoDB 未启动
- 配置文件错误
- Python 依赖问题

**排查步骤：**

```bash
# 查看退出日志
docker logs $(docker ps -aq --latest)

# 手动运行容器（不使用 -d）
docker run --rm -it \
  -v $(PWD)/config:/quants-lab/config \
  --env-file .env \
  hummingbot/quants-lab \
  conda run -n quants-lab python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
```

### 问题 2: 容器运行一段时间后停止

**可能原因：**
- 内存不足（退出代码 137）
- API 限流导致异常
- 未捕获的异常

**排查步骤：**

```bash
# 查看退出代码
docker inspect <container_id> --format='{{.State.ExitCode}}'

# 查看内存使用
docker stats --no-stream

# 查看最后的错误
docker logs --tail 100 <container_id> | grep -i "error\|exception\|traceback"
```

### 问题 3: 数据停止更新但容器仍在运行

**可能原因：**
- API 限流
- 网络问题
- 任务被阻塞

**排查步骤：**

```bash
# 进入容器检查
docker exec -it <container_id> /bin/bash

# 查看进程
ps aux | grep python

# 检查网络
curl https://api.gateio.ws/api/v4/spot/tickers
```

---

## 📚 相关文档

- [订单簿数据采集指南](./ORDERBOOK_COLLECTION_GUIDE.md)
- [无 MongoDB 模式运行](./NO_MONGODB_MODE.md)
- [AWS Lightsail 部署指南](./AWS_LIGHTSAIL_DEPLOYMENT_GUIDE.md)

---

**最后更新**: 2024-11-18

