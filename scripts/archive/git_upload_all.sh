#!/bin/bash
# 自动化 Git Commit 和推送脚本

echo "🚀 开始 Git Commit 流程..."
echo ""

cd /Users/alice/Dropbox/投资/量化交易/quants-lab

# ============================================================================
# Commit 2: 清理测试脚本和临时工具
# ============================================================================
echo "📝 Commit 2: 清理测试脚本和临时工具..."

git rm -f scripts/debug_dex_data.py scripts/debug_okx_page.py \
  scripts/easyocr_extract.py scripts/extract_marked_tokens.py \
  scripts/manual_tokens_to_md.py scripts/monitor_crawl.py \
  scripts/okx_docs_crawler.py scripts/okx_docs_crawler_advanced.py \
  scripts/okx_docs_crawler_improved.py scripts/pdf_to_markdown.py \
  scripts/pdf_to_md_ocr.py scripts/quick_extract.py \
  scripts/run_dex_cex_aligned.py scripts/run_okx_crawler.py \
  scripts/test_crawler.py scripts/test_dex_ohlcv_system.py \
  scripts/test_dex_task.py scripts/test_improved_crawler.py \
  scripts/verify_cex_dex_alignment.py scripts/view_parquet.py \
  test_append.py test_download_now.py \
  docs/geckoterminal_api.md docs/IMPLEMENTATION_SUMMARY.md \
  TEST_RESULTS.md 2>/dev/null

git commit -m "chore: 清理测试脚本和临时工具

- 删除所有 test_*.py（已完成测试）
- 删除 OKX 爬虫脚本（非核心功能）
- 删除 PDF 处理工具（一次性使用）
- 删除代币提取工具（一次性使用）
- 删除调试和验证脚本
- 删除重复和临时文档
- 总计删除 26 个文件"

echo "✅ Commit 2 完成"
echo ""

# ============================================================================
# Commit 3: 核心功能改进
# ============================================================================
echo "📝 Commit 3: 核心功能改进..."

git add scripts/analyze_cex_dex_spread.py \
  scripts/download_dex_ohlcv.py \
  scripts/import_freqtrade_data.py \
  core/services/pool_mapping.py \
  core/tasks/orchestrator.py \
  config/base_ecosystem_downloader_full.yml \
  config/dex_candles_base.yml \
  docs/CEX_DEX_SPREAD_ANALYSIS.md \
  docs/COMMANDS_CHEATSHEET.md \
  docs/POOL_MAPPING_GUIDE.md

git commit -m "feat: 核心功能改进和Bug修复

改进:
- 价差分析支持 NaN/inf 处理
- DEX池子选择改为 volume_usd_h24（交易量）
- 数据导入支持 MEXC 交易所
- 任务调度精度优化到 0.5 秒（5秒订单簿采集）

修复:
- 修复 connector_name 属性错误
- 修复空数据 KeyError
- 修复池子映射逻辑

文件:
- scripts/analyze_cex_dex_spread.py
- scripts/download_dex_ohlcv.py
- scripts/import_freqtrade_data.py
- core/services/pool_mapping.py
- core/tasks/orchestrator.py"

echo "✅ Commit 3 完成"
echo ""

# ============================================================================
# Commit 4: 订单簿采集系统
# ============================================================================
echo "📝 Commit 4: 订单簿采集系统..."

git add app/tasks/data_collection/orderbook_snapshot_task.py \
  config/orderbook_snapshot_gateio.yml \
  config/orderbook_snapshot_gateio_optimized.yml \
  config/orderbook_snapshot_mexc.yml

git commit -m "feat: 实现高频订单簿数据采集系统

核心功能:
- ✅ 5秒间隔实时订单簿快照
- ✅ 100档深度数据采集
- ✅ 多交易所支持（Gate.io, MEXC）
- ✅ 数据完整性验证（sequence number）
- ✅ 并发控制（Semaphore 限流）
- ✅ 自动数据分区（按日期）

技术实现:
- asyncio 异步并发采集
- aiohttp 高性能 HTTP 请求
- Parquet 压缩存储
- 智能错误重试

文件:
- app/tasks/data_collection/orderbook_snapshot_task.py
- config/orderbook_snapshot_gateio.yml
- config/orderbook_snapshot_mexc.yml
- config/orderbook_snapshot_gateio_optimized.yml"

echo "✅ Commit 4 完成"
echo ""

# ============================================================================
# Commit 5: 配置文件
# ============================================================================
echo "📝 Commit 5: 新增配置文件..."

git add config/base_ecosystem_downloader_unavailable.yml \
  config/mexc_base_ecosystem_downloader.yml \
  config/token_mapping.yml \
  "config/geckoterminal_pairs_lists/markdown/⭐ Base_Arb _ CoinGecko.md" \
  "config/geckoterminal_pairs_lists/screenshot/⭐ Base_Arb _ CoinGecko.pdf" 2>/dev/null

