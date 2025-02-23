from typing import Dict, Any, List
from core.api.client import APIClient
from core.api.device_config import DeviceConfigAPI
from core.api.user_device import UserDeviceAPI
import asyncio

async def main():
    # 创建API客户端实例
    client = APIClient()
    
    try:
        # 创建设备配置API和用户设备API实例
        device_config_api = DeviceConfigAPI(client)
        user_device_api = UserDeviceAPI(client)
        
        # 示例：获取用户的设备列表
        user_id = "user123"
        devices = await user_device_api.get_device_list(user_id)
        print(f"用户设备列表: {devices}")
        
        # 示例：获取特定设备的配置信息
        if devices:
            device_id = devices[0]['id']  # 使用第一个设备作为示例
            
            # 获取设备配置
            config = await device_config_api.get_device_config(device_id)
            print(f"设备配置: {config}")
            
            # 更新设备配置
            new_config = {
                "volume": 80,
                "brightness": 100,
                "auto_update": True
            }
            update_result = await device_config_api.update_device_config(device_id, new_config)
            print(f"配置更新结果: {update_result}")
            
            # 获取配置历史记录
            config_history = await device_config_api.get_config_history(device_id)
            print(f"配置历史记录: {config_history}")
            
            # 示例：更新设备名称
            new_name = "客厅智能音箱"
            name_update_result = await user_device_api.update_device_name(device_id, new_name)
            print(f"设备名称更新结果: {name_update_result}")
    
    except Exception as e:
        print(f"发生错误: {str(e)}")
    
    finally:
        # 确保关闭客户端连接
        await client.close()

# 运行示例
if __name__ == "__main__":
    asyncio.run(main())