import time
from rag import RagService
import streamlit as st
import config_data


def process_stream_response(
            _reasoning_content,
            _thinking_placeholder,
            _text_content,
            _text_placeholder,
            _st_messages,
            function: str
):
    if function == "cloud":
        for chunk in response:
            # """这里双层循环而不能直接索引是因为流式输出需要等待服务器将结果放进列表之中"""
            for content in chunk.content:
                res_type = content["type"]

                if res_type == "reasoning":
                    for i in content["summary"]:
                        _reasoning_content += i["text"]
                        _thinking_placeholder.markdown(_reasoning_content)

                if res_type == "text":
                    _text_content += content["text"]
                    _text_placeholder.markdown(_text_content)

        _st_messages.append(
            {"role": "assistant", "content": _text_content, "reasoning_content": _reasoning_content})

    elif function == "native":
        for chunk in response:
            reasoning = getattr(chunk, "additional_kwargs", 0)
            _reasoning_content += reasoning.get("reasoning_content", "")

            _text_content += getattr(chunk, "content", "")
            # print(reasoning_content)
            if _reasoning_content != "":
                _thinking_placeholder.markdown(_reasoning_content)
            _text_placeholder.markdown(_text_content)
        _st_messages.append(
            {"role": "assistant", "content": _text_content, "reasoning_content": _reasoning_content})

# 标题
st.title("『奇迹与你』")
st.divider()  # 分隔符

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService(config_data.function)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for messages in st.session_state["messages"]:
    if messages["role"] == "user":
        st.chat_message(messages["role"]).write(messages["content"])

    if messages["role"] == "assistant":
        with st.chat_message("assistant"):
            with st.expander("Thinking..."):
                st.write(messages["reasoning_content"])
            st.write(messages["content"])

# 页面最下方提供用户输入栏
prompt = st.chat_input("给『奇迹与你』发送消息")

if prompt:
    # 用户输出，用户对话记录
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # ai聊天窗口下的两个占位符 思考 和 文本
        with st.expander("Thinking..."):
            thinking_placeholder = st.empty()
        text_placeholder = st.empty()

    # 文本注入模型拿到响应迭代器
    response = st.session_state["rag"].chain.stream({"input": prompt}, config_data.config)

    # 两个变量，分别存放思考信息和文本输出信息
    reasoning_content = ""
    text_content = ""

    # 函数封装的主要部分
    # 需要提取的参数， response、reasoning_content、text_content、thinking_placeholder、text_placeholder、st.session_state["messages"].
    # 从响应中获取chunk片段 进行打印输出
    process_stream_response(
        reasoning_content,
        thinking_placeholder,
        text_content,
        text_placeholder,
        st.session_state["messages"],
        config_data.function
    )
    # for chunk in response:
    #     # """这里双层循环而不能直接索引是因为流式输出需要等待服务器将结果放进列表之中"""
    #     for content in chunk.content:
    #         res_type = content["type"]
    #
    #         if res_type == "reasoning":
    #             for i in content["summary"]:
    #                 reasoning_content += i["text"]
    #                 thinking_placeholder.markdown(reasoning_content)
    #
    #         if res_type == "text":
    #             text_content += content["text"]
    #             text_placeholder.markdown(text_content)
    #
    # st.session_state["messages"].append(
    #     {"role": "assistant", "content": text_content, "reasoning_content": reasoning_content})












