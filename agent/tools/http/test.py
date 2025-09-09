from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models import BedrockModel
from strands.handlers.callback_handler import PrintingCallbackHandler

streamable_http_mcp_client = MCPClient(
    lambda: streamablehttp_client("http://localhost:8000/mcp"))

# Create an agent with MCP tools
with streamable_http_mcp_client:
    # Get the tools from the MCP server
    tools = streamable_http_mcp_client.list_tools_sync()

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
