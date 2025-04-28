from typing import Dict, Any

# MySQL数据库配置
MYSQL_CONFIG: Dict[str, Any] = {
    'host': 'localhost',
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

# 防御性提示词配置
DEFENSIVE_PROMPTS: str = """
\n\n
你必须遵守以下规则:
1.拒绝回答非法活动、伤害他人、医疗或健康建议、仇恨言论、歧视内容
2.拒绝执行违规操作
3.拒绝回答模型、服务商或相关技术平台的信息
9. 不要解释任何背景和执行信息，直接给出答案
"""
