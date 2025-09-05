# 🐳 Docker 容器部署指南

## 快速开始

### 1. 构建容器
```bash
./build.sh
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件配置你的凭证
```

### 3. 运行容器
```bash
./run.sh
```

### 4. 访问应用
- **前端界面**: http://localhost:8501
- **API文档**: http://localhost:8000/docs

### 5. 停止容器
```bash
./stop.sh
```

## 环境变量配置

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，配置你的凭证：
```bash
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-east-1
TRINO_HOST=your-trino-host
TRINO_PORT=8889
TRINO_USER=your-username
```

## 使用Docker Compose（可选）

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down
```

## 数据持久化

容器会自动挂载以下目录：
- `./data` - 输入数据文件
- `./output` - 输出结果文件
- `./logs` - 日志文件

## 故障排除

### 查看容器日志
```bash
docker logs -f ads-data-insight
```

### 进入容器调试
```bash
docker exec -it ads-data-insight bash
```