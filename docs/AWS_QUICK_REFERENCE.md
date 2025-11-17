# ☁️ AWS 部署快速参考卡片

> **一页纸总结 AWS 部署的关键信息**

---

## 🚀 三步部署

### **本地操作（10分钟）**

```bash
# 1️⃣ 修改配置
vim scripts/deploy_to_aws.sh
# 修改: AWS_IP="你的IP" 和 KEY_FILE="密钥路径"

# 2️⃣ 运行部署脚本
bash scripts/deploy_to_aws.sh

# 3️⃣ 完成！
```

---

## 📊 推荐配置

| 项目 | 配置 | 说明 |
|------|------|------|
| **实例类型** | `t3.medium` | 2 vCPU, 4GB RAM |
| **存储** | `500 GB gp3` | SSD，足够 2 个月 |
| **区域** | 新加坡/东京 | 低延迟 |
| **操作系统** | Ubuntu 22.04 LTS | 稳定 |
| **月费** | ~$75-80 | 约 ¥550/月 |

---

## 💰 成本明细

```
EC2 (t3.medium):  $30/月
EBS (500GB):      $40/月
数据传输:         $5-10/月
─────────────────────────
总计:             ~$75-80/月
```

---

## 🔧 常用命令

### **SSH 连接**

```bash
ssh -i ~/key.pem ubuntu@<AWS_IP>
```

### **服务管理**

```bash
# 查看状态
sudo systemctl status orderbook-collector

# 重启服务
sudo systemctl restart orderbook-collector

# 查看日志
tail -f ~/quants-lab/logs/orderbook_collection.log
```

### **监控检查**

```bash
# 健康检查
cd ~/quants-lab && python scripts/monitor_orderbook_collection.py

# 磁盘使用
df -h

# 数据大小
du -sh ~/quants-lab/app/data/cache/orderbook_snapshots/
```

### **数据管理**

```bash
# 清理旧数据
python scripts/cleanup_old_orderbook_data.py --days 7

# 下载数据到本地
scp -i ~/key.pem -r ubuntu@<IP>:~/quants-lab/app/data/cache/orderbook_snapshots/ ./
```

---

## 📈 性能指标

| 指标 | 目标值 | 告警阈值 |
|------|--------|---------|
| 采集成功率 | >99% | <95% |
| 数据滞后 | <10秒 | >30秒 |
| CPU 使用 | <50% | >90% |
| 磁盘使用 | <80% | >90% |
| 429错误率 | 0% | >1% |

---

## 💾 存储需求

| 时间周期 | 存储空间 |
|---------|---------|
| **每天** | 8.3 GB |
| **每周** | 58 GB |
| **每月** | 249 GB |
| **2个月** | 500 GB ✅ |

**清理策略**: 保留 7-14 天，旧数据自动清理

---

## ⚠️ 故障排查

### **服务未运行**

```bash
sudo systemctl start orderbook-collector
sudo journalctl -u orderbook-collector -n 50
```

### **429 限流错误**

```bash
grep "429" ~/quants-lab/logs/orderbook_collection.log
# 解决: 降低并发数 (MAX_CONCURRENT = 6)
```

### **磁盘满**

```bash
python scripts/cleanup_old_orderbook_data.py --days 3
```

### **数据滞后**

```bash
# 检查网络
ping api.gateio.ws

# 重启服务
sudo systemctl restart orderbook-collector
```

---

## 🔐 安全检查清单

- [ ] SSH 仅密钥登录（禁用密码）
- [ ] 安全组仅开放必要端口 (22, 443)
- [ ] 使用弹性 IP（固定地址）
- [ ] 启用 UFW 防火墙
- [ ] 配置 CloudWatch 告警
- [ ] 设置 EBS 自动快照
- [ ] 定期更新系统（自动安全更新）

---

## 📊 监控设置

### **Cron 任务**

```cron
# 每5分钟健康检查
*/5 * * * * python scripts/monitor_orderbook_collection.py

# 每天凌晨2点清理
0 2 * * * python scripts/cleanup_old_orderbook_data.py --days 7

# 每天凌晨3点检查磁盘
0 3 * * * df -h ~/quants-lab
```

### **CloudWatch 告警**

```
1. 磁盘使用 > 80%
2. CPU 使用 > 90% (5分钟)
3. 网络中断检测
```

---

## 🎯 AWS 控制台链接

| 服务 | 链接 |
|------|------|
| **EC2** | https://console.aws.amazon.com/ec2/ |
| **CloudWatch** | https://console.aws.amazon.com/cloudwatch/ |
| **SNS** | https://console.aws.amazon.com/sns/ |
| **IAM** | https://console.aws.amazon.com/iam/ |

---

## 📞 紧急联系

### **重启实例**

```
AWS Console → EC2 → 实例 → 重启
```

### **远程重启服务**

```bash
ssh -i ~/key.pem ubuntu@<IP> "sudo systemctl restart orderbook-collector"
```

### **远程健康检查**

```bash
ssh -i ~/key.pem ubuntu@<IP> "cd ~/quants-lab && python scripts/monitor_orderbook_collection.py"
```

---

## 🔄 更新部署

### **方法 1: 重新运行部署脚本**

```bash
# 在本地
bash scripts/deploy_to_aws.sh
```

### **方法 2: 手动更新单个文件**

```bash
# 上传文件
scp -i ~/key.pem file.py ubuntu@<IP>:~/quants-lab/

# 重启服务
ssh -i ~/key.pem ubuntu@<IP> "sudo systemctl restart orderbook-collector"
```

### **方法 3: Git 拉取**

```bash
# SSH 到服务器
ssh -i ~/key.pem ubuntu@<IP>

# 更新代码
cd ~/quants-lab
git pull

# 重启服务
sudo systemctl restart orderbook-collector
```

---

## 📚 完整文档

| 文档 | 说明 |
|------|------|
| [AWS 部署指南](AWS_DEPLOYMENT_GUIDE.md) | 详细部署步骤 |
| [快速启动](QUICKSTART_5S_ORDERBOOK.md) | 5秒采集指南 |
| [高频配置](HIGH_FREQUENCY_ORDERBOOK_SETUP.md) | 性能优化 |
| [API 限流](GATEIO_API_RATE_LIMITS.md) | 限流策略 |

---

## 🎊 关键优势

| 优势 | 说明 |
|------|------|
| ✅ **稳定性** | 24/7 运行，不受本地影响 |
| ✅ **性能** | 低延迟，快速响应 |
| ✅ **可扩展** | 按需扩展存储和计算 |
| ✅ **监控** | CloudWatch 专业监控 |
| ✅ **省心** | 自动化管理 |

---

## 📞 帮助资源

| 资源 | 链接 |
|------|------|
| **AWS 文档** | https://docs.aws.amazon.com/ |
| **EC2 用户指南** | https://docs.aws.amazon.com/ec2/ |
| **CloudWatch** | https://docs.aws.amazon.com/cloudwatch/ |
| **AWS 免费套餐** | https://aws.amazon.com/free/ |

---

## 🎯 检查清单

部署前：
- [ ] 创建 AWS 账号
- [ ] 创建 EC2 实例 (t3.medium, 500GB)
- [ ] 下载密钥文件 (.pem)
- [ ] 配置安全组 (SSH, HTTPS)
- [ ] 分配弹性 IP

部署后：
- [ ] SSH 连接成功
- [ ] 服务运行正常
- [ ] 数据正在采集
- [ ] Cron 任务配置
- [ ] CloudWatch 监控
- [ ] EBS 快照设置

---

**💡 提示**: 保存此页面作为快速参考！📋✨

