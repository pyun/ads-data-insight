from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
import logging
from config.logger_config import setup_logger
from config.config import preAgentConfig
from config.config import sqlAgentConfig
from config.config import reportAgentConfig
from config.config import deployment
from handler.handler import AgentHandler
from config.config import TRINO_CONFIG
from tools.strands.server import TrinoTools
from strands_tools import file_read, file_write, shell, use_aws, python_repl,editor
from strands.handlers.callback_handler import PrintingCallbackHandler
from importlib.metadata import version
from strands_tools.code_interpreter import AgentCoreCodeInterpreter

setup_logger()
logger = logging.getLogger(__name__)

app = BedrockAgentCoreApp()
logger.info(f"---strands-agents-version:---- {version('strands-agents')}")

def process_workflow(user_input: str) -> str:
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
        tools = [use_aws,file_read, file_write]
        bedrock_agent_core_code_interpreter = AgentCoreCodeInterpreter(region="us-east-1",identifier="code_interpreter_tool_hy159-z0YhWHcibv")

        # 步骤1: 生成GAID条件
        logger.info("步骤1: 开始生成GAID条件")
        if deployment == "AGENTCORE":
            tools.append(bedrock_agent_core_code_interpreter.code_interpreter)
        elif deployment == "LOCAL":
            tools.append(python_repl)
        
        preAgent = Agent(
            model=preAgentConfig.get("model"),
            tools=trino_mcp.list_tools()+tools,
            system_prompt=preAgentConfig.get("systemPrompt"),
            callback_handler=PrintingCallbackHandler()
        )
        logger.info(f"preAgent使用了tools：{preAgent.tool_names}")
        condition = preAgent(user_input)
        logger.info(f"preAgent返回结果：{condition}")

        # 步骤2: 生成SQL语句
        logger.info("步骤2: 开始生成SQL语句")
        sqlAgent = Agent(
            model=sqlAgentConfig.get("model"),
            tools=trino_mcp.list_tools(),
            system_prompt=sqlAgentConfig.get("systemPrompt"),
            callback_handler=PrintingCallbackHandler()
        )
        sql = sqlAgent(str(condition))
        logger.info(f"sqlAgent返回结果：{sql}")

        # 步骤3: 执行SQL语句，生成报告
        logger.debug("步骤3: 开始生成报告")
        reportAgent = Agent(
            model=reportAgentConfig.get("model"),
            tools=tools,
            system_prompt=reportAgentConfig.get("systemPrompt"),
            callback_handler=PrintingCallbackHandler()
        )
        sql_results = reportAgent(str(sql))
        logger.info(f"reportAgent返回结果：{sql_results}")

        return str(sql_results)
        
    except Exception as e:
        error_msg = f"工作流处理失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return f"错误：{error_msg}"

def test():
    agent = Agent(
        system_prompt="你是一个AI助手，请根据我的要求，完成任务.",
        tools=[use_aws],
        callback_handler=PrintingCallbackHandler()
    )
    user_message = "帮我下载s3对象s3://pyunemrbucket/trino/input/input1.csv"
    result = agent(user_message)
    return result

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("prompt", """
    gaid：s3://pyunemrbucket/trino/input/input1.csv
	包名:com.example.social
	事件名称:install
	时间周期:20250701-20250811
    condition:
    """)
    result = process_workflow(user_message)
    #result = test()
    return result

if __name__ == "__main__":
    app.run()
