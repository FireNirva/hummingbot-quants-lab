# Git Commit 计划

## 📋 Commit 分组策略

### Commit 1: 清理 OKX 爬虫数据（非核心功能）
- 删除 scripts/data/okx_docs/

### Commit 2: 清理测试脚本和临时工具
- 删除所有 test_*.py
- 删除调试脚本
- 删除 PDF/代币提取工具
- 删除验证脚本

### Commit 3: 核心功能改进
- 修改 scripts/analyze_cex_dex_spread.py（NaN处理）
- 修改 scripts/download_dex_ohlcv.py（池子选择逻辑）
- 修改 scripts/import_freqtrade_data.py（MEXC支持）
- 修改 core/services/pool_mapping.py
- 修改配置文件

### Commit 4: 订单簿采集系统
- 新增 app/tasks/data_collection/orderbook_snapshot_task.py
- 修改 core/tasks/orchestrator.py（调度优化）
- 新增订单簿配置文件

### Commit 5: 套利策略文档
- 新增套利相关文档

### Commit 6: AWS 部署
- 新增 AWS 部署文档和脚本

### Commit 7: 数据采集文档
- 新增数据采集相关文档

### Commit 8: 订单簿采集文档
- 新增订单簿采集相关文档

### Commit 9: 辅助脚本
- 新增订单簿管理脚本
- 新增分析脚本

### Commit 10: 项目整理
- 更新 README.md
- 新增 docs/INDEX.md
- 新增 scripts/README.md
- 新增清理总结

