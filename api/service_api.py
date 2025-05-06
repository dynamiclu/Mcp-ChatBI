import asyncio
from fastapi.responses import StreamingResponse
from fastapi import Body
from server.configuration import Configuration
from server.server import Server
from session.douyin_open_api_session import DouyinOpenApiSession

config = Configuration()
server_config = config.load_config("server/servers_config.json")
servers = [
    Server(name, srv_config)
    for name, srv_config in server_config["mcpServers"].items()
]
chat_session = DouyinOpenApiSession(servers)



async def gen_chat_response(query: str = Body(..., description="用户输入", examples=["请您输入问题"]), session_id: str = Body(..., description="会话ID", examples=["0"]), open_id: str = Body(..., description="用户ID", examples=["0"])):
    if not query or query == "" or not session_id or not open_id:
        return StreamingResponse(content="抱歉，请您输入问题", status_code=200,
                                 media_type="text/markdown; charset=utf-8")
    if session_id == "0":
        await chat_session.init_servers()

    async def event_generator():
        yield "小精灵开始工作了... ![加载中](https://static.fengmiai.com/source_image/loading.gif)"
        try:
            async for chunk in chat_session.start(query=query, session_id=session_id, open_id=open_id):
                await asyncio.sleep(0.01)
                yield chunk
        except asyncio.CancelledError:
            await chat_session.cleanup_servers()
            yield "小精灵工作被取消了..."

    return StreamingResponse(event_generator(), media_type="text/plain; charset=utf-8")
