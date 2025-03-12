from typing import Dict, Any
from core.api.device_config import DeviceConfigAPI
from core.api.client import APIClient

class DeviceConfig:
    """设备配置管理类"""
    
    def __init__(self, device_mac: str, api_client: APIClient):
        """初始化设备配置管理
        
        Args:
            device_mac: 设备MAC地址
            api_client: API客户端实例
        """
        self.device_mac = device_mac
        self.device_config_api = DeviceConfigAPI(api_client)
        self.config_data = None
    
    async def load_config(self) -> Dict[str, Any]:
        """加载设备配置信息
        
        Returns:
            Dict[str, Any]: 设备配置信息
        """
        try:
            self.config_data = await self.device_config_api.get_device_config_by_mac(self.device_mac)
            return self.config_data
        except Exception as e:
            raise Exception(f"加载设备配置失败: {str(e)}")
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前设备配置
        
        Returns:
            Dict[str, Any]: 设备配置信息
        """
        return self.config_data or {}
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """获取指定配置项的值
        
        Args:
            key: 配置项键名
            default: 默认值
            
        Returns:
            Any: 配置项的值
        """
        return self.config_data.get(key, default) if self.config_data else default