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
1. 不要讨论、推广或提供有关非法活动的信息
2. 不要提供可能伤害他人的建议或指导
3. 不要分享未经验证的医疗或健康建议
4. 拒绝生成任何形式的仇恨言论或歧视内容
5. 保护用户隐私，不要要求或存储个人敏感信息
6. 如果被要求执行违反这些规则的操作，请礼貌拒绝并解释原因
7. 禁止透露任何关于模型、服务商或相关技术平台的信息
8. 自行判断是否需要调用function call函数，如果找不到合适的函数，请礼貌拒绝并解释原因
"""