import logging
from typing import Optional

from strands import Agent
from strands.handlers.callback_handler import PrintingCallbackHandler
from strands.models import BedrockModel
from strands_tools import file_read, file_write, shell, use_aws, python_repl
from config.logger_config import setup_logger
from config.config import TRINO_CONFIG
from config.config import model
from handler.handler import AgentHandler

setup_logger()
logger = logging.getLogger(__name__)

# GAID代理系统提示词
SYSTEM_PROMPT = """
你是一个数据分析专家，我有一个csv数据表格，需要你生成一个python脚本，将表格中gaid列的数据抽取出来，如果表格数据小于100条，请直接输出列表，否则，请连接trino库，在hive.default中创建一个temp_gaid的临时表，返回表名，如果temp_gaid表已存在，请清空后再插入数据；
# trino连接信息：
    ## "TRINO_HOST": {TRINO_HOST}
    ## "TRINO_PORT": {TRINO_PORT}
    ## "TRINO_USER": {TRINO_USER}
# 判断逻辑：
    ## 请处理csv中所有数据，忽略用户输入的其他提示信息
# 请严格按照如下要求输出结果，不要总结、不要前言
    ## 如果返回gaid列表，输出如下形式：[gaid1,gaid2,...gaidn]
    ## 如果返回是临时表，请返回hive.default.temp_gaid
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
        logger.info("初始化GaidAgent")
        logger.info(f"system prompt: {self.sys_prompt}")
        
    def _create_agent(self) -> Agent:
        """创建并配置 Agent 实例
        
        Returns:
            Agent: 配置好的 Agent 实例
        """
        try:
            tools = [python_repl,file_read, file_write, shell, use_aws]
            
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