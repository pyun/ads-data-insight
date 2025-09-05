#!/bin/bash

echo "🛑 停止广告投放数据洞察系统..."

# 停止容器
docker stop ads-data-insight 2>/dev/null || echo "容器未运行"

# 删除容器
docker rm ads-data-insight 2>/dev/null || echo "容器不存在"

echo "✅ 系统已停止"