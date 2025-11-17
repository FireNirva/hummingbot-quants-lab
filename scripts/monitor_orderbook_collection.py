#!/usr/bin/env python3
"""
订单簿采集监控脚本

用途：
- 检查订单簿数据的实时性
- 监控采集成功率
- 检测数据滞后
- 生成健康报告

使用方法：
    python scripts/monitor_orderbook_collection.py
    
    # 或设置为定时任务
    */5 * * * * cd /path/to/quants-lab && python scripts/monitor_orderbook_collection.py >> logs/monitor.log 2>&1
"""

import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.data_paths import data_paths

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 配置
TRADING_PAIRS = [
    "IRON-USDT", "VIRTUAL-USDT", "MIGGLES-USDT", "BENJI-USDT", "AERO-USDT",
    "BRETT-USDT", "SOSO-USDT", "AWE-USDT", "CLANKER-USDT", "DEGEN-USDT",
    "AIXBT-USDT", "EDGE-USDT", "PRIME-USDT", "FAI-USDT", "FLOCK-USDT",
    "BNKR-USDT", "LMTS-USDT", "PRO-USDT", "PAAL-USDT", "COMMON-USDT",
    "PARTI-USDT", "PROMPT-USDT", "UNITE-USDT", "TALENT-USDT"
]

CONNECTOR = "gate_io"
EXPECTED_FREQUENCY_SECONDS = 5  # 预期采集频率
CHECK_WINDOW_MINUTES = 5  # 检查最近N分钟的数据


def get_orderbook_file(pair: str, date: datetime) -> Path:
    """获取订单簿文件路径"""
    date_str = date.strftime('%Y%m%d')
    filename = f"{CONNECTOR}_{pair.replace('-', '_')}_{date_str}.parquet"
    return data_paths.orderbook_snapshots_dir / filename


def check_pair_health(pair: str) -> dict:
    """检查单个交易对的健康状态"""
    now = datetime.now(timezone.utc)
    today_file = get_orderbook_file(pair, now)
    
    result = {
        'pair': pair,
        'has_data': False,
        'latest_time': None,
        'lag_seconds': None,
        'recent_count': 0,
        'expected_count': 0,
        'collection_rate': 0.0,
        'status': 'UNKNOWN',
        'warnings': []
    }
    
    if not today_file.exists():
        result['status'] = 'NO_FILE'
        result['warnings'].append(f"今日数据文件不存在: {today_file.name}")
        return result
    
    try:
        # 读取数据
        df = pd.read_parquet(today_file)
        
        if df.empty:
            result['status'] = 'EMPTY'
            result['warnings'].append("数据文件为空")
            return result
        
        result['has_data'] = True
        
        # 确保 timestamp 列是 datetime 类型
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 检查最新数据时间
        latest_time = df['timestamp'].max()
        
        # 如果 latest_time 是 naive，添加 UTC 时区
        if latest_time.tzinfo is None:
            latest_time = latest_time.replace(tzinfo=timezone.utc)
        
        result['latest_time'] = latest_time
        
        # 计算滞后
        lag = (now - latest_time).total_seconds()
        result['lag_seconds'] = lag
        
        # 检查最近N分钟的采集率
        check_start = now - timedelta(minutes=CHECK_WINDOW_MINUTES)
        recent_df = df[df['timestamp'] >= check_start]
        
        result['recent_count'] = len(recent_df)
        result['expected_count'] = int((CHECK_WINDOW_MINUTES * 60) / EXPECTED_FREQUENCY_SECONDS)
        result['collection_rate'] = (result['recent_count'] / result['expected_count']) * 100 if result['expected_count'] > 0 else 0
        
        # 状态判断
        if lag > 60:  # 滞后超过1分钟
            result['status'] = 'CRITICAL'
            result['warnings'].append(f"数据严重滞后: {lag:.0f}秒")
        elif lag > 30:  # 滞后超过30秒
            result['status'] = 'WARNING'
            result['warnings'].append(f"数据滞后: {lag:.0f}秒")
        elif result['collection_rate'] < 80:  # 采集率低于80%
            result['status'] = 'WARNING'
            result['warnings'].append(f"采集率偏低: {result['collection_rate']:.1f}%")
        elif result['collection_rate'] < 90:  # 采集率低于90%
            result['status'] = 'OK'
            result['warnings'].append(f"采集率可接受: {result['collection_rate']:.1f}%")
        else:
            result['status'] = 'HEALTHY'
        
    except Exception as e:
        result['status'] = 'ERROR'
        result['warnings'].append(f"读取数据错误: {str(e)}")
        logger.error(f"Error checking {pair}: {e}", exc_info=True)
    
    return result


