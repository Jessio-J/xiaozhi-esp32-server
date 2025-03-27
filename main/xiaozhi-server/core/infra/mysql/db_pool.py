from typing import Any
import mysql.connector
from mysql.connector import pooling
from config.config import MYSQL_CONFIG

class DatabasePool:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._pool = mysql.connector.pooling.MySQLConnectionPool(**MYSQL_CONFIG)
        return cls._instance

    @classmethod
    def get_connection(cls):
        """获取数据库连接

        Returns:
            MySQLConnection: 数据库连接对象
        """
        return cls._pool.get_connection()