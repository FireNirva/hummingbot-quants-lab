#!/usr/bin/env python3
"""
测试 MongoDB 任务锁定逻辑

目的：诊断为什么 MEXC 任务无法获取锁定
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from pymongo import MongoClient


async def test_mark_task_running():
    """测试 MongoDB 的 mark_task_running 逻辑"""
    
    print("=" * 70)
    print("测试 MongoDB 任务锁定逻辑")
    print("=" * 70)
    
    client = MongoClient('mongodb://admin:admin@localhost:27017/')
    db = client['quants_lab']
    collection = db.task_schedules
    
    task_name = "test_mexc_task"
    
    # 1. 清理测试数据
    print(f"\n1. 清理测试数据...")
    collection.delete_many({'task_name': task_name})
    print(f"   ✅ 已清理")
    
    # 2. 第一次尝试获取锁（应该成功）
    print(f"\n2. 第一次尝试获取锁...")
    result = collection.update_one(
        {"task_name": task_name, "is_running": False},
        {
            "$set": {
                "is_running": True,
                "current_execution_id": "exec_1",
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    print(f"   modified_count: {result.modified_count}")
    
    if result.modified_count == 0:
        # 检查任务是否存在
        existing = collection.find_one({"task_name": task_name})
        if existing:
            print(f"   ❌ 任务已存在且正在运行: {existing}")
        else:
            # 创建新记录
            print(f"   任务不存在，创建新记录...")
            collection.insert_one({
                "task_name": task_name,
                "is_running": True,
                "current_execution_id": "exec_1",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            print(f"   ✅ 创建成功")
    else:
        print(f"   ✅ 获取锁成功")
    
    # 3. 查看当前状态
    print(f"\n3. 当前 MongoDB 状态:")
    task = collection.find_one({"task_name": task_name})
    if task:
        print(f"   task_name: {task['task_name']}")
        print(f"   is_running: {task['is_running']}")
        print(f"   execution_id: {task.get('current_execution_id')}")
    
    # 4. 第二次尝试获取锁（应该失败）
    print(f"\n4. 第二次尝试获取锁（模拟重复调度）...")
    result2 = collection.update_one(
        {"task_name": task_name, "is_running": False},
        {
            "$set": {
                "is_running": True,
                "current_execution_id": "exec_2",
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    print(f"   modified_count: {result2.modified_count}")
    
    if result2.modified_count == 0:
        existing = collection.find_one({"task_name": task_name})
        if existing and existing.get("is_running"):
            print(f"   ❌ 正确！任务正在运行，无法获取锁")
            return True  # 这是预期的行为
        else:
            print(f"   ⚠️  意外：任务存在但 is_running=False?")
            print(f"   {existing}")
    else:
        print(f"   ❌ 错误！不应该能获取锁两次")
        return False
    
    # 5. 释放锁
    print(f"\n5. 释放锁...")
    collection.update_one(
        {"task_name": task_name},
        {
            "$set": {
                "is_running": False,
                "current_execution_id": None,
                "updated_at": datetime.utcnow()
            }
        }
    )
    print(f"   ✅ 锁已释放")
    
    # 6. 第三次尝试获取锁（应该成功）
    print(f"\n6. 第三次尝试获取锁（锁已释放）...")
    result3 = collection.update_one(
        {"task_name": task_name, "is_running": False},
        {
            "$set": {
                "is_running": True,
                "current_execution_id": "exec_3",
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    print(f"   modified_count: {result3.modified_count}")
    
    if result3.modified_count > 0:
        print(f"   ✅ 正确！锁已释放，可以重新获取")
        return True
    else:
        print(f"   ❌ 错误！锁已释放但仍无法获取")
        return False
    
    # 清理
    collection.delete_many({'task_name': task_name})


async def test_mexc_specific():
    """测试 MEXC 特定的任务名"""
    
    print("\n" + "=" * 70)
    print("测试 MEXC 任务名 'orderbook_snapshot_mexc'")
    print("=" * 70)
    
    client = MongoClient('mongodb://admin:admin@localhost:27017/')
    db = client['quants_lab']
    collection = db.task_schedules
    
    task_name = "orderbook_snapshot_mexc"
    
    # 查看当前状态
    print(f"\n1. 查看当前 MongoDB 中的 MEXC 任务:")
    mexc_task = collection.find_one({"task_name": task_name})
    
    if mexc_task:
        print(f"   ❌ 找到 MEXC 任务记录:")
        for key, value in mexc_task.items():
            print(f"      {key}: {value}")
        
        print(f"\n2. 这就是问题所在！删除这条记录...")
        collection.delete_one({"task_name": task_name})
        print(f"   ✅ 已删除")
    else:
        print(f"   ✅ 未找到 MEXC 任务记录（这是正常的）")
    
    # 查看所有任务
    print(f"\n3. 所有任务记录:")
    all_tasks = list(collection.find())
    if all_tasks:
        for task in all_tasks:
            print(f"   • {task['task_name']}: is_running={task.get('is_running')}")
    else:
        print(f"   ✅ task_schedules 集合为空")


if __name__ == "__main__":
    print("\n🧪 MongoDB 任务锁定逻辑测试\n")
    
    try:
        asyncio.run(test_mark_task_running())
        asyncio.run(test_mexc_specific())
        
        print("\n" + "=" * 70)
        print("✅ 测试完成")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