def generate_report(results: list) -> dict:
    """生成总体健康报告"""
    total = len(results)
    healthy = sum(1 for r in results if r['status'] == 'HEALTHY')
    ok = sum(1 for r in results if r['status'] == 'OK')
    warning = sum(1 for r in results if r['status'] == 'WARNING')
    critical = sum(1 for r in results if r['status'] == 'CRITICAL')
    error = sum(1 for r in results if r['status'] in ['ERROR', 'NO_FILE', 'EMPTY', 'UNKNOWN'])
    
    avg_collection_rate = sum(r['collection_rate'] for r in results if r['has_data']) / max(1, sum(1 for r in results if r['has_data']))
    
    avg_lag = sum(r['lag_seconds'] for r in results if r['lag_seconds'] is not None) / max(1, sum(1 for r in results if r['lag_seconds'] is not None))
    
    report = {
        'timestamp': datetime.now(timezone.utc),
        'total_pairs': total,
        'healthy': healthy,
        'ok': ok,
        'warning': warning,
        'critical': critical,
        'error': error,
        'avg_collection_rate': avg_collection_rate,
        'avg_lag_seconds': avg_lag,
        'overall_status': 'HEALTHY' if (healthy + ok) / total > 0.9 else ('WARNING' if warning > 0 else 'CRITICAL')
    }
    
    return report


def print_report(results: list, report: dict):
    """打印格式化报告"""
    print("\n" + "=" * 80)
    print(f"📊 订单簿采集健康报告 - {report['timestamp'].strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    
    # 总体状态
    status_emoji = {
        'HEALTHY': '✅',
        'WARNING': '⚠️',
        'CRITICAL': '🔴'
    }
    
    print(f"\n{status_emoji.get(report['overall_status'], '❓')} 总体状态: {report['overall_status']}")
    print(f"\n📈 统计摘要:")
    print(f"   • 总交易对: {report['total_pairs']}")
    print(f"   • ✅ 健康: {report['healthy']} ({report['healthy']/report['total_pairs']*100:.1f}%)")
    print(f"   • 🟢 正常: {report['ok']} ({report['ok']/report['total_pairs']*100:.1f}%)")
    print(f"   • ⚠️  警告: {report['warning']} ({report['warning']/report['total_pairs']*100:.1f}%)")
    print(f"   • 🔴 严重: {report['critical']} ({report['critical']/report['total_pairs']*100:.1f}%)")
    print(f"   • ❌ 错误: {report['error']} ({report['error']/report['total_pairs']*100:.1f}%)")
    
    print(f"\n📊 性能指标:")
    print(f"   • 平均采集率: {report['avg_collection_rate']:.1f}%")
    print(f"   • 平均数据滞后: {report['avg_lag_seconds']:.1f}秒")
    print(f"   • 检查窗口: 最近{CHECK_WINDOW_MINUTES}分钟")
    print(f"   • 预期频率: 每{EXPECTED_FREQUENCY_SECONDS}秒")
    
    # 问题详情
    problems = [r for r in results if r['status'] in ['WARNING', 'CRITICAL', 'ERROR', 'NO_FILE', 'EMPTY']]
    
    if problems:
        print(f"\n⚠️  需要关注的交易对 ({len(problems)}):")
        for r in problems:
            status_icon = {
                'WARNING': '⚠️',
                'CRITICAL': '🔴',
                'ERROR': '❌',
                'NO_FILE': '📁',
                'EMPTY': '📭'
            }
            icon = status_icon.get(r['status'], '❓')
            
            print(f"\n   {icon} {r['pair']} - {r['status']}")
            
            if r['latest_time']:
                print(f"      最新数据: {r['latest_time'].strftime('%Y-%m-%d %H:%M:%S UTC')}")
                print(f"      数据滞后: {r['lag_seconds']:.0f}秒")
            
            if r['has_data']:
                print(f"      采集率: {r['collection_rate']:.1f}% ({r['recent_count']}/{r['expected_count']})")
            
            if r['warnings']:
                for warning in r['warnings']:
                    print(f"      • {warning}")
    else:
        print(f"\n✅ 所有交易对运行正常！")
    
    # 推荐操作
    if report['overall_status'] == 'CRITICAL':
        print(f"\n🚨 推荐操作:")
        print(f"   1. 检查采集任务是否正在运行: ps aux | grep orderbook")
        print(f"   2. 查看任务日志: tail -100 logs/orderbook_collection.log")
        print(f"   3. 检查网络连接和Gate.io API状态")
        print(f"   4. 重启采集任务: python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml")
    elif report['overall_status'] == 'WARNING':
        print(f"\n💡 建议:")
        print(f"   1. 监控接下来几个周期的表现")
        print(f"   2. 检查是否有429限流错误: grep '429' logs/orderbook_collection.log")
        print(f"   3. 如果持续出现问题，考虑降低采集频率或减少并发数")
    
    print("\n" + "=" * 80 + "\n")


def main():
    """主函数"""
    logger.info("开始订单簿采集健康检查...")
    
    # 检查所有交易对
    results = []
    for pair in TRADING_PAIRS:
        logger.debug(f"检查 {pair}...")
        result = check_pair_health(pair)
        results.append(result)
    
    # 生成报告
    report = generate_report(results)
    
    # 打印报告
    print_report(results, report)
    
    # 返回状态码
    if report['overall_status'] == 'CRITICAL':
        sys.exit(2)
    elif report['overall_status'] == 'WARNING':
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

