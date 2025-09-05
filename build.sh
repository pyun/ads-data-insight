#!/bin/bash

echo "🚀 构建广告投放数据洞察系统容器..."

# 构建Docker镜像
docker build -t ads-data-insight:latest .

echo "✅ 容器构建完成！"
echo "📋 使用以下命令运行容器："
echo "   ./run.sh"