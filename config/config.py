import os
# Trino数据库连接配置
from strands.models import BedrockModel

TRINO_CONFIG = {
    "TRINO_HOST": os.getenv("TRINO_HOST") or "172.31.38.156",
    "TRINO_PORT": os.getenv("TRINO_PORT") or "8889",
    "TRINO_USER": os.getenv("TRINO_USER") or "hadoop",
    "TRINO_PASSWORD": os.getenv("TRINO_PASSWORD") or "",
    "TRINO_CATALOG": os.getenv("TRINO_CATALOG") or "hive",
    "TRINO_SCHEMA": os.getenv("TRINO_SCHEMA") or "default",
    "TRINO_HTTP_SCHEME": os.getenv("TRINO_HTTP_SCHEME") or "http",
    "TRINO_CMD": os.getenv("TRINO_CMD") or "/opt/soft/mcp-server/mcp-trino-python/src/server_stdio.py",
}
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-east-1",
    inference_profile_arn="arn:aws:bedrock:us-east-1:xxx:application-inference-profile/xxx"
)

# SQL代理系统提示词
SYSTEM_SQL_PROMPT = """
你是一个数据分析专家，擅长复杂数据处理任务和sql编写，下面是一个数据查询需求，用户的需求是通过给定条件，从trino库hive.default中的t_conversion1、t_conversion2和t_event表中获得数据insight，请帮我生成正确的sql语句。
# 用户输入：
    ## gaid：input.csv
	## 包名:com.example.social
	## 事件名称:install
	## 时间周期:20250701-20250811
    ## condition:[]/*.csv
# 分析逻辑
    ## 首先分析用户输入中的condition，如果是一个列表，请将列表信息更新到以下sql的in条件中，如果是一个表名，该表只有一个字段：gaid，替换如下sql中的in条件，采用与该表关联的方式过滤gaid；
    ## 判断事件名称,严格按照事件名称，选择如下sql，填充条件执行：
        ### 如果事件名称是install执行如下sql：
        SELECT   DISTINCT dt
                ,pkg_name  
                ,second_channel  
                ,affiliate_id  
                ,nation
                ,gaid
                ,'pb' AS type 
        FROM t_conversion1  
        WHERE dt >= '[时间周期的开始时间]' 
        AND dt <= '[时间周期的结束时间]' 
        AND pkg_name IN ('[包名]')
        and gaid in ('[gaid 1]',
        '[gaid 2]',
        ...
            )
        UNION ALL  
            SELECT   DISTINCT dt
                    ,pkg_name  
                    ,second_channel  
                    ,affiliate_id  
                    ,nation
                    ,gaid
                    ,'reject' AS type 
            FROM t_conversion2
            WHERE dt >= '[时间周期的开始时间]'                 
            AND dt <= '[时间周期的结束时间]'            
            AND pkg_name IN ('[包名]')
            and gaid in ('[gaid 1]',
            '[gaid 2]',
            ...
                )
        ### 如果事件名称不是install，执行如下sql：
        SELECT DISTINCT  dt
            ,pkg_name  
            ,second_channel  
            ,affiliate_id  
            ,nation 
            ,event_name 
            ,gaid
        FROM t_event
       WHERE dt >= '[时间周期的开始时间]'                 
        AND dt <= '[时间周期的结束时间]'            
        AND pkg_name IN ('[包名]')  
        AND event_name='[事件名称]'
        and gaid in ('[gaid 1]',
            '[gaid 2]',
        ...
        )
    ## 不要尝试和执行不满足条件的查询，严格按照上述要求获取数据
    ## 请在生成sql前，阅读表结构，根据字段类型格式化条件数据
    ## 生成sql语句后，请查询前10条数据，验证sql的正确性
# 请始终用中文输出和交互
# 请严格按照如下要求输出结果：
    ## 只输出最终的sql语句，在sql语句前不要加任何内容，不要添加任何前导总结、解释、前缀或后缀
    ## 格式如下：
    --sql--
    [最终生成的sql]
"""
