from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

from api.data_query import router as data_query_router
from config.logger_config import setup_logger

setup_logger()

app = FastAPI(
    title="Data Query API",
    description="数据查询API服务",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(data_query_router)

@app.get("/")
async def root():
    return {"message": "Data Query API服务运行中"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/download/{filename}")
async def download_file(filename: str):
    # 使用绝对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(base_dir), "output")
    file_path = os.path.join(output_dir, filename)
    
    if os.path.exists(file_path):
        return FileResponse(
            file_path, 
            filename=filename, 
            media_type='application/octet-stream',
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "*"
            }
        )
    else:
        return {"error": "File not found"}