git commit -m "feat: 新增多交易所配置支持

配置:
- MEXC Base 生态交易对
- Gate.io 不可用交易对列表
- Token 映射配置
- GeckoTerminal 交易对列表

支持交易所:
- Gate.io（主力）
- MEXC（补充）

支持网络:
- Base Chain
- BSC
- Solana"

echo "✅ Commit 5 完成"
echo ""

# ============================================================================
# Commit 6: AWS 部署
# ============================================================================
echo "📝 Commit 6: AWS 部署..."

git add docs/AWS_DEPLOYMENT_GUIDE.md \
  docs/AWS_QUICK_REFERENCE.md \
  docs/AWS_STORAGE_CALCULATION.md \
  scripts/aws_setup.sh \
  scripts/deploy_to_aws.sh

git commit -m "docs: AWS 部署完整指南

文档:
- ✅ EC2 实例配置
- ✅ systemd 服务管理
- ✅ CloudWatch 监控集成
- ✅ 存储需求计算
- ✅ 安全配置

脚本:
- ✅ 自动化部署脚本
- ✅ EC2 环境配置脚本

特性:
- 一键部署
- 自动化配置
- 监控告警
- 数据备份"

echo "✅ Commit 6 完成"
echo ""

# ============================================================================
# Commit 7: 套利策略文档
# ============================================================================
echo "📝 Commit 7: 套利策略文档..."

git add docs/ARBITRAGE_DATA_STRATEGY.md \
  docs/FINAL_SCORING_RESULTS.md \
  docs/CAPITAL_REQUIREMENT_ANALYSIS.md \
  docs/SCORING_FORMULA_OPTIMIZATION.md \
  docs/V4_VOLUME_THRESHOLD_OPTIMIZATION.md \
  docs/QUICK_REFERENCE_TRADE_SIZE.md

git commit -m "docs: CEX-DEX 套利策略文档

文档:
- ✅ 数据策略（回测/仓位管理时长）
- ✅ 评分公式优化
- ✅ 资金需求分析
- ✅ 交易规模快速参考
- ✅ 交易量阈值优化

分析:
- 32个交易对评分排名
- 流动性深度分析
- 最优交易规模计算
- 资金配置建议"

echo "✅ Commit 7 完成"
echo ""

# ============================================================================
# Commit 8: 数据采集文档
# ============================================================================
echo "📝 Commit 8: 数据采集文档..."

git add docs/ALTERNATIVE_DATA_SOURCES.md \
  docs/API_KEY_ANSWER.md \
  docs/CRYPTO_LAKE_INTEGRATION.md \
  docs/CRYPTO_LAKE_QUICKSTART.md \
  docs/GATEIO_API_RATE_LIMITS.md \
  docs/GATEIO_PUBLIC_API_VS_PRIVATE_API.md \
  docs/WORKFLOW_GUIDE.md \
  docs/QUICK_START_32PAIRS.md \
  docs/TOKEN_MAPPING_GUIDE.md

git commit -m "docs: 数据采集完整指南

文档:
- ✅ Crypto Lake 集成
- ✅ Gate.io API 使用
- ✅ 替代数据源
- ✅ 工作流程指南
- ✅ 快速入门指南

主题:
- API 限流说明
- 数据源对比
- 公共 vs 私有 API
- Token 映射配置"

echo "✅ Commit 8 完成"
echo ""

# ============================================================================
# Commit 9: 订单簿采集文档
# ============================================================================
echo "📝 Commit 9: 订单簿采集文档..."

git add docs/ORDERBOOK_COLLECTION_GUIDE.md \
  docs/ORDERBOOK_IMPLEMENTATION_EXPLAINED.md \
  docs/ORDERBOOK_SEQUENCE_NUMBER_EXPLAINED.md \
  docs/ORDERBOOK_UPDATE_ID_ANALYSIS.md \
  docs/ORDERBOOK_UPDATE_ID_CHANGELOG.md \
  docs/ORDERBOOK_SAMPLING_FREQUENCY_GUIDE.md \
  docs/ORDERBOOK_PRECISION_OPTIMIZATION.md \
  docs/ORDERBOOK_DATA_PARTITIONING.md \
  docs/ORDERBOOK_TIMEZONE_EXPLAINED.md \
  docs/ORDERBOOK_TASK_MANAGEMENT.md \
  docs/ORDERBOOK_CLEANUP_GUIDE.md \
  docs/HIGH_FREQUENCY_ORDERBOOK_SETUP.md \
  docs/QUICKSTART_5S_ORDERBOOK.md \
  docs/START_ORDERBOOK_COLLECTION.md \
  docs/STOP_TASKS_QUICK_GUIDE.md \
  docs/TIMEZONE_VISUAL_GUIDE.md \
  docs/LIQUIDITY_ANALYSIS_SUMMARY.md \
  docs/MULTI_EXCHANGE_ORDERBOOK_SETUP.md \
  docs/GATEIO_ORDERBOOK_STRUCTURE.md \
  docs/DELAY_ANALYSIS.md

