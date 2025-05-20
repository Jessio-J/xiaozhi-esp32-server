import time
import os
import uuid
import io
import wave
from typing import Optional, Tuple, List
import asyncio
import dashscope
from gummy import *

from core.providers.asr.base import ASRProviderBase
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()

class ASRProvider(ASRProviderBase):
    def __init__(self, config: dict, delete_audio_file: bool):
        """初始化Gummy ASR提供者"""
        self.api_key = config.get("api_key", "")
        self.output_dir = config.get("output_dir", "tmp/")
        self.model = config.get("model", "gummy-chat-v1")
        self.format = config.get("format", "pcm")
        self.sample_rate = config.get("sample_rate", 16000)
        self.transcription_enabled = config.get("transcription_enabled", True)
        self.translation_enabled = config.get("translation_enabled", False)
        self.translation_target_languages = config.get("translation_target_languages", ["en"])
        
        # 设置DashScope API Key
        if self.api_key:
            dashscope.api_key = self.api_key
            
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.delete_audio_file = delete_audio_file
        
    def save_audio_to_file(self, opus_data: List[bytes], session_id: str) -> str:
        """将Opus音频数据解码并保存为WAV文件"""
        file_name = f"asr_{session_id}_{uuid.uuid4()}.wav"
        file_path = os.path.join(self.output_dir, file_name)

        # 使用与doubao相同的方法解码opus数据
        pcm_data = self.decode_opus(opus_data, session_id)

        with wave.open(file_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 2 bytes = 16-bit
            wf.setframerate(16000)
            wf.writeframes(b"".join(pcm_data))

        return file_path
        
    @staticmethod
    def decode_opus(opus_data: List[bytes], session_id: str) -> List[bytes]:
        """将Opus音频数据解码为PCM数据"""
        import opuslib_next
        
        decoder = opuslib_next.Decoder(16000, 1)  # 16kHz, 单声道
        pcm_data = []

        for opus_packet in opus_data:
            try:
                pcm_frame = decoder.decode(opus_packet, 960)  # 960 samples = 60ms
                pcm_data.append(pcm_frame)
            except opuslib_next.OpusError as e:
                logger.bind(tag=TAG).error(f"Opus解码错误: {e}", exc_info=True)

        return pcm_data
    
    async def speech_to_text(self, opus_data: List[bytes], session_id: str) -> Tuple[Optional[str], Optional[str]]:
        """将语音数据转换为文本"""
        try:
            # 合并所有opus数据包并解码
            pcm_data = self.decode_opus(opus_data, session_id)
            combined_pcm_data = b''.join(pcm_data)
            
            # 使用Future来处理回调结果
            transcription_result_future = asyncio.Future()
            translation_result_future = asyncio.Future()
            
            class GummyCallback(TranslationRecognizerCallback):
                def __init__(self, trans_future, transcr_future):
                    self.translation_future = trans_future
                    self.transcription_future = transcr_future
                    self.transcription_text = ""
                    self.translation_text = ""
                
                def on_open(self) -> None:
                    logger.bind(tag=TAG).debug("Gummy ASR连接已打开")
                
                def on_close(self) -> None:
                    logger.bind(tag=TAG).debug("Gummy ASR连接已关闭")
                    # 如果结果尚未被设置，则设置最终结果
                    if not self.transcription_future.done():
                        self.transcription_future.set_result(self.transcription_text)
                    if not self.translation_future.done():
                        self.translation_future.set_result(self.translation_text)
                
                def on_event(
                    self,
                    request_id,
                    transcription_result: TranscriptionResult,
                    translation_result: TranslationResult,
                    usage,
                ) -> None:
                    if transcription_result is not None:
                        self.transcription_text = transcription_result.text
                        logger.bind(tag=TAG).debug(f"识别结果: {self.transcription_text}")
                    
                    if translation_result is not None and len(translation_result.get_language_list()) > 0:
                        lang = translation_result.get_language_list()[0]
                        translation = translation_result.get_translation(lang)
                        if translation:
                            self.translation_text = translation.text
                            logger.bind(tag=TAG).debug(f"翻译结果 ({lang}): {self.translation_text}")
            
            callback = GummyCallback(translation_result_future, transcription_result_future)
            
            # 创建识别器
            start_time = time.time()
            translator = TranslationRecognizerChat(
                model=self.model,
                format=self.format,
                sample_rate=self.sample_rate,
                transcription_enabled=self.transcription_enabled,
                translation_enabled=self.translation_enabled,
                translation_target_languages=self.translation_target_languages,
                callback=callback,
            )
            
            # 开始识别
            translator.start()
            
            # 发送音频数据
            chunk_size = 3200  # 每个音频帧的大小(200ms at 16kHz)
            for i in range(0, len(combined_pcm_data), chunk_size):
                chunk = combined_pcm_data[i:i+chunk_size]
                if not translator.send_audio_frame(chunk):
                    logger.bind(tag=TAG).debug("句子结束，停止发送")
                    break
                await asyncio.sleep(0.01)  # 小暂停允许处理
            
            # 停止识别
            translator.stop()
            
            # 等待结果
            try:
                transcription = await asyncio.wait_for(transcription_result_future, timeout=10)
                translation = await asyncio.wait_for(translation_result_future, timeout=1)
                
                processing_time = time.time() - start_time
                logger.bind(tag=TAG).info(f"Gummy ASR处理耗时: {processing_time:.2f}秒")
                
                return transcription, translation
                
            except asyncio.TimeoutError:
                logger.bind(tag=TAG).error("Gummy ASR等待结果超时")
                return "", None
            
        except Exception as e:
            logger.bind(tag=TAG).error(f"Gummy ASR处理失败: {e}", exc_info=True)
            return "", None
