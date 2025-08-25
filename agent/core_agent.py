import csv
import logging
import os
from datetime import datetime
from typing import Optional

import trino
from agent.gaid_agent import GaidAgent
from agent.sql_agent import SqlAgent
from config.logger_config import setup_logger
from config.config import TRINO_CONFIG
from config.config import SYSTEM_SQL_PROMPT

setup_logger()
logger = logging.getLogger(__name__)


class CoreAgent:
    """核心代理类，协调GAID代理和SQL代理完成数据分析工作流"""

    def __init__(self, gaid_agent: Optional[GaidAgent] = None, sql_agent: Optional[SqlAgent] = None):
        """初始化核心代理
        
        Args:
            gaid_agent: GAID处理代理实例，如果为None则创建新实例
            sql_agent: SQL处理代理实例，如果为None则创建新实例
        """
        logger.info("初始化CoreAgent")

        try:
            self.gaid_agent = gaid_agent if gaid_agent is not None else GaidAgent()
            self.sql_agent = sql_agent if sql_agent is not None else SqlAgent(SYSTEM_SQL_PROMPT)  # 优先从配置中读取提示词
            logger.info("CoreAgent初始化成功")
        except Exception as e:
            logger.error(f"CoreAgent初始化失败: {e}")
            raise

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
            # 步骤1: 生成GAID条件
            logger.debug("步骤1: 开始生成GAID条件")
            condition_results = self.gaid_agent.run(user_input)
            logger.info(f"GAID条件生成完成: {str(condition_results)[:200]}...")  # 限制日志长度

            # 步骤2: 生成SQL语句
            logger.debug("步骤2: 开始生成SQL语句")
            combined_input = f"{user_input};condition:{condition_results}"
            sql_results = self.sql_agent.run(combined_input)

            # 提取SQL语句
            if "--sql--" in str(sql_results):
                sql_results = str(sql_results).split("--sql--")[1].strip()
                logger.info("SQL语句提取成功")
            else:
                logger.warning("未找到--sql--标记，返回原始结果")

            logger.info(f"工作流处理完成，SQL结果: {sql_results}")
            return str(sql_results)

        except Exception as e:
            error_msg = f"工作流处理失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return f"错误：{error_msg}"

    def execute_sql(self, sql: str) -> str:
        """执行SQL语句并返回结果"""
        if not sql or not sql.strip():
            return "错误：SQL语句不能为空"
        if not sql.startswith("SELECT"):
            return "错误：SQL语句必须以SELECT开头"

        conn = None
        cursor = None
        try:
            logger.info("开始连接Trino数据库")

            conn = trino.dbapi.connect(
                host=TRINO_CONFIG['TRINO_HOST'],
                port=int(TRINO_CONFIG['TRINO_PORT']),
                user=TRINO_CONFIG['TRINO_USER'],
                catalog='hive',
                schema='default'
            )

            cursor = conn.cursor()
            logger.debug(f"执行SQL: {sql}")

            cursor.execute(sql)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            # 保存为CSV文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = f"output/query_result_{timestamp}.csv"

            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(columns)  # 写入列名
                writer.writerows(results)  # 写入数据

            logger.info(f"SQL执行完成，结果已保存到: {csv_filename}")

            return os.path.abspath(csv_filename)

        except Exception as e:
            error_msg = f"SQL执行失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return f"错误：{error_msg}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def run(self, user_input) -> str:
        sql = self.process_workflow(user_input)
        return self.execute_sql(sql)
