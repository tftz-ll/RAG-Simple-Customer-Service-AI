import time
from rag import RagService
import streamlit as st
import config_data
# 标题
st.title("奇迹与你")
st.divider()  # 分隔符

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你好，有什么可以帮到你的吗？"}]

for messages in st.session_state["messages"]:
    st.chat_message(messages["role"]).write(messages["content"])

# 页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:

    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # 页面中输出用户提问
    with st.spinner("Thinking....."):
        response = st.session_state["rag"].chain.stream({"input": prompt}, config_data.config)

        res = st.chat_message("assistant").write_stream(response)
        st.session_state["messages"].append({"role": "assistant", "content": res})












