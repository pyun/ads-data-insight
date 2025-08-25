import os

# Trino数据库连接配置
from strands.models import BedrockModel

# TRINO_CONFIG = {
#     "TRINO_HOST": "172.31.38.156",
#     "TRINO_PORT": "8889",
#     "TRINO_USER": "hadoop"
# }
TRINO_CONFIG = {
    "TRINO_HOST": os.getenv("TRINO_HOST") or "172.31.38.156",
    "TRINO_PORT": os.getenv("TRINO_PORT") or "8889",
    "TRINO_USER": os.getenv("TRINO_USER") or "hadoop",
    "TRINO_PASSWORD": os.getenv("TRINO_PASSWORD") or "",
    "TRINO_CATALOG": os.getenv("TRINO_CATALOG") or "",
    "TRINO_SCHEMA": os.getenv("TRINO_SCHEMA") or "",
    "TRINO_HTTP_SCHEME": os.getenv("TRINO_HTTP_SCHEME") or "http",
    "TRINO_COMMAND": os.getenv("TRINO_MCP_PY") or "/data/mcp-trino-python/src/server_stdio.py",
}
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-east-1",
    # inference_profile_arn="arn:aws:bedrock:us-east-1:xxx:application-inference-profile/xxx"
)

# SQL代理系统提示词
SYSTEM_SQL_PROMPT = None

