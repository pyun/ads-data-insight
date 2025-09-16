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
from strands_tools import file_read, file_write, shell, use_aws, python_repl,editor
from strands.handlers.callback_handler import PrintingCallbackHandler
import boto3
import json

def test():
    trino_mcp = TrinoTools(TRINO_CONFIG)
    agent = Agent(
        model=preAgentConfig.get("model"),
        tools=trino_mcp.list_tools(),
        callback_handler=PrintingCallbackHandler()
    )
    print(agent.tool_names)
    result = agent("帮我列出trino中的所有表")
    print(f"\n-----result----{result}\n")

def agentCoreTest():
    client = boto3.client('bedrock-agentcore', region_name='us-east-1')
    payload = json.dumps({
        "prompt": "gaid：s3://pyunemrbucket/trino/input/input1.csv 包名:com.example.social 事件名称:install 时间周期:20250701-20250811 condition:"}
    )

    response = client.invoke_agent_runtime(
        agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:297126936078:runtime/ads_insight_agent-ho7JgH4kuU',
        payload=payload,
        qualifier="DEFAULT" # Optional
    )
    response_body = response['response'].read()
    response_data = json.loads(response_body)
    print("Agent Response:", response_data)

if __name__ == "__main__":
    agentCoreTest()
    #localTest()