# Trino数据库连接配置
from strands.models import BedrockModel

TRINO_CONFIG = {
    "TRINO_HOST": "172.31.38.156",
    "TRINO_PORT": "8889", 
    "TRINO_USER": "hadoop"
}
model = BedrockModel(
                model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                region_name="us-east-1"
            )