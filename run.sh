#!/bin/bash

echo "🚀 启动广告投放数据洞察系统..."

# 检查镜像是否存在
if ! docker images ads-data-insight:latest | grep -q ads-data-insight; then
    echo "❌ 镜像不存在，请先运行 ./build.sh 构建镜像"
    exit 1
fi

# 停止并删除已存在的容器
docker stop ads-data-insight 2>/dev/null || true
docker rm ads-data-insight 2>/dev/null || true

# 检查.env文件
if [ ! -f .env ]; then
    echo "⚠️  .env文件不存在，请复制.env.example并配置环境变量"
    echo "   cp .env.example .env"
    exit 1
fi

# 运行容器
docker run -d \
    --name ads-data-insight \
    -p 8000:8000 \
    -p 8501:8501 \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/output:/app/output \
    -v $(pwd)/logs:/app/logs \
    --env-file .env \
    ads-data-insight:latest

echo "✅ 容器启动成功！"
echo "🌐 访问地址："
echo "   前端界面: http://localhost:8501"
echo "   API文档:  http://localhost:8000/docs"
echo ""
echo "📋 管理命令："
echo "   查看日志: docker logs -f ads-data-insight"
echo "   停止容器: docker stop ads-data-insight"