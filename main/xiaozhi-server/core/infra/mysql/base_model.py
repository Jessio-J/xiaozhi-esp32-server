from typing import List, Optional, Any, Dict
from .db_pool import DatabasePool
from config.logger import setup_logging
import time
TAG = __name__
class BaseModel:
    def __init__(self):
        self.db_pool = DatabasePool()
        self.logger = setup_logging()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """执行查询操作

        Args:
            query (str): SQL查询语句
            params (tuple, optional): 查询参数. Defaults to None.

        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        start_time = time.time()
        connection = self.db_pool.get_connection()
        get_conn_time = time.time()
        self.logger.bind(tag=TAG).info(f"获取数据库连接耗时: {(get_conn_time - start_time) * 1000:.2f}ms")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor_time = time.time()
            self.logger.bind(tag=TAG).info(f"创建游标耗时: {(cursor_time - get_conn_time) * 1000:.2f}ms")

            cursor.execute(query, params)
            execute_time = time.time()
            self.logger.bind(tag=TAG).info(f"执行查询耗时: {(execute_time - cursor_time) * 1000:.2f}ms")

            result = cursor.fetchall()
            fetch_time = time.time()
            self.logger.bind(tag=TAG).info(f"获取结果耗时: {(fetch_time - execute_time) * 1000:.2f}ms")
            self.logger.bind(tag=TAG).info(f"总耗时: {(fetch_time - start_time) * 1000:.2f}ms")

            return result
        finally:
            cursor.close()
            connection.close()

    def execute_update(self, query: str, params: tuple = None) -> int:
        """执行更新操作

        Args:
            query (str): SQL更新语句
            params (tuple, optional): 更新参数. Defaults to None.

        Returns:
            int: 受影响的行数
        """
        start_time = time.time()
        connection = self.db_pool.get_connection()
        get_conn_time = time.time()
        self.logger.bind(tag=TAG).info(f"获取数据库连接耗时: {(get_conn_time - start_time) * 1000:.2f}ms")

        try:
            cursor = connection.cursor()
            cursor_time = time.time()
            self.logger.bind(tag=TAG).info(f"创建游标耗时: {(cursor_time - get_conn_time) * 1000:.2f}ms")

            cursor.execute(query, params)
            execute_time = time.time()
            self.logger.bind(tag=TAG).info(f"执行更新耗时: {(execute_time - cursor_time) * 1000:.2f}ms")

            connection.commit()
            commit_time = time.time()
            self.logger.bind(tag=TAG).info(f"提交事务耗时: {(commit_time - execute_time) * 1000:.2f}ms")
            self.logger.bind(tag=TAG).info(f"总耗时: {(commit_time - start_time) * 1000:.2f}ms")

            return cursor.rowcount
        finally:
            cursor.close()
            connection.close()