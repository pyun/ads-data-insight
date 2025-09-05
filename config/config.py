# Trino数据库连接配置
from strands.models import BedrockModel
import os

TRINO_CONFIG = {
    "TRINO_HOST": os.getenv("TRINO_HOST") or "172.31.38.156",
    "TRINO_PORT": os.getenv("TRINO_PORT") or "8889",
    "TRINO_USER": os.getenv("TRINO_USER") or "hadoop"
}
model = BedrockModel(
                model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                region_name="us-east-1"
            )