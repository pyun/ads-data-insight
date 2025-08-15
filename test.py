import json

from mcp import StdioServerParameters, stdio_client
from agent.gaid_agent import GaidAgent
from agent.core_agent import CoreAgent
from agent.sql_agent import SqlAgent
from config.config import TRINO_CONFIG
from strands import Agent
from config.config import model
from handler.handler import AgentHandler
from strands.tools.mcp import MCPClient

user_input = """
            1. gaid：/data/genai/ads-data-insight/data/input.csv
            2. 包名:com.example.social
            3. 事件名称:install
            4. 时间周期:20250701-20250811
            5. condition: 
        """


def test1():
    gaid_agent = GaidAgent()
    response = gaid_agent.run(user_input)
    print("\n---------result----------\n")
    print(response)


def test2():
    sql_agent = SqlAgent()
    response = sql_agent.run(
        user_input+"['BB42A58C-4E51-13C3-1088-58A4754781DC', 'AC71B613-4E24-AEA1-DF25-6E5B5CA684AB']")
    print("\n---------result----------\n")
    print(response)


def test3():
    core_agent = CoreAgent()
    response = core_agent.process_workflow(user_input)
    print("\n---------result----------\n")
    print(response)


def test4():
    core_agent = CoreAgent()
    response = core_agent.execute_sql("select * from hive.default.t_event")
    print("\n---------result----------\n")
    print(response)


def test5():
    params = StdioServerParameters(
        command="python",
        # args=["/data/mcp-trino-python/src/server_stdio.py"],
                args=["/data/genai/ads-data-insight/trino-mcp/server.py"],
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
    print(f"------listing tools------")
    tools = server.list_tools_sync()
    print(f"------tools-------\n{tools}")

    print("------------testing-------------")
    agent = Agent(
        model=model,
        tools=tools,
        callback_handler=AgentHandler()
    )
    response = agent("帮我列出有哪些表")
    server.stop(None, None, None)


def main():
    test5()


if __name__ == "__main__":
    main()
