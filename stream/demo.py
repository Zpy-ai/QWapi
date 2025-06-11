import streamlit as st
from openai import OpenAI

# 设置页面标题和配置
st.set_page_config(page_title="千问Plus", layout="wide")
st.title("🤖 通义千问Plus")

# 初始化OpenAI客户端
client = OpenAI(
    api_key="sk-139a40229c0e4bd58191a7a2f8c9c8f3",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 初始化聊天历史
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

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 获取用户输入
if prompt := st.chat_input("请输入您的问题..."):
    # 添加用户消息到历史记录
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 获取AI响应
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
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # 只有在成功获取到响应时才添加到历史记录
                if full_response:
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error("未能获取到有效的响应")
            except Exception as e:
                st.error(f"处理响应时发生错误: {str(e)}")

# 添加清除聊天按钮
if st.sidebar.button("清除聊天历史"):
    st.session_state.messages = []
    st.experimental_rerun()

# 添加侧边栏说明
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