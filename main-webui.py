import gradio as gr
import time
import asyncio
from api.api_request import ApiRequest
from config.config import API_URL, WEB_SERVER_PORT, WEB_SERVER_HOST
api = ApiRequest(base_url=API_URL, no_remote_api=False)

open_id = "first_man"
session_id = "0"
examples_list = [["查看视频列表数据，生成数据分析报告"], ["分析一下美猴王大闹天宫的情况"], ["粉丝来源分析"], ["粉丝画像数据"], ["用户粉丝数"]]

# 定义一个生成器函数，模拟逐步生成回复
async def stream_response(message, history):
    global session_id
    async for chunk in api.data_assistant_chat(query=message, session_id=session_id, open_id=open_id):
        if chunk:
            await asyncio.sleep(0.005)
            new_history = history + [{"role": "assistant", "content": str(chunk)}]
            yield new_history  # 逐步更新历史记录



webui_title = """
# 抖数精灵 （Data Genius）
"""
init_message = [{"role": "assistant",
                 "content": "您好，我是抖数精灵，您的抖音运营数据分析助手。请告诉我您想了解的数据分析问题，我会为您提供详细的分析和建议。"}]
custom_css = """
#chat_bi {
    height: 60vh !important; /* 使聊天机器人高度占满整个视口 */
    overflow-y: auto !important; /* 添加滚动条以处理内容溢出 */
}
"""

# 定义 Gradio 界面
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown(webui_title)
    chatbot = gr.Chatbot(type="messages", value=init_message, elem_id="chat_bi")  # 创建 Chatbot 组件
    msg = gr.Textbox(label="输入你的问题")  # 用户输入框
    hidden_msg = gr.Textbox(visible=False)
    examples = gr.Examples(examples=examples_list, inputs=[hidden_msg], elem_id="examples")


    def user_submit(message, history):
        global session_id
        if not history or len(history) <= 1:
            session_id = "0"  # 如果历史记录为空，重置 session_id 为 0
        else:
            session_id = str(int(time.time()))  # 如果历史记录不为空，设置 session_id 为当前时间戳
        new_history = history + [{"role": "user", "content": message}]
        return "", new_history, message  # 返回空字符串、更新后的历史记录和用户消息

    hidden_msg.change(user_submit, [hidden_msg, chatbot], [msg, chatbot, hidden_msg], queue=False).then(
        stream_response,
        [hidden_msg, chatbot],
        chatbot
    )
    msg.submit(user_submit, [msg, chatbot], [msg, chatbot, msg], queue=False).then(
        stream_response,
        [msg, chatbot],
        chatbot
    )

# 启动 Gradio 应用
if __name__ == '__main__':
    demo.launch(server_name=WEB_SERVER_HOST, server_port=WEB_SERVER_PORT, share=False)
