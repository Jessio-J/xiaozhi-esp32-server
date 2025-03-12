from typing import Dict, Any, List
from .client import APIClient

class UserDeviceAPI:
    """用户设备相关API接口封装"""
    
    def __init__(self, client: APIClient):
        """初始化用户设备API
        
        Args:
            client: API客户端实例
        """
        self.client = client
    
    async def get_device_list(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户的设备列表
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[Dict[str, Any]]: 设备列表数据
        """
        return await self.client.get(f'users/{user_id}/devices')
    
    async def get_device_detail(self, device_id: str) -> Dict[str, Any]:
        """获取设备详细信息
        
        Args:
            device_id: 设备ID
            
        Returns:
            Dict[str, Any]: 设备详细信息
        """
        return await self.client.get(f'devices/{device_id}')
    
    async def bind_device(self, user_id: str, device_data: Dict[str, Any]) -> Dict[str, Any]:
        """绑定新设备
        
        Args:
            user_id: 用户ID
            device_data: 设备绑定数据
            
        Returns:
            Dict[str, Any]: 绑定结果
        """
        return await self.client.post(f'users/{user_id}/devices', json=device_data)
    
    async def unbind_device(self, user_id: str, device_id: str) -> Dict[str, Any]:
        """解绑设备
        
        Args:
            user_id: 用户ID
            device_id: 设备ID
            
        Returns:
            Dict[str, Any]: 解绑结果
        """
        return await self.client.delete(f'users/{user_id}/devices/{device_id}')
    
    async def update_device_name(self, device_id: str, name: str) -> Dict[str, Any]:
        """更新设备名称
        
        Args:
            device_id: 设备ID
            name: 新的设备名称
            
        Returns:
            Dict[str, Any]: 更新结果
        """
        return await self.client.put(f'devices/{device_id}', json={'name': name})
    
    async def register_device(self, device_mac: str) -> Dict[str, Any]:
        """注册设备
        
        Args:
            device_mac: 设备MAC地址
            
        Returns:
            Dict[str, Any]: 注册结果
        """
        return await self.client.post('device/register', json={'deviceMac': device_mac})