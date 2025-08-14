from agent.gaid_agent import GaidAgent
from agent.core_agent import CoreAgent
from agent.sql_agent import SqlAgent
from config.trino_config import TRINO_CONFIG

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
    response = sql_agent.run(user_input+"['BB42A58C-4E51-13C3-1088-58A4754781DC', 'AC71B613-4E24-AEA1-DF25-6E5B5CA684AB']")
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
def main():
    test4()

if __name__ == "__main__":
    main()