#!/bin/bash

# 启动后端API服务（后台运行）
python app.py &

# 等待后端服务启动
sleep 5

# 启动前端服务
cd frontend && streamlit run app.py --server.port 8501 --server.address 0.0.0.0