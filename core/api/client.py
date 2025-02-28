import aiohttp
from typing import Any, Dict, Optional
from config.settings import load_config
import ssl

class APIClient:
    """基础HTTP客户端类，处理所有API请求"""
    
    def __init__(self):
        config = load_config()
        self.base_url = config['api']['base_url']
        self.verify_ssl = config['api'].get('verify_ssl', True)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _ensure_session(self):
        """确保aiohttp session已创建"""
        if self.session is None:
            if not self.verify_ssl:
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                connector = aiohttp.TCPConnector(ssl=ssl_context)
                self.session = aiohttp.ClientSession(connector=connector)
            else:
                self.session = aiohttp.ClientSession()
    
    async def close(self):
        """关闭HTTP会话"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """发送HTTP请求并处理响应
        
        Args:
            method: HTTP方法
            path: API路径
            **kwargs: 请求参数
        
        Returns:
            Dict[str, Any]: API响应数据
        
        Raises:
            aiohttp.ClientError: 当HTTP请求失败时
        """
        await self._ensure_session()
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        
        async with self.session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get(self, path: str, **kwargs) -> Dict[str, Any]:
        """发送GET请求"""
        return await self._request('GET', path, **kwargs)
    
    async def post(self, path: str, **kwargs) -> Dict[str, Any]:
        """发送POST请求"""
        return await self._request('POST', path, **kwargs)
    
    async def put(self, path: str, **kwargs) -> Dict[str, Any]:
        """发送PUT请求"""
        return await self._request('PUT', path, **kwargs)
    
    async def delete(self, path: str, **kwargs) -> Dict[str, Any]:
        """发送DELETE请求"""
        return await self._request('DELETE', path, **kwargs)