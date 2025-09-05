import logging
from typing import Optional
import os
os.environ["AWS_REGION"] = "ap-southeast-1"

from strands import Agent
from mcp import StdioServerParameters, stdio_client
from strands.handlers.callback_handler import PrintingCallbackHandler
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from strands_tools import file_read, file_write, shell, use_aws, python_repl
from config.logger_config import setup_logger
from config.config import TRINO_CONFIG
from config.config import model
from handler.handler import AgentHandler

setup_logger()
logger = logging.getLogger(__name__)


# GAID代理系统提示词
SYSTEM_PROMPT = """
你是一个数据分析专家，我有一个数据表格，需要你完成如下任务：
1. 将表格中gaid列的数据抽取出来，生成一个只包含一列，列名是gaid的csv文件，文件名保持不变；
2. 将该文件上传到s3，s3目录：s3://pyuntestbucket1/trino/input/[文件名，去掉扩展名]/
3. 然后用trino mcp，在hive.default中创建一个临时表，表名与文件名同名，表的external_location指定为上一步上传对象的目录；
# trino连接信息：
    ## "TRINO_HOST": {TRINO_HOST}
    ## "TRINO_PORT": {TRINO_PORT}
    ## "TRINO_USER": {TRINO_USER}
# 判断逻辑：
    ## 请处理csv中所有数据，忽略用户输入的其他提示信息
# 请严格按照如下要求输出结果，不要总结、不要前言
    ## 请返回hive.default.[临时表名]
# 请始终用中文输出和交互
"""


class GaidAgent:
    """
    GAID代理类，负责从 CSV 文件中提取 GAID 数据
    根据数据量大小决定返回列表或创建临时表
    """
    
    def __init__(self, sys_prompt: Optional[str] = None):
        """初始化GAID代理
        
        Args:
            sys_prompt: 系统提示词，默认使用内置提示词
        """
        self.sys_prompt = sys_prompt if sys_prompt is not None else SYSTEM_PROMPT
        self.sys_prompt = self.sys_prompt.format(**TRINO_CONFIG)
        self.server = None
        logger.info("初始化GaidAgent")

        try:
            self._initialize_mcp_server()
            logger.info("GaidAgent初始化成功")
        except Exception as e:
            logger.error(f"GaidAgent初始化失败: {e}")
            raise

        logger.info(f"system prompt: {self.sys_prompt}")
    
    def _initialize_mcp_server(self):
        """初始化MCP服务器连接"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            mcp_server_file = os.path.join(
                os.path.dirname(base_dir), "trino-mcp/server.py")
            params = StdioServerParameters(
                command="python",
                args=[mcp_server_file],
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
                #tools.extend(self.server.list_tools_sync())
                # 将self.server.list_tools_sync()的所有元素加到tools之前 
                tools = self.server.list_tools_sync() + tools
                logger.debug(f"已添加MCP工具，总工具数: {len(tools)}")
            
            agent = Agent(
                model=model,
                tools=tools,
                system_prompt=self.sys_prompt,
                callback_handler=AgentHandler()
            )
            
            logger.debug("Agent创建成功")
            return agent
            
        except Exception as e:
            logger.error(f"Agent创建失败: {e}")
            raise
    
    def run(self, user_prompt: str):
        """运行 GAID 提取任务
        
        Args:
            user_prompt: 用户输入的提示词
            
        Returns:
            代理的响应结果
        """
        if not user_prompt or not user_prompt.strip():
            logger.warning("用户输入为空")
            return "错误：用户输入不能为空"
        
        logger.info(f"开始运行GAID提取任务，输入: {user_prompt[:100]}...")  # 限制日志长度
        
        try:
            agent = self._create_agent()
            response = agent(user_prompt)
            
            # 记录执行指标
            if hasattr(response, 'metrics') and response.metrics:
                total_tokens = response.metrics.accumulated_usage.get('totalTokens', 0)
                execution_time = sum(response.metrics.cycle_durations) if response.metrics.cycle_durations else 0
                tools_used = list(response.metrics.tool_metrics.keys()) if response.metrics.tool_metrics else []
                
                logger.info(f"GAID代理执行指标 - Token数: {total_tokens}, 执行时间: {execution_time:.2f}秒, 使用工具: {tools_used}")
            
            logger.info(f"GAID代理返回结果: {str(response)[:200]}...")  # 限制日志长度
            return response
            
        except Exception as e:
            error_msg = f"GAID代理运行失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return f"错误：{error_msg}"