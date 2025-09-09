from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.handlers.callback_handler import PrintingCallbackHandler
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel
from server import TrinoTools

trino_mcp = TrinoTools({
    "host": "172.31.38.156",
    "port": "8889",
    "user": "hadoop"
})

print("------------testing-------------")
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-east-1"
)

agent = Agent(
    model=model,
    tools=trino_mcp.list_tools(),
    callback_handler=PrintingCallbackHandler()
)
print(f"------tools-------\n{agent.tool_names}")
response = agent("帮我列出有哪些表")

