import asyncio
import os
from typing import Any, Literal, cast
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from contextlib import AsyncExitStack

from common.log import logger
from common.tool import Tool

DEFAULT_ENCODING = "utf-8"
DEFAULT_ENCODING_ERROR_HANDLER = "strict"
DEFAULT_HTTP_TIMEOUT = 5
DEFAULT_SSE_READ_TIMEOUT = 60 * 5


class Server:
    """Manages MCP server connections and tool execution."""

    def __init__(self, name: str, config: dict[str, Any]) -> None:
        self.name: str = name
        self.config: dict[str, Any] = config
        self.stdio_context: Any | None = None
        self.session: ClientSession | None = None
        self._cleanup_lock: asyncio.Lock = asyncio.Lock()
        self.exit_stack: AsyncExitStack = AsyncExitStack()

    # async def initialize(self) -> None:
    #     """Initialize the server connection."""
    #     command = (
    #         shutil.which("python")
    #         if self.config["command"] == "python"
    #         else self.config["command"]
    #     )
    #     if command is None:
    #         raise ValueError("The command must be a valid string and cannot be None.")
    #
    #     server_params = StdioServerParameters(
    #         command=command,
    #         args=self.config["args"],
    #         env={**os.environ, **self.config["env"]}
    #         if self.config.get("env")
    #         else None,
    #     )
    #     try:
    #         stdio_transport = await self.exit_stack.enter_async_context(
    #             stdio_client(server_params)
    #         )
    #         read, write = stdio_transport
    #         session = await self.exit_stack.enter_async_context(
    #             ClientSession(read, write)
    #         )
    #         await session.initialize()
    #         self.session = session
    #     except Exception as e:
    #         logger.error(f"Error initializing server {self.name}: {e}")
    #         await self.cleanup()
    #         raise

    async def initialize(self) -> None:
        transport = self.config.get("transport", "stdio")
        if transport == "sse":
            await self.connect_to_server_via_sse(
                url=self.config["url"],
                headers=self.config["headers"],
                timeout=self.config.get("timeout", DEFAULT_HTTP_TIMEOUT),
                sse_read_timeout=self.config.get("sse_read_timeout", DEFAULT_SSE_READ_TIMEOUT),
            )
        elif transport == "stdio":
            await self.connect_to_server_via_stdio(
                command=self.config["command"],
                args=self.config["args"],
                env={**os.environ, **self.config["env"]}
                if self.config.get("env")
                else None,
                encoding=DEFAULT_ENCODING,
            )
        else:
            raise ValueError(f"Unsupported transport: {transport}. Must be 'stdio' or 'sse'")

    async def connect_to_server_via_stdio(
            self,
            *,
            command: str,
            args: list[str],
            env: dict[str, str] | None = None,
            encoding: str = DEFAULT_ENCODING,
            encoding_error_handler: Literal[
                "strict", "ignore", "replace"
            ] = DEFAULT_ENCODING_ERROR_HANDLER,
    ) -> None:
        """
        通过标准输入输出连接到服务器。

        Args:
            server_name (str): 服务器名称。
            command (str): 要执行的命令。
            args (list[str]): 命令参数列表。
            env (dict[str, str] | None): 环境变量，默认为 None。
            encoding (str): 编码方式，默认为 DEFAULT_ENCODING。
            encoding_error_handler (Literal["strict", "ignore", "replace"]): 编码错误处理方式，默认为 DEFAULT_ENCODING_ERROR_HANDLER。

        Returns:
            None

        """
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env,
            encoding=encoding,
            encoding_error_handler=encoding_error_handler,
        )

        # Create and store the connection
        try:
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            read, write = stdio_transport
            session = cast(
                ClientSession,
                await self.exit_stack.enter_async_context(ClientSession(read, write)),
            )
            await session.initialize()
            self.session = session

        except Exception as e:
            logger.error(f"Error initializing server {self.name}: {e}")
            await self.cleanup()
            raise

    async def connect_to_server_via_sse(
            self,
            *,
            url: str,
            headers: dict[str, Any] | None = None,
            timeout: float = DEFAULT_HTTP_TIMEOUT,
            sse_read_timeout: float = DEFAULT_SSE_READ_TIMEOUT,
    ) -> None:
        """
        通过SSE连接到服务器。
        Args:
            server_name (str): 服务器名称。
            url (str): SSE服务器的URL。
            headers (dict[str, Any] | None): 请求头，默认为None。
            timeout (float): HTTP请求超时时间，默认为DEFAULT_HTTP_TIMEOUT。
            sse_read_timeout (float): SSE读取超时时间，默认为DEFAULT_SSE_READ_TIMEOUT。
        Returns:
            None
        """
        try:
            sse_transport = await self.exit_stack.enter_async_context(
                sse_client(url, headers, timeout, sse_read_timeout)
            )
            read, write = sse_transport
            session = cast(
                ClientSession,
                await self.exit_stack.enter_async_context(ClientSession(read, write)),
            )
            await session.initialize()
            self.session = session

        except Exception as e:
            logger.error(f"Error initializing server {self.name}: {e}")
            await self.cleanup()
            raise

    async def list_tools(self) -> list[Any]:
        """List available tools from the server.

        Returns:
            A list of available tools.

        Raises:
            RuntimeError: If the server is not initialized.
        """
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        tools_response = await self.session.list_tools()
        tools = []

        for item in tools_response:
            if isinstance(item, tuple) and item[0] == "tools":
                for tool in item[1]:
                    tools.append(Tool(tool.name, tool.description, tool.inputSchema))

        return tools

    async def execute_tool(
            self,
            tool_name: str,
            arguments: dict[str, Any],
            retries: int = 2,
            delay: float = 1.0,
    ) -> Any:
        """Execute a tool with retry mechanism.

        Args:
            tool_name: Name of the tool to execute.
            arguments: Tool arguments.
            retries: Number of retry attempts.
            delay: Delay between retries in seconds.

        Returns:
            Tool execution result.

        Raises:
            RuntimeError: If server is not initialized.
            Exception: If tool execution fails after all retries.
        """
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        attempt = 0
        while attempt < retries:
            try:
                logger.info(f"Executing {tool_name}...")
                result = await self.session.call_tool(tool_name, arguments)

                return result

            except Exception as e:
                attempt += 1
                logger.warning(
                    f"Error executing tool: {e}. Attempt {attempt} of {retries}."
                )
                if attempt < retries:
                    logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logger.error("Max retries reached. Failing.")
                    raise

    async def cleanup(self) -> None:
        """Clean up server resources."""
        async with self._cleanup_lock:
            try:
                await self.exit_stack.aclose()
                self.session = None
                self.stdio_context = None
            except Exception as e:
                logger.error(f"Error during cleanup of server {self.name}: {e}")
