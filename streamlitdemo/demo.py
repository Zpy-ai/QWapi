import streamlit as st
from openai import OpenAI


client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=("sk-139a40229c0e4bd58191a7a2f8c9c8f3"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
def get_completion(text):
    completion = client.chat.completions.create(
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ],
    )
    return completion


st.title("通义千问")


prompt = st.chat_input("快输入你的内容")

if prompt:
    user_message = st.chat_message("user")
    user_message.write(prompt)

    response = get_completion(prompt)
    ai_message = st.chat_message("ai")
    ai_message.write(response)




# streamlit run demo.py