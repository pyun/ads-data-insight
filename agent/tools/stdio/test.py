from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.handlers.callback_handler import PrintingCallbackHandler
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel

params = StdioServerParameters(
    command="python",
    args=["server.py"],
    env={
        "TRINO_HOST": "172.31.38.156",
        "TRINO_PORT": "8889",
        "TRINO_USER": "hadoop"
    }
)
# Create an MCP client with stdio transport
server = MCPClient(lambda: stdio_client(params))
# Start the server
print(f"------Connecting to server------")
server.start()
print(f"------Connected to server------")

tools = server.list_tools_sync()

print("------------testing-------------")
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-east-1"
)
agent = Agent(
    model=model,
    tools=tools,
    callback_handler=PrintingCallbackHandler()
)
print(f"------tools-------\n{agent.tool_names}")
response = agent("帮我列出有哪些表")
server.stop(None, None, None)
