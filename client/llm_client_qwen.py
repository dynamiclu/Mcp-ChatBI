import dashscope
from dashscope.api_entities.dashscope_response import GenerationResponse

from config import config

_max_retries = 5


def _generate_response_stream(messages: [dict]) -> str:
    api_key = config.app.get("qwen_api_key")
    model_name = config.app.get("qwen_model_name")
    dashscope.api_key = api_key
    response_stream = dashscope.Generation.call(
        model=model_name, messages=messages, stream=True
    )
    if response_stream:
        try:
            # 初始化一个变量用于存储完整的生成内容
            full_content = ""
            # 遍历流式响应
            for chunk in response_stream:
                if isinstance(chunk, GenerationResponse):
                    status_code = chunk.status_code
                    if status_code != 200:
                        raise Exception(
                            f' returned an error response: "{chunk}"'
                        )

                    # 获取当前 chunk 的内容
                    if "output" in chunk and "text" in chunk["output"]:
                        content_chunk = chunk["output"]["text"]
                        full_content += content_chunk

                        # 实时输出当前 chunk 的内容（可以根据需求调整）
                        # print(content_chunk, end="", flush=True)
                        yield content_chunk

                    else:
                        raise Exception(
                            f' returned an invalid chunk: "{chunk}"'
                        )
                else:
                    raise Exception(
                        f' returned an invalid response type: "{chunk}"'
                    )
            # 返回完整的生成内容
            # return full_content
        except Exception as e:
            raise Exception(f"Error during streaming: {e}")
    else:
        raise Exception(f" returned an empty response")


def _generate_response(messages: [dict]) -> str:
    content = ""
    api_key = config.app.get("qwen_api_key")
    model_name = config.app.get("qwen_model_name")
    dashscope.api_key = api_key
    response = dashscope.Generation.call(
        model=model_name, messages=messages
    )
    if response:
        if isinstance(response, GenerationResponse):
            status_code = response.status_code
            if status_code != 200:
                raise Exception(
                    f'returned an error response: "{response}"'
                )
            content = response["output"]["text"]
            return content
        else:
            raise Exception(
                f'returned an invalid response: "{response}"'
            )
    else:
        raise Exception(f" returned an empty response")


