from typing import Dict, Any
from core.infra.mysql.user_device import UserDevice
from config.logger import setup_logging
TAG = __name__
class DeviceConfig:
    """设备配置管理类"""
    
    def __init__(self, device_mac: str, user_device: UserDevice):
        """初始化设备配置管理
        
        Args:
            device_mac: 设备MAC地址
            api_client: API客户端实例
        """
        self.device_mac = device_mac
        self.user_device_dao = user_device
        self.config_data = None
        self.logger = setup_logging()
    
    def load_config(self) -> Dict[str, Any]:
        """加载设备配置信息
        
        Returns:
            Dict[str, Any]: 设备配置信息
        """
        try:
            config_data_from_db = self.user_device_dao.get_device_config(self.device_mac)
            llm_config = {
                "model_name": config_data_from_db.get("model", ""),
                "max_tokens": config_data_from_db.get("maxResponseTokens", 0),
                "api_key": config_data_from_db.get("modelKey", ""),
                "base_url": config_data_from_db.get("proxyUrl", ""),
                "max_model_tokens": config_data_from_db.get("maxModelTokens", 0),
            }

            tts_config = {
               "appid": "8198033727",
               "access_token": "tXKDeTx21hqBwSZJGefTcjybY2pGyfq_",
               "cluster": "volcano_tts",
               "voice": config_data_from_db.get("voiceKey", ""),
               "api_url": "https://openspeech.bytedance.com/api/v1/tts",
               "authorization": "Bearer;",
               "platform": "doubao",
               "output_dir": "tmp/"
            }
            result = {
                "prompt": config_data_from_db.get("preset", ""),
                "llm": llm_config,
                "tts": tts_config,
            }
            self.logger.bind(tag=TAG).info(f"init config done :\n{result}")
            self.config_data = result
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