git commit -m "docs: 订单簿采集系统完整文档

文档（20个）:
- ✅ 采集系统实现详解
- ✅ 高频采集配置（5秒）
- ✅ Sequence Number 说明
- ✅ 数据分区策略
- ✅ 时区和UTC说明
- ✅ 任务管理指南
- ✅ 流动性分析
- ✅ 多交易所设置

主题:
- 5秒高频采集
- 100档深度
- 数据完整性
- 并发控制
- 存储优化"

echo "✅ Commit 9 完成"
echo ""

# ============================================================================
# Commit 10: 辅助脚本
# ============================================================================
echo "📝 Commit 10: 辅助脚本..."

git add scripts/analyze_liquidity_and_capital.py \
  scripts/analyze_orderbook_data.py \
  scripts/batch_optimize_trade_size.py \
  scripts/calculate_optimal_trade_size.py \
  scripts/calculate_slippage_from_orderbook.py \
  scripts/check_orderbook_data.py \
  scripts/check_realtime_orderbook.py \
  scripts/clean_and_restart.sh \
  scripts/cleanup_old_orderbook_data.py \
  scripts/continue_analysis.sh \
  scripts/download_crypto_lake_data.py \
  scripts/get_realtime_orderbook.py \
  scripts/monitor_orderbook_collection.py \
  scripts/monitor_orderbook_liquidity.py \
  scripts/query_orderbook_by_date.py \
  scripts/quick_test_pairs.sh \
  scripts/restart_orderbook_gateio.sh \
  scripts/run_complete_analysis.sh \
  scripts/run_complete_analysis_manual.sh \
  scripts/run_dex_download_now.py \
  scripts/run_mexc_analysis.sh \
  scripts/status_orderbook_tasks.sh \
  scripts/stop_all_orderbook.sh \
  scripts/stop_orderbook_tasks.sh \
  scripts/switch_to_optimized_orderbook.sh

git commit -m "feat: 新增订单簿和套利分析脚本

订单簿管理（10个）:
- check_realtime_orderbook.py - 实时状态监控
- monitor_orderbook_liquidity.py - 流动性分析
- cleanup_old_orderbook_data.py - 自动清理
- restart/stop/status - 任务管理

套利分析（6个）:
- calculate_optimal_trade_size.py - 最优规模
- batch_optimize_trade_size.py - 批量优化
- analyze_liquidity_and_capital.py - 流动性分析
- calculate_slippage_from_orderbook.py - 滑点计算

工作流（5个）:
- run_complete_analysis.sh - 完整分析流程
- run_mexc_analysis.sh - MEXC 分析
- clean_and_restart.sh - 清理重启

数据下载（3个）:
- download_crypto_lake_data.py
- run_dex_download_now.py
- get_realtime_orderbook.py"

echo "✅ Commit 10 完成"
echo ""

# ============================================================================
# Commit 11: 项目整理
# ============================================================================
echo "📝 Commit 11: 项目整理和文档索引..."

git add README.md \
  docs/INDEX.md \
  scripts/README.md \
  docs/PROJECT_ORGANIZATION_SUMMARY.md \
  docs/CLEANUP_SUMMARY.md \
  docs/GIT_UPLOAD_GUIDE.md \
  CLEANUP_SUMMARY.md \
  GIT_UPLOAD_GUIDE.md \
  git_commit_plan.md 2>/dev/null

git commit -m "docs: 项目整理和完整索引

更新:
- ✅ 全新 README.md（中文，完整功能说明）
- ✅ docs/INDEX.md（57个文档完整索引）
- ✅ scripts/README.md（36个脚本完整索引）
- ✅ 项目整理总结
- ✅ 清理总结（45个文件）
- ✅ Git 上传指南

清理成果:
- 删除 45 个重复/临时文件
- 整理 docs/ 和 scripts/ 目录
- 根目录精简到 5 个文件
- 创建完整文档和脚本索引

项目特性:
- ✅ CEX-DEX 跨交易所套利
- ✅ 5秒高频订单簿采集
- ✅ 流动性分析和优化
- ✅ AWS 一键部署
- ✅ 完整文档系统"

echo "✅ Commit 11 完成"
echo ""

# ============================================================================
# 汇总
# ============================================================================

echo "=" * 80
echo ""
echo "✅ 所有 Commit 完成！"
echo ""
echo "📊 统计:"
echo "   • Commit 数量: 11 个"
echo "   • 删除文件: ~280 个"
echo "   • 新增文件: ~90 个"
echo "   • 修改文件: ~10 个"
echo ""
echo "🚀 准备推送到 GitHub..."
echo ""
echo "请运行以下命令推送:"
echo "   git push origin main"
echo ""
echo "或者添加远程仓库后推送:"
echo "   git remote add origin https://github.com/YOUR-USERNAME/REPO-NAME.git"
echo "   git push -u origin main"
echo ""

