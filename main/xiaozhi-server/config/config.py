from typing import Dict, Any

# MySQL数据库配置
MYSQL_CONFIG: Dict[str, Any] = {
    'host': '106.52.252.80',
    'port': 3306,
    'user': 'root',
    'password': 'b5bd5cd81fc2ab28',
    'database': 'samewayai',
    'charset': 'utf8mb4',
    
    # 连接池配置
    'pool_name': 'mypool',
    'pool_size': 16,
    'pool_reset_session': True,
    
    # 额外配置
    'use_unicode': True,
    'use_pure': True,  # 使用纯Python实现的MySQL协议
    'autocommit': True,
    'time_zone': '+08:00'
}