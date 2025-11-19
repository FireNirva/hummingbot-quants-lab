# 🐳 Docker 常用命令速查表

## 📋 容器管理

### 启动和停止

```bash
# 使用 Makefile (单个容器)
make run-tasks config=orderbook_snapshot_gateio.yml

# 使用 Docker Compose (推荐)
docker-compose -f docker-compose-orderbook.yml up -d

# 启动并包含 MEXC 采集
docker-compose -f docker-compose-orderbook.yml --profile mexc up -d

# 停止所有服务
docker-compose -f docker-compose-orderbook.yml down

# 停止但保留数据
docker-compose -f docker-compose-orderbook.yml stop

# 重启服务
docker-compose -f docker-compose-orderbook.yml restart orderbook-gateio
```

### 查看状态

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括停止的）
docker ps -a

# 查看容器详细信息
docker inspect <container_id>

# 查看资源使用
docker stats

# 查看特定容器资源
docker stats <container_id> --no-stream
```

---

## 📜 日志管理

### 查看日志

```bash
# 查看实时日志
docker logs -f <container_id>

# 查看最近 100 行
docker logs --tail 100 <container_id>

# 查看带时间戳的日志
docker logs -t <container_id>

# 查看某个时间段的日志
docker logs --since "2024-11-18T14:00:00" <container_id>
docker logs --since 30m <container_id>

# 查看 Docker Compose 服务日志
docker-compose -f docker-compose-orderbook.yml logs -f orderbook-gateio

# 查看所有服务日志
docker-compose -f docker-compose-orderbook.yml logs -f
```

### 保存日志

```bash
# 导出日志到文件
docker logs <container_id> > container.log 2>&1

# 导出最近的错误
docker logs <container_id> 2>&1 | grep -i "error" > errors.log

# 使用 Docker Compose 导出
docker-compose -f docker-compose-orderbook.yml logs orderbook-gateio > gateio.log
```

---

## 🔍 故障排查

### 快速诊断

```bash
# 运行健康检查脚本
./scripts/check_docker_health.sh

# 查看退出代码
docker inspect <container_id> --format='{{.State.ExitCode}}'

# 查看容器状态
docker inspect <container_id> --format='{{json .State}}' | jq

# 查看最近失败的容器
docker ps -a --filter "status=exited" --filter "exited=1" --latest
```

### 进入容器调试

```bash
# 进入运行中的容器
docker exec -it <container_id> /bin/bash

# 执行单个命令
docker exec <container_id> ls -la /quants-lab/logs

# 查看容器内进程
docker exec <container_id> ps aux

# 测试网络连接
docker exec <container_id> curl -I https://api.gateio.ws
```

### 查看错误

```bash
# 查找错误信息
docker logs <container_id> 2>&1 | grep -i "error\|exception\|failed"

# 查找最近 5 分钟的错误
docker logs --since 5m <container_id> 2>&1 | grep -i "error"

# 统计错误数量
docker logs <container_id> 2>&1 | grep -i "error" | wc -l
```

---

## 🗄️ 数据和卷管理

### 查看卷

```bash
# 列出所有卷
docker volume ls

# 查看卷详情
docker volume inspect quants-lab-mongodb-data

# 清理未使用的卷
docker volume prune
```

### 备份和恢复

```bash
# 备份 MongoDB 数据
docker exec mongodb mongodump --out /tmp/backup
docker cp mongodb:/tmp/backup ./mongodb-backup

# 恢复 MongoDB 数据
docker cp ./mongodb-backup mongodb:/tmp/
docker exec mongodb mongorestore /tmp/mongodb-backup
```

---

## 🔄 重启策略

### 修改重启策略

```bash
# 修改为自动重启
docker update --restart=unless-stopped <container_id>

# 修改为总是重启
docker update --restart=always <container_id>

# 禁用自动重启
docker update --restart=no <container_id>
```

### Docker Compose 重启策略

在 `docker-compose-orderbook.yml` 中：

```yaml
services:
  orderbook-gateio:
    restart: unless-stopped  # 推荐：除非手动停止，否则总是重启
    # restart: always         # 总是重启（包括手动停止后）
    # restart: on-failure     # 仅在失败时重启
    # restart: no             # 永不重启
```

---

## 🧹 清理和维护

### 清理容器

```bash
# 删除停止的容器
docker container prune

# 删除特定容器
docker rm <container_id>

# 强制删除运行中的容器
docker rm -f <container_id>
```

### 清理镜像

```bash
# 删除未使用的镜像
docker image prune

# 删除所有未使用的镜像
docker image prune -a

# 删除特定镜像
docker rmi hummingbot/quants-lab
```

### 完全清理

```bash
# 清理所有未使用的资源
docker system prune

# 清理所有资源（包括卷）
docker system prune -a --volumes

# 查看磁盘使用
docker system df
```

---

## 📊 监控和性能

### 资源监控

```bash
# 实时查看所有容器资源
docker stats

# 查看特定容器资源
docker stats <container_id>

# 查看容器事件
docker events

# 查看 Docker Compose 服务状态
docker-compose -f docker-compose-orderbook.yml ps

# 查看服务健康状态
docker-compose -f docker-compose-orderbook.yml ps --format json | jq
```

### 性能分析

```bash
# 查看容器进程
docker top <container_id>

# 查看容器文件系统变化
docker diff <container_id>

# 查看端口映射
docker port <container_id>
```

---

## 🚀 快速操作命令

### 一键脚本

```bash
# 健康检查
./scripts/check_docker_health.sh

# 启动监控和自动重启
./scripts/monitor_and_restart.sh

# 监控数据更新
./scripts/watch_orderbook_live.sh 5
```

### Docker Compose 快速命令

```bash
# 启动所有服务
docker-compose -f docker-compose-orderbook.yml up -d

# 查看日志（实时）
docker-compose -f docker-compose-orderbook.yml logs -f

# 重启服务
docker-compose -f docker-compose-orderbook.yml restart

# 停止服务
docker-compose -f docker-compose-orderbook.yml stop

# 停止并删除容器
docker-compose -f docker-compose-orderbook.yml down

# 重新构建并启动
docker-compose -f docker-compose-orderbook.yml up -d --build

# 查看服务状态
docker-compose -f docker-compose-orderbook.yml ps

# 执行命令
docker-compose -f docker-compose-orderbook.yml exec orderbook-gateio bash
```

---

## ⚠️ 常见问题解决

### 问题 1: 容器无法启动

```bash
# 查看详细错误
docker logs <container_id>

# 检查端口占用
lsof -i :27017

# 检查卷权限
ls -la app/data
```

### 问题 2: 内存不足

```bash
# 查看内存使用
docker stats --no-stream

# 设置内存限制
docker run --memory="2g" ...

# 或在 docker-compose.yml 中设置
deploy:
  resources:
    limits:
      memory: 2G
```

### 问题 3: 日志过大

```bash
# 查看日志大小
docker inspect --format='{{.LogPath}}' <container_id> | xargs ls -lh

# 清空日志
truncate -s 0 $(docker inspect --format='{{.LogPath}}' <container_id>)

# 配置日志轮转（在 docker-compose.yml）
logging:
  driver: "json-file"
  options:
    max-size: "100m"
    max-file: "5"
```

---

## 📚 相关文档

- [Docker 日志记录与错误排查](./DOCKER_LOGGING_AND_DEBUGGING.md)
- [订单簿数据采集指南](./ORDERBOOK_COLLECTION_GUIDE.md)
- [AWS Lightsail 部署指南](./AWS_LIGHTSAIL_DEPLOYMENT_GUIDE.md)

---

**最后更新**: 2024-11-18

