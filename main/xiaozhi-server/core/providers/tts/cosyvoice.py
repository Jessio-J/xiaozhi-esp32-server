import os
import uuid
import requests
from config.logger import setup_logging
from datetime import datetime
from core.providers.tts.base import TTSProviderBase
import dashscope
from dashscope.audio.tts_v2 import *
TAG = __name__
logger = setup_logging()

class TTSProvider(TTSProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file=False)
        dashscope.api_key = "sk-8726c8fae0864f679c56cf6c5a845cb5"
        # 模型
        self.model = "cosyvoice-v2"
        # 音色
        self.voice = "longxiaochun_v2"
        # 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
        self.synthesizer = SpeechSynthesizer(model=self.model, voice=self.voice, format=AudioFormat.WAV_16000HZ_MONO_16BIT)
        self.format = config.get("format", "wav")
        self.output_file = config.get("output_dir", "tmp/")

    def generate_filename(self):
        return os.path.join(self.output_file, f"tts-cosyvoice-{datetime.now().date()}@{uuid.uuid4().hex}.{self.format}")

    async def text_to_speak(self, text, output_file):
        # 发送待合成文本，获取二进制音频
        self.logger.bind(tag=TAG).error(f"cosyvoice尝试生成text: {text}")
        audio = self.synthesizer.call(text)
        logger.bind(tag=TAG).error(f"[cosyvoice] requestId: {self.synthesizer.get_last_request_id()}, first package delay ms: {self.synthesizer.get_first_package_delay()}")

        if audio:
            with open(output_file, "wb") as file:
                file.write(audio)
        else:
            logger.bind(tag=TAG).error(f"cosyvoice请求失败: {self.synthesizer.get_response}")
