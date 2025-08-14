# 广告投放数据洞察前端

这是一个基于Streamlit构建的广告投放数据洞察前端应用。

## 功能特性

- 📊 广告渠道数据分析
- 📝 工单内容输入
- 📁 CSV文件上传（支持拖拽）
- 🔗 分析结果下载

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

### 方式1：使用脚本
```bash
./run.sh
```

### 方式2：直接运行
```bash
streamlit run app.py
```

应用将在 http://localhost:8501 启动

## API接口

应用会向 `/api/analyze` 接口提交数据，请确保后端API服务正常运行。

## 使用说明

1. 在左侧栏选择"广告渠道数据分析"
2. 输入工单内容
3. 上传CSV格式的gaid文件
4. 点击提交按钮
5. 查看分析结果并下载

## 输入数据样例

1. gaid：input.csv
2. 包名:com.example.social
3. 事件名称:install
4. 时间周期:20250701-20250811