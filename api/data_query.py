import os
import tempfile
from typing import Optional
import logging

import boto3
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Request

from agent.core_agent import CoreAgent
from config.logger_config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/data-query", tags=["data-query"])


@router.post("/upload-file")
async def query_with_upload_file(
    request: Request,
    user_input: str = Form(...),
    file: UploadFile = File(...)
):
    """根据用户输入和上传文件返回数据"""
    try:
        # 保存上传文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # 更新用户输入中的文件路径
        updated_input = user_input + temp_file_path
        logger.info(f"updated_input:{updated_input}")

        # 执行查询
        core_agent = CoreAgent()
        result = core_agent.run(updated_input)

        # 清理临时文件
        try:
            os.unlink(temp_file_path)
        except OSError:
            pass
        
        # 将文件路径转换为HTTP下载地址
        if result and os.path.exists(result):
            filename = os.path.basename(result)
            base_url = f"{request.url.scheme}://{request.url.netloc}"
            download_url = f"{base_url}/download/{filename}"
            return {"download_url": download_url}
        else:
            return {"result": result}
        
    except Exception as e:
        logger.error(f"Error in query_with_upload_file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/file-path")
async def query_with_file_path(
    request: Request,
    user_input: str = Form(...),
    file_path: str = Form(...)
):
    """根据用户输入和文件路径返回数据"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"文件不存在: {file_path}")
        
        # 更新用户输入中的文件路径
        updated_input = user_input.replace("input.csv", file_path)
        
        # 执行查询
        core_agent = CoreAgent()
        result = core_agent.run(updated_input)
        
        # 将文件路径转换为HTTP下载地址
        if result and os.path.exists(result):
            filename = os.path.basename(result)
            base_url = f"{request.url.scheme}://{request.url.netloc}"
            download_url = f"{base_url}/download/{filename}"
            return {"download_url": download_url}
        else:
            return {"result": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/s3-path")
async def query_with_s3_path(
    request: Request,
    user_input: str = Form(...),
    s3_path: str = Form(...),
    aws_access_key_id: Optional[str] = Form(None),
    aws_secret_access_key: Optional[str] = Form(None),
    aws_region: str = Form("us-east-1")
):
    """根据用户输入和S3路径返回数据"""
    try:
        # 解析S3路径
        if not s3_path.startswith("s3://"):
            raise HTTPException(status_code=400, detail="S3路径必须以s3://开头")
        
        s3_path_parts = s3_path[5:].split("/", 1)
        bucket_name = s3_path_parts[0]
        object_key = s3_path_parts[1] if len(s3_path_parts) > 1 else ""
        
        # 创建S3客户端
        s3_client = boto3.client('s3')
        
        # 下载文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{os.path.basename(object_key)}") as temp_file:
            s3_client.download_fileobj(bucket_name, object_key, temp_file)
            temp_file_path = temp_file.name
        
        # 更新用户输入中的文件路径
        updated_input = user_input.replace("input.csv", temp_file_path)
        
        # 执行查询
        core_agent = CoreAgent()
        result = core_agent.run(updated_input)
        
        # 清理临时文件
        try:
            os.unlink(temp_file_path)
        except OSError:
            pass
        
        # 将文件路径转换为HTTP下载地址
        if result and os.path.exists(result):
            filename = os.path.basename(result)
            base_url = f"{request.url.scheme}://{request.url.netloc}"
            download_url = f"{base_url}/download/{filename}"
            return {"download_url": download_url}
        else:
            return {"result": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))