from typing import Dict, Any, List
from .client import APIClient

class DeviceConfigAPI:
    """设备配置相关API接口封装"""
    
    def __init__(self, client: APIClient):
        """初始化设备配置API
        
        Args:
            client: API客户端实例
        """
        self.client = client
    
    async def get_device_config(self, device_id: str) -> Dict[str, Any]:
        """获取设备配置信息
        
        Args:
            device_id: 设备ID
            
        Returns:
            Dict[str, Any]: 设备配置信息
        """
        return await self.client.get(f'devices/{device_id}/config')
    
    async def update_device_config(self, device_id: str, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新设备配置
        
        Args:
            device_id: 设备ID
            config_data: 新的配置数据
            
        Returns:
            Dict[str, Any]: 更新结果
        """
        return await self.client.put(f'devices/{device_id}/config', json=config_data)
    
    async def get_config_template(self, device_type: str) -> Dict[str, Any]:
        """获取设备类型对应的配置模板
        
        Args:
            device_type: 设备类型
            
        Returns:
            Dict[str, Any]: 配置模板数据
        """
        return await self.client.get(f'config-templates/{device_type}')
    
    async def get_config_history(self, device_id: str) -> List[Dict[str, Any]]:
        """获取设备配置历史记录
        
        Args:
            device_id: 设备ID
            
        Returns:
            List[Dict[str, Any]]: 配置历史记录列表
        """
        return await self.client.get(f'devices/{device_id}/config/history')
    
    async def restore_config(self, device_id: str, version_id: str) -> Dict[str, Any]:
        """恢复到指定版本的配置
        
        Args:
            device_id: 设备ID
            version_id: 配置版本ID
            
        Returns:
            Dict[str, Any]: 恢复结果
        """
        return await self.client.post(f'devices/{device_id}/config/restore', json={'version_id': version_id})