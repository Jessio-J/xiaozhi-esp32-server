from typing import List, Optional, Any, Dict
from mysql.connector.cursor import MySQLCursor
from .db_pool import DatabasePool

class BaseModel:
    def __init__(self):
        self.db_pool = DatabasePool()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """执行查询操作

        Args:
            query (str): SQL查询语句
            params (tuple, optional): 查询参数. Defaults to None.

        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        connection = self.db_pool.get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
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
        connection = self.db_pool.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            connection.close()