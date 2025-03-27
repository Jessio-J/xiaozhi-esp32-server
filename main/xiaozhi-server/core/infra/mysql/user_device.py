from typing import List, Optional, Any, Dict
from datetime import datetime
from .base_model import BaseModel

class UserDevice(BaseModel):
    def __init__(self):
        super().__init__()

    def register_device(self, device_id: str, device_config_id: str) -> int:
        query = "INSERT INTO device_bind (device_id, device_config_id) VALUES (%s, %s)"
        return self.execute_update(query, (device_id, device_config_id))

    def create(self, name: str, device_id: str) -> int:
        query = "INSERT INTO devices (name, device_id) VALUES (%s, %s)"
        return self.execute_update(query, (name, device_id))

    def update_status(self, device_id: str, status: str) -> int:
        query = "UPDATE devices SET status = %s, last_online = NOW() WHERE device_id = %s"
        return self.execute_update(query, (status, device_id))

    def get_by_device_id(self, device_id: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM devices WHERE device_id = %s"
        result = self.execute_query(query, (device_id,))
        return result[0] if result else None