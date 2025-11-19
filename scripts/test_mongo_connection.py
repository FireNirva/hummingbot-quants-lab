#!/usr/bin/env python3
"""
快速测试 MongoDB 连接
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import sys

def test_connection(uri):
    """测试MongoDB连接"""
    print(f"\n🔌 测试连接: {uri[:50]}...")
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # 触发实际连接
        info = client.server_info()
        print(f"   ✅ 连接成功!")
        print(f"   MongoDB 版本: {info.get('version', 'unknown')}")
        
        # 列出数据库
        dbs = client.list_database_names()
        print(f"   📚 可用数据库: {', '.join(dbs)}")
        
        client.close()
        return True
    except ConnectionFailure as e:
        print(f"   ❌ 连接失败: {e}")
        return False
    except OperationFailure as e:
        print(f"   ❌ 认证失败: {e}")
        return False
    except Exception as e:
        print(f"   ❌ 错误: {type(e).__name__}: {e}")
        return False

def main():
    print("=" * 80)
    print("MongoDB 连接测试")
    print("=" * 80)
    
    # 测试不同的连接字符串
    test_uris = [
        ("不带认证", "mongodb://localhost:27017/"),
        ("admin认证", "mongodb://admin:admin@localhost:27017/"),
        ("指定数据库", "mongodb://admin:admin@localhost:27017/quants_lab"),
        ("完整URI (来自.env)", "mongodb://admin:admin@localhost:27017/quants_lab?authSource=admin"),
    ]
    
    results = []
    for name, uri in test_uris:
        success = test_connection(uri)
        results.append((name, success))
    
    # 总结
    print("\n" + "=" * 80)
    print("📊 测试总结")
    print("=" * 80)
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"   {status} {name}")
    
    # 建议
    print("\n💡 建议:")
    if any(success for _, success in results):
        working_uri = next(uri for (name, uri), success in zip(test_uris, results) if success)
        print(f"   使用这个连接字符串: {working_uri}")
    else:
        print("   所有连接都失败了！")
        print("   1. 检查 MongoDB 容器是否真的在运行: docker ps | grep mongodb")
        print("   2. 查看 MongoDB 日志: docker logs mongodb")
        print("   3. 重启 MongoDB: docker restart mongodb")

if __name__ == "__main__":
    main()

