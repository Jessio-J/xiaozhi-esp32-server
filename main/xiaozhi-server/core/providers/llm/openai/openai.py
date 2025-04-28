import openai
from config.logger import setup_logging
from core.utils.util import check_model_key
from core.providers.llm.base import LLMProviderBase
from threading import Lock

TAG = __name__
logger = setup_logging()


class LLMProvider(LLMProviderBase):
    def __init__(self,config):
        self.client_map = {}

    def _get_or_create_client(self, config):
        model_name = config.get("model_name")
        if model_name not in self.client_map:
            api_key = config.get("api_key")
            base_url = config.get("base_url")
            # if base_url:
            #     base_url = f"{base_url.rstrip('/')}/v1/"
            check_model_key("LLM", api_key)
            self.client_map[model_name] = openai.OpenAI(api_key=api_key, base_url=base_url)
        return self.client_map[model_name]

    def response(self, session_id, dialogue, config = None):
        
        try:
            logger.bind(tag=TAG).info(f"response: ",dialogue)
            client = self._get_or_create_client(config)
            max_tokens = config.get("max_tokens", 500)
            responses = client.chat.completions.create(
                model=config.get("model_name"),
                messages=dialogue,
                stream=True,
                max_tokens=max_tokens,
            )

            is_active = True
            for chunk in responses:
                try:
                    # 检查是否存在有效的choice且content不为空
                    delta = chunk.choices[0].delta if getattr(chunk, 'choices', None) else None
                    content = delta.content if hasattr(delta, 'content') else ''
                except IndexError:
                    content = ''
                if content:
                    # 处理标签跨多个chunk的情况
                    if '<think>' in content:
                        is_active = False
                        content = content.split('<think>')[0]
                    if '</think>' in content:
                        is_active = True
                        content = content.split('</think>')[-1]
                    if is_active:
                        yield content

        except Exception as e:
            logger.bind(tag=TAG).error(f"Error in response generation: {e}")

    def response_with_functions(self, session_id, dialogue, functions=None,config=None):
       
        try:
            logger.bind(tag=TAG).info(f"response_with_functions: {dialogue}")
            logger.bind(tag=TAG).info(f"functions: {functions}")
            client = self._get_or_create_client(config)
            stream = client.chat.completions.create(
                model=config.get("model_name"),
                messages=dialogue,
                stream=True,
                tools=functions
            )

            for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    logger.bind(tag=TAG).error(f"chunk.choices: {chunk.choices}")
                    yield chunk.choices[0].delta.content, chunk.choices[0].delta.tool_calls

        except Exception as e:
            logger.bind(tag=TAG).error(f"Error in function call streaming: {e}")
            yield {"type": "content", "content": f"【OpenAI服务响应异常: {e}】"}
