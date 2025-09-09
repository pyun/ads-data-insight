from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
import logging
from config.logger_config import setup_logger
from config.config import preAgentConfig
from config.config import sqlAgentConfig
from config.config import reportAgentConfig
from handler.handler import AgentHandler
from config.config import TRINO_CONFIG
from tools.strands.server import TrinoTools
from strands_tools import file_read, file_write, shell, use_aws, python_repl

setup_logger()
logger = logging.getLogger(__name__)

app = BedrockAgentCoreApp()

def process_workflow(self, user_input: str) -> str:
    """处理完整的数据分析工作流
    
    Args:
        user_input: 用户输入的查询需求
        
    Returns:
        str: 最终生成的SQL语句或错误信息
    """
    if not user_input or not user_input.strip():
        logger.warning("用户输入为空")
        return "错误：用户输入不能为空"
    
    logger.info(f"开始处理工作流，用户输入: {user_input}")  
    
    try:
        trino_mcp = TrinoTools(TRINO_CONFIG)

        # 步骤1: 生成GAID条件
        logger.debug("步骤1: 开始生成GAID条件")
        tools = [file_read, file_write, shell, use_aws, python_repl]
        preAgent = Agent(
            model=preAgentConfig.get("model"),
            tools=tools.extend(trino_mcp.list_tools()),
            system_prompt=preAgentConfig.get("systemPrompt"),
            callback_handler=AgentHandler()
        )
        condition = preAgent(user_input)

        # 步骤2: 生成SQL语句
        logger.debug("步骤2: 开始生成SQL语句")
        sqlAgent = Agent(
            model=sqlAgentConfig.get("model"),
            tools=trino_mcp.list_tools(),
            system_prompt=sqlAgentConfig.get("systemPrompt"),
            callback_handler=AgentHandler()
        )
        sql = sqlAgent(condition)

        # 步骤3: 执行SQL语句，生成报告
        logger.debug("步骤3: 开始生成报告")
        reportAgent = Agent(
            model=reportAgentConfig.get("model"),
            tools=[file_read, file_write, shell, use_aws, python_repl],
            system_prompt=reportAgentConfig.get("systemPrompt"),
            callback_handler=AgentHandler()
        )
        sql_results = reportAgent(sql)

        return str(sql_results)
        
    except Exception as e:
        error_msg = f"工作流处理失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return f"错误：{error_msg}"

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    result = process_workflow(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
