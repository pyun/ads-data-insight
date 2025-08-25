import logging
from typing import Optional

from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.handlers.callback_handler import PrintingCallbackHandler
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from strands_tools import file_read, file_write, shell, use_aws, python_repl
from config.logger_config import setup_logger
from config.config import TRINO_CONFIG

setup_logger()
logger = logging.getLogger(__name__)

# SQL代理系统提示词
SYSTEM_PROMPT = """
你是一个数据分析专家，擅长复杂数据处理任务和sql编写，下面是一个数据查询需求，用户的需求是通过给定条件，从trino库hive.default中的t_conversion1、t_conversion2和t_event表中获得数据insight，请帮我生成正确的sql语句。
# 用户输入：
    ## gaid：input.csv
	## 包名:com.example.social
	## 事件名称:install
	## 时间周期:20250701-20250811
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


class SqlAgent:
    """
    SQL代理类，负责生成和执行SQL查询
    连接Trino数据库并提供数据分析功能
    """
    
    def __init__(self, sys_prompt: Optional[str] = None):
        """初始化SQL代理
        
        Args:
            sys_prompt: 系统提示词，默认使用内置提示词
        """
        self.sys_prompt = sys_prompt if sys_prompt is not None else SYSTEM_PROMPT
        self.server = None
        logger.info("初始化SqlAgent")
        
        try:
            self._initialize_mcp_server()
            logger.info("SqlAgent初始化成功")
        except Exception as e:
            logger.error(f"SqlAgent初始化失败: {e}")
            raise
    
    def _initialize_mcp_server(self):
        """初始化MCP服务器连接"""
        try:
            params = StdioServerParameters(
                command="python",
                args=[TRINO_CONFIG.get('TRINO_MCP_PY')],
                env=TRINO_CONFIG
            )
            
            # 创建MCP客户端
            self.server = MCPClient(lambda: stdio_client(params))
            self.server.start()
            logger.debug("MCP服务器连接成功")
            
        except Exception as e:
            logger.error(f"MCP服务器连接失败: {e}")
            raise
    
    def _create_agent(self) -> Agent:
        """创建并配置 Agent 实例
        
        Returns:
            Agent: 配置好的 Agent 实例
        """
        try:
            tools = [file_read, file_write, shell, use_aws, python_repl]
            
            # 添加MCP工具
            if self.server:
                tools.extend(self.server.list_tools_sync())
                logger.debug(f"已添加MCP工具，总工具数: {len(tools)}")
            
            model = BedrockModel(
                model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                region_name="us-east-1"
            )
            
            agent = Agent(
                model=model,
                tools=tools,
                system_prompt=self.sys_prompt,
                callback_handler=PrintingCallbackHandler()
            )
            
            logger.debug("SQL Agent创建成功")
            return agent
            
        except Exception as e:
            logger.error(f"SQL Agent创建失败: {e}")
            raise
    
    def run(self, user_prompt: str):
        """运行SQL生成和执行任务
        
        Args:
            user_prompt: 用户输入的提示词
            
        Returns:
            代理的响应结果
        """
        if not user_prompt or not user_prompt.strip():
            logger.warning("用户输入为空")
            return "错误：用户输入不能为空"
        
        logger.info(f"开始运行SQL任务，输入: {user_prompt[:100]}...")  # 限制日志长度
        
        try:
            agent = self._create_agent()
            response = agent(user_prompt)
            
            # 记录执行指标
            if hasattr(response, 'metrics') and response.metrics:
                total_tokens = response.metrics.accumulated_usage.get('totalTokens', 0)
                execution_time = sum(response.metrics.cycle_durations) if response.metrics.cycle_durations else 0
                tools_used = list(response.metrics.tool_metrics.keys()) if response.metrics.tool_metrics else []
                
                logger.info(f"SQL代理执行指标 - Token数: {total_tokens}, 执行时间: {execution_time:.2f}秒, 使用工具: {tools_used}")
            
            logger.info(f"SQL代理返回结果: {response}")  # 限制日志长度
            return response
            
        except Exception as e:
            error_msg = f"SQL代理运行失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return f"错误：{error_msg}"
    
    def __del__(self):
        """清理方法，在SqlAgent实例销毁时停止服务器"""
        try:
            if hasattr(self, 'server') and self.server:
                self.server.stop(None, None, None)
                logger.debug("MCP服务器已停止")
        except Exception as e:
            logger.warning(f"停止MCP服务器时出现警告: {e}")