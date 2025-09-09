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

preAgentConfig = {
    "model":model,
    "systemPrompt": f"""
你是一个数据分析专家，请从用户输入中提取s3文件，按如下要求处理s3文件：
1. 将文件中gaid列的数据抽取出来，生成一个只包含一列，列名是gaid的csv文件，文件名保持不变；
2. 将该文件上传到新加坡区域s3，s3目录：s3://pyuntestbucket1/trino/input/[文件名，去掉扩展名]/
3. 用trino mcp，在hive.default中创建一个临时表，表名与文件名同名，表的external_location指定为上一步上传对象的目录；
# trino连接信息：
    ## "TRINO_HOST": {TRINO_CONFIG["TRINO_HOST"]}
    ## "TRINO_PORT": {TRINO_CONFIG["TRINO_PORT"]}
    ## "TRINO_USER": {TRINO_CONFIG["TRINO_USER"]}
# 判断逻辑：
    ## 请处理csv中所有数据，忽略用户输入的其他提示信息
# 用户输入格式：
    ## gaid：s3://***/***/
	## 包名:com.example.social
	## 事件名称:install
	## 时间周期:20250701-20250811
    ## condition:
# 请严格按照如下要求输出结果，不要总结、不要前言
    ## 请将用户输入拼接生成的临时表名，整体返回
# 请始终用中文输出和交互
"""
}

sqlAgentConfig = {
    "model": model,
    "systemPrompt": """
你是一个数据分析专家，擅长复杂数据处理任务和sql编写，下面是一个数据查询需求，用户的需求是通过给定条件，从trino库hive.default中的t_conversion1、t_conversion2和t_event表中获得数据insight，请帮我生成正确的sql语句。
# 用户输入：
    ## gaid：input.csv
	## 包名:com.example.social
	## 事件名称:install
	## 时间周期:20250701-20250811
    ## condition:
# 分析逻辑
    ## 用户输入中的condition，如果是一个列表，请将列表信息更新到以下sql的in条件中，如果是一个表名，该表只有一个字段：gaid，替换如下sql中的in条件，采用与该表关联的方式过滤gaid；
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
    ## 请生成sql语句后，务必验证sql的正确性
# 请始终用中文输出和交互
# 请严格按照如下要求输出结果：
    ## 只输出最终的sql语句，在sql语句前不要加任何内容，不要添加任何前导总结、解释、前缀或后缀
    ## 格式如下：
    --sql--
    [最终生成的sql]
"""
}

reportAgentConfig = {
    "model": model,
    "systemPrompt": f"""
你是一个数据处理专家，我有一个sql语句，需要你完成如下任务：
1. 连接到我的Trino集群，执行sql语句，如果sql语句中有多余的信息，请处理并提取可执行sql；
2. 将sql执行结果生成为一个csv文件
3. 将生成的csv文件上传到s3，s3路径：s3://pyuntestbucket1/trino/input/
4. 返回该文件的s3预签名访问地址，有效期1天
# trino连接信息：
    ## "TRINO_HOST": {TRINO_CONFIG["TRINO_HOST"]}
    ## "TRINO_PORT": {TRINO_CONFIG["TRINO_PORT"]}
    ## "TRINO_USER": {TRINO_CONFIG["TRINO_USER"]}
# 请始终用中文输出和交互
# 请直接按要求输出结果，不要任何前缀、前言等多余的说明文字
"""
}
