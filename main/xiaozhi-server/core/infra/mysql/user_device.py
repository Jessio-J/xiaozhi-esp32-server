from typing import List, Optional, Any, Dict
from datetime import datetime
from .base_model import BaseModel
from config.logger import setup_logging
TAG = __name__
class UserDevice(BaseModel):
    def __init__(self):
        super().__init__()
        self.logger = setup_logging()

    def register_device(self, device_id: str, device_config_id: str) -> int:
        """
        注册设备
        :param device_id: 设备ID
        :param device_config_id: 设备配置ID
        :return: 设备ID
        """
        query = "SELECT * FROM device_bind WHERE deviceMac = %s"
        result = self.execute_query(query, (device_id,))
        if result:
            self.logger.bind(tag=TAG).info(f"设备已存在：{result}")
            return 1  # 设备已存在，返回1
        device_name = f"同途硬件设备-{device_id[-5:]}"
        update = "INSERT INTO device_bind (deviceMac, deviceConfigId, userId, deviceName) VALUES (%s, %s, 9, %s)"
        return self.execute_update(update, (device_id, device_config_id,device_name))

    def get_device_config(self, device_id: str,device_config_id: str) -> Optional[Dict[str, Any]]:
        """
        获取设备配置
        :param device_id: 设备ID
        :return: 设备配置信息
        """
        if device_config_id:
            query = """
                   select f.configName,f.voiceKey,f.voicePlatform,f.voiceModel,f.appName,f.preset,m.model,m.proxyUrl,m.key modelKey,m.maxModelTokens,m.maxResponseTokens,f.asrType from
    (select vv.deviceMac,vv.configName,vv.relatedAppId,vv.voice_id,vv.platform voicePlatform,vv.voice_source voiceModel,vv.voice_id voiceKey, a.name appName, a.preset,vv.modelId,vv.asrType
     from ( select d.*,v.platform,v.voice_source,v.voice_id from
                                                (select b.deviceMac, c.configName,c.relatedAppId,c.voiceId,c.modelId,c.asrType from device_bind b
                     join device_config c on  c.id = %s and b.deviceMac = %s) d join voice v on d.voiceId = v.id) vv
              left join app a on vv.relatedAppId = a.id) f
        left join models m on f.modelId = m.id;
                    """
            self.logger.bind(tag=TAG).info(f"查询设备配置: {query}, {device_config_id}, {device_id}")
            result = self.execute_query(query, (device_config_id,device_id))
        else:
            query = """
                select f.id,f.configName,f.voiceType,f.voiceKey,f.appName,f.preset,f.voicePlatform,m.model,m.proxyUrl,m.key modelKey,m.maxModelTokens,m.maxResponseTokens from
                (select d.*, a.name appName, a.preset
                from (select b.deviceMac, c.* from device_bind b
                    left join device_config c on b.deviceConfigId = c.id where deviceMac = %s) d
                left join app a on d.relatedAppId = a.id) f
                left join models m on f.modelId = m.id;
            """
            self.logger.bind(tag=TAG).info(f"查询设备配置: {query}, {device_id}")
            result = self.execute_query(query, (device_id,))
        if result:
            return result[0]
        return None