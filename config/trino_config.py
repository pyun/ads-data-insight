import os
# Trino数据库连接配置
TRINO_CONFIG = {
    "TRINO_HOST": os.getenv("TRINO_HOST") or "172.31.38.156",
    "TRINO_PORT": os.getenv("TRINO_PORT") or "8889",
    "TRINO_USER": os.getenv("TRINO_USER") or "hadoop",
    "TRINO_PASSWORD": os.getenv("TRINO_PASSWORD") or "",
    "TRINO_CATALOG": os.getenv("TRINO_CATALOG") or "hive",
    "TRINO_SCHEMA": os.getenv("TRINO_SCHEMA") or "default",
    "TRINO_HTTP_SCHEME": os.getenv("TRINO_HTTP_SCHEME") or "http",
}
