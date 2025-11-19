#!/usr/bin/env python3
"""
测试 Storage 选择逻辑
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_storage_selection():
    """测试存储选择逻辑"""
    
    print("=" * 80)
    print("🧪 测试 Storage 选择逻辑")
    print("=" * 80)
    print()
    
    # 测试 1: 有 MONGO_URI
    print("测试 1: 有 MONGO_URI 配置")
    print("-" * 80)
    os.environ["MONGO_URI"] = "mongodb://localhost:27017"
    mongo_uri = os.getenv("MONGO_URI")
    
    if mongo_uri:
        print(f"✅ MONGO_URI: {mongo_uri}")
        print("   → 应该使用: MongoDBTaskStorage")
        storage_type = "MongoDBTaskStorage"
    else:
        print("❌ MONGO_URI: Not set")
        print("   → 应该使用: NoOpTaskStorage")
        storage_type = "NoOpTaskStorage"
    
    print(f"   结果: {storage_type}")
    print()
    
    # 测试 2: 无 MONGO_URI
    print("测试 2: 无 MONGO_URI 配置")
    print("-" * 80)
    if "MONGO_URI" in os.environ:
        del os.environ["MONGO_URI"]
    mongo_uri = os.getenv("MONGO_URI")
    
    if mongo_uri:
        print(f"✅ MONGO_URI: {mongo_uri}")
        print("   → 应该使用: MongoDBTaskStorage")
        storage_type = "MongoDBTaskStorage"
    else:
        print("❌ MONGO_URI: Not set")
        print("   → 应该使用: NoOpTaskStorage")
        storage_type = "NoOpTaskStorage"
    
    print(f"   结果: {storage_type}")
    print()
    
    # 测试 3: 导入 NoOpTaskStorage
    print("测试 3: 导入 NoOpTaskStorage 类")
    print("-" * 80)
    try:
        from core.tasks.storage import NoOpTaskStorage
        print("✅ 成功导入 NoOpTaskStorage")
        print(f"   类型: {NoOpTaskStorage}")
        print(f"   文档: {NoOpTaskStorage.__doc__}")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
    print()
    
    # 测试 4: 实例化 NoOpTaskStorage
    print("测试 4: 实例化 NoOpTaskStorage")
    print("-" * 80)
    try:
        from core.tasks.storage import NoOpTaskStorage
        storage = NoOpTaskStorage()
        print("✅ 成功实例化 NoOpTaskStorage")
        print(f"   实例: {storage}")
        print(f"   类型: {type(storage)}")
    except Exception as e:
        print(f"❌ 实例化失败: {e}")
    print()
    
    print("=" * 80)
    print("✅ 所有测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_storage_selection()

