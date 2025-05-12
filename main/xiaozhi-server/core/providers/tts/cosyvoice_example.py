# coding=utf-8

import dashscope
from dashscope.audio.tts_v2 import *
import asyncio
import concurrent.futures
def main():
    # 若没有将API Key配置到环境变量中，需将your-api-key替换为自己的API Key
    dashscope.api_key = "sk-8726c8fae0864f679c56cf6c5a845cb5"

    # 模型
    model = "cosyvoice-v2"
    # 音色
    voice = "longxiaochun_v2"

    # 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
    synthesizer = SpeechSynthesizer(model=model, voice=voice,format=AudioFormat.WAV_16000HZ_MONO_16BIT)
    # 发送待合成文本，获取二进制音频

    
    async def synthesize_text():
        text = "你好不好啊啊啊啊，在干什么啊？"
        audio_result = synthesizer.call(text)
        print('[Metric] requestId: {}, first package delay ms: {}'.format(
            synthesizer.get_last_request_id(),
            synthesizer.get_first_package_delay()))
        return audio_result
    
    # 创建异步任务并执行10遍
    loop = asyncio.get_event_loop()
    tasks = [synthesize_text() for _ in range(10)]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    
    # 保存所有合成的音频文件
    for i, audio in enumerate(results):
        # 为每个音频文件生成唯一的文件名
        filename = f'output_{i+1}.wav'
        # 将音频保存至本地
        with open(filename, 'wb') as f:
            f.write(audio)
        print(f'已保存音频文件: {filename}')


if __name__ == "__main__":
    main()