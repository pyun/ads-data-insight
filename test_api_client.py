#!/usr/bin/env python3
"""
API客户端测试代码
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_upload_file():
    """测试文件上传接口"""
    print("=== 测试文件上传接口 ===")
    
    url = f"{BASE_URL}/data-query/upload-file"
    
    # 准备测试数据
    user_input = """
    1. gaid：input.csv
    2. 包名:com.example.social
    3. 事件名称:install
    4. 时间周期:20250701-20250811
    """
    
    # 上传文件
    with open("data/input1.csv", "rb") as f:
        files = {"file": ("input.csv", f, "text/csv")}
        data = {"user_input": user_input}
        
        response = requests.post(url, files=files, data=data)
        
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_file_path():
    """测试文件路径接口"""
    print("=== 测试文件路径接口 ===")
    
    url = f"{BASE_URL}/data-query/file-path"
    
    data = {
        "user_input": """
        1. gaid：input.csv
        2. 包名:com.example.social
        3. 事件名称:install
        4. 时间周期:20250701-20250811
        """,
        "file_path": "/data/genai/ads-data-insight/data/input1.csv"
    }
    
    response = requests.post(url, data=data)
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_s3_path():
    """测试S3路径接口"""
    print("=== 测试S3路径接口 ===")
    
    url = f"{BASE_URL}/data-query/s3-path"
    
    data = {
        "user_input": """
        1. gaid：input.csv
        2. 包名:com.example.social
        3. 事件名称:install
        4. 时间周期:20250701-20250811
        """,
        "s3_path": "s3://pyuntestbucket1/trino/input1.csv",
        "aws_region": "us-east-1"
    }
    
    response = requests.post(url, data=data)
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    
    response = requests.get(f"{BASE_URL}/health")
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def main():
    """运行所有测试"""
    print("开始API客户端测试...\n")
    
    try:
        # 测试健康检查
        # test_health_check()
        
        # 测试文件路径接口
        test_file_path()
        
        # 测试文件上传接口
        # test_upload_file()
        
        # 测试S3路径接口（需要配置AWS凭证）
        # test_s3_path()
        
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到API服务器，请确保服务已启动")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    main()