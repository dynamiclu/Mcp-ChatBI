from config.config import API_URL
import httpx

def set_httpx_timeout(timeout=60.0):
    httpx._config.DEFAULT_TIMEOUT_CONFIG.connect = timeout
    httpx._config.DEFAULT_TIMEOUT_CONFIG.read = timeout
    httpx._config.DEFAULT_TIMEOUT_CONFIG.write = timeout

set_httpx_timeout()

class ApiRequest:
    def __init__(
            self,
            base_url: str = API_URL,
            timeout: float = 120.0,
            no_remote_api: bool = False,  # call api view function directly
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.no_remote_api = no_remote_api

    def _parse_url(self, url: str) -> str:
        if not url.startswith("http") and self.base_url:
            part1 = self.base_url.strip(" /")
            part2 = url.strip(" /")
            return f"{part1}/{part2}"
        else:
            return url


    async def data_assistant_chat(
            self,
            query: str,
            session_id: str = None,
            open_id: str = ""
    ):
        data = {
            "query": query,
            "session_id": session_id,
            "open_id": open_id
        }
        url = self._parse_url("/api/data/assistant/chat")
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, json=data) as response:
                async for chunk in response.aiter_bytes(None):
                    chunk_text = chunk.decode('utf-8')
                    yield chunk_text



