import asyncio
import json
from types import GeneratorType
from typing import Any
from common.log import logger
from client.llm_client_qwen import _generate_response, _generate_response_stream
from common.utils import is_valid_json
from server.server import Server

messages = []


async def trim_messages(messages_list: list, max_messages: int) -> list:
    """Trim the messages list to ensure its length does not exceed max_messages using FIFO logic.
    Ensure that messages with {"role": "system"} are always retained.
    """
    system_messages = [msg for msg in messages_list if msg.get("role") == "system"]
    other_messages = [msg for msg in messages_list if msg.get("role") != "system"]

    if len(system_messages) + len(other_messages) > max_messages:
        # Calculate the maximum number of other messages to keep
        max_other_messages = max_messages - len(system_messages)
        other_messages = other_messages[-max_other_messages:]

    # Combine system messages and other messages
    return system_messages + other_messages

# async def trim_messages(messages_list: list, max_messages: int) -> list:
#     """Trim the messages list to ensure its length does not exceed max_messages using FIFO logic."""
#     if len(messages_list) > max_messages:
#         return messages_list[-max_messages:]
#     return messages_list


class DouyinOpenApiSession:
    """Orchestrates the interaction between user, LLM, and tools."""

    def __init__(self, servers: list[Server]) -> None:
        self.servers: list[Server] = servers
        # self.init_servers()

    async def init_servers(self) -> None:
        """Initialize all servers."""
        for server in self.servers:
            try:
                await server.initialize()
                # yield "Success to initialize server"
            except Exception as e:
                logger.error(f"Failed to initialize server: {e}")
                await self.cleanup_servers()
                return

    async def cleanup_servers(self) -> None:
        """Clean up all servers properly."""
        cleanup_tasks = []
        for server in self.servers:
            cleanup_tasks.append(asyncio.create_task(server.cleanup()))

        if cleanup_tasks:
            try:
                await asyncio.gather(*cleanup_tasks, return_exceptions=True)
            except Exception as e:
                logger.warning(f"Warning during final cleanup: {e}")

    async def process_llm_response(self, llm_response: str) -> str:
        """Process the LLM response and execute tools if needed.

        Args:
            llm_response: The response from the LLM.

        Returns:
            The result of tool execution or the original response.
        """

        try:
            tool_call = json.loads(llm_response)
            if "工具" in tool_call and "参数" in tool_call:
                logger.info(f"Executing tool: {tool_call['工具']}")
                logger.info(f"With arguments: {tool_call['参数']}")

                for server in self.servers:
                    tools = await server.list_tools()
                    if any(tool.name == tool_call["工具"] for tool in tools):
                        try:
                            result = await server.execute_tool(
                                tool_call["工具"], tool_call["参数"]
                            )

                            if isinstance(result, dict) and "progress" in result:
                                progress = result["progress"]
                                total = result["total"]
                                percentage = (progress / total) * 100
                                logger.info(
                                    f"Progress: {progress}/{total} "
                                    f"({percentage:.1f}%)"
                                )

                            return f"Tool execution result: {result}"
                        except Exception as e:
                            error_msg = f"Error executing tool: {str(e)}"
                            logger.error(error_msg)
                            return error_msg

                return f"No server found with tool: {tool_call['工具']}"
            return llm_response
        except json.JSONDecodeError:
            return llm_response

    async def start(self, query: str, session_id: str = None, open_id: str = "", max_messages: int = 18) -> Any:
        global messages
        yield "开始理解语义... ![加载中](https://static.fengmiai.com/source_image/loading.gif)"
        if session_id is None or session_id == "0":
            all_tools = []
            for server in self.servers:
                tools = await server.list_tools()
                all_tools.extend(tools)
            tools_description = "\n".join([tool.format_for_llm() for tool in all_tools])
            system_message = (
                "You are called 抖数精灵, a senior data analysis assistant, and you can use the following tools:\n\n"
                f"{tools_description}\n"
                "Your open_id:"f"{open_id}\n"
                "Choose the appropriate tool based on the user's question. \n"
                "IMPORTANT: When you need to use the tool, you must only use JSON for response, while planning the exact number of steps and step names for using the tools\n"
                "Before all the tool is fully tuned, you can only return the exact JSON object format below, nothing else:\n"
                "{\n"
                '    "工具": "tool-name",\n'
                '    "参数": {\n'
                '        "argument-name": "value"\n'
                '    },\n'
                '    "任务数": "Total number of steps"'
                '    "任务名称": "All step names"'
                '    "当前任务ID": "Current step ID"'
                '    "当前任务名": "Name of the current step"'
                "}\n\n"
                "After receiving all steps tool's response:\n"
                "If no tools are required, generate the content in Markdown format according to the following template, excluding JSON format:\n"
                "    # 一、数据概览与问题分析 \n"
                "    ## 1.1 Subheading\n"
                "     data_list to markdown table \n"
                "     - data list description"
                "     ![charts](chart_url)"
                "     - data charts description"
                "     ### problem title\n"
                "     - problem Content\n"
                "    ## 1.2 Subheading   \n"
                "     ..."
                "    # 二、优化建议 \n"
                "     ## 2.1 suggestions1\n"
                "     - suggestions1 Content\n"
                "     ..."
                "    # 三、总结 \n"
                "     - Content\n"
                "     ..."
                "1. Transform the raw data into a natural, conversational response\n"
                "2. Have a deep understanding of the data, find n potential problems, and provide n improvement suggestions\n"
                "3. Focus on the most relevant information,Be concise and don't say anything unnecessary\n"
                "4. Use appropriate context from the user's question\n"
            )
            messages.clear()
            messages.append({"role": "system", "content": system_message})

        if len(messages) > max_messages:  # 只保留20条对话的记忆
            messages = await trim_messages(messages_list=messages, max_messages=max_messages)

        try:
            messages.append({"role": "user", "content": query})
            logger.info("First Messages: %s", messages)
            yield "正在理解意图... ![加载中](https://static.fengmiai.com/source_image/loading.gif)"
            await asyncio.sleep(0.01)
            # llm_response = _generate_response(messages=messages)
            llm_response = _generate_response_stream(messages=messages)
            full_llm = ""
            for stream in llm_response:
                yield stream
                full_llm = stream
            logger.info("First llm_response: %s", full_llm)
            if is_valid_json(full_llm):
                tool_call = json.loads(full_llm)
                if "任务数" in tool_call and "当前任务ID" in tool_call and "当前任务名" in tool_call:
                    yield "开始规划任务..."
                    await asyncio.sleep(0.01)
                    steps = tool_call["任务数"]
                    step_names = tool_call["任务名称"]
                    curr_step_id = tool_call["当前任务ID"]
                    curr_step_name = tool_call["当前任务名"]
                    logger.info(
                        "steps：%s curr_step_id: %s curr_step_name: %s" % (steps, curr_step_id, curr_step_name))
                    curr_step_id = 1
                    yield "计算出共有%s个步骤, 分布为%s... ![加载中](https://static.fengmiai.com/source_image/loading.gif) " % (str(steps), step_names)
                    await asyncio.sleep(0.01)
                    while curr_step_id <= int(steps):
                        yield "正在执行第%s个任务: %s... ![加载中](https://static.fengmiai.com/source_image/loading.gif)" % (str(curr_step_id), str(curr_step_name))
                        await asyncio.sleep(0.01)
                        result = await self.process_llm_response(full_llm)
                        logger.info("process_llm_response result: %s" % result)

                        if result != full_llm:
                            messages.append({"role": "assistant", "content": full_llm})
                            messages.append({"role": "system", "content": result})
                            logger.info("curr_step_id: %s messages: %s" % (curr_step_id, messages))
                            yield "正在判断第%s个任务:'%s'的执行情况...  ![加载中](https://static.fengmiai.com/source_image/loading.gif)" % (str(curr_step_id), str(curr_step_name))
                            await asyncio.sleep(0.01)
                            llm_response_stream = _generate_response_stream(messages=messages)
                            curr_step_id += 1
                            full_llm = ""
                            # isEnd = True
                            for stream in llm_response_stream:
                                yield stream
                                full_llm = stream
                            if is_valid_json(full_llm):
                                logger.info("curr_step_id: %s llm_response: %s" % (curr_step_id, full_llm))
                                messages.append(
                                    {"role": "assistant", "content": full_llm}
                                )
                            else:
                                messages.append({"role": "assistant",
                                                 "content": 'The Json format is incorrect. Return again'})
                                continue
                        else:
                            messages.append({"role": "assistant", "content": llm_response})

                        # for stream int llm_response:
                        if is_valid_json(full_llm):
                            yield "正在做最后的总结... ![加载中](https://static.fengmiai.com/source_image/loading.gif)"
                            llm_response_stream_final = _generate_response_stream(messages=messages)
                            for stream in llm_response_stream_final:
                                yield stream


        except Exception as e:
            logger.error(f"Error processing LLM response: {e}")
            yield f"Error processing LLM response: {e}"
        finally:
            logger.info("Main finally")
