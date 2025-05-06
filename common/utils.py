
import json
import pydantic
import asyncio
from pydantic import BaseModel
from typing import List

def is_valid_json(llm_response: str) -> bool:
    """判断字符串是否为有效的 JSON 结构。

    Args:
        llm_response: 要判断的字符串。

    Returns:
        如果字符串是有效的 JSON 结构，返回 True；否则返回 False。
    """
    try:
        json.loads(llm_response.strip())
        return True
    except json.JSONDecodeError as e:
        # logger.error(f"Invalid JSON: {e}")
        return False

def run_async(cor):
    '''
    在同步环境中运行异步代码.
    '''
    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
    return loop.run_until_complete(cor)

def iter_over_async(ait, loop):
    '''
    将异步生成器封装成同步生成器.
    '''
    ait = ait.__aiter__()
    async def get_next():
        try:
            obj = await ait.__anext__()
            return False, obj
        except StopAsyncIteration:
            return True, None
    while True:
        done, obj = loop.run_until_complete(get_next())
        if done:
            break
        yield obj

class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="HTTP status code")
    msg: str = pydantic.Field("success", description="HTTP status message")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
            }
        }


class ListResponse(BaseResponse):
    data: List[str] = pydantic.Field(..., description="List of names")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": ["", "", ""],
            }
        }