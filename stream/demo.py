import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="千问Plus", layout="wide")
st.title("🤖 通义千问Plus")

client = OpenAI(
    api_key="sk-139a40229c0e4bd58191a7a2f8c9c8f3",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_completion(text):
    try:
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *st.session_state.messages,  # 包含历史消息
                {"role": "user", "content": text},
            ],
            stream=True,
            stream_options={"include_usage": True}
        )
        return completion
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        return None

# 显示聊天历史，本质是循环再显示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 获取用户输入,海象运算符 := 一种赋值表达式，允许在表达式中同时进行赋值和条件判断
if prompt := st.chat_input("请输入您的问题..."):
    # 添加用户消息到历史记录
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 使用 st.chat_message("user") 创建一个代表用户的消息气泡,在消息气泡内显示用户输入的内容
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 使用 st.empty() 创建一个空容器，用于动态更新内容，创建 full_response 字符串，用于逐步构建完整的 AI 响应
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 处理流式响应
        response = get_completion(prompt)
        if response:
            try:
                for chunk in response:
                    if hasattr(chunk, 'choices') and chunk.choices and hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")# 使用▌字符模拟打字光标，增强交互感。
                
                message_placeholder.markdown(full_response)
                
                # 只有在成功获取到响应时才添加到历史记录
                if full_response:
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error("未能获取到有效的响应")
            except Exception as e:
                st.error(f"处理响应时发生错误: {str(e)}")


if st.sidebar.button("清除聊天历史"):
    st.session_state.messages = []
    st.rerun()  # 重新运行应用，使界面更新反映清除后的状态


with st.sidebar:
    st.markdown("""
    ### 使用说明
    1. 在输入框中输入您的问题
    2. 按回车键或点击发送按钮
    3. 等待AI助手的回答
    4. 可以点击"清除聊天历史"重新开始对话
    
    ### 功能特点
    - 支持流式输出
    - 保存聊天历史
    - 支持Markdown格式
    """)