"""
基于Streamlit完成WEB网页上传服务

好处：简单的几行代码就可以完成快速的网页开发

每当 web 页面内容发生变化，本页代码重新执行
问题：1、状态丢失怎么解决？
        streamlit自带了session_state消息存放
     2、想要删除知识库只知识怎么办？
"""
import streamlit as st
import time
from knowledge_base import KnowledgeBaseService
# 创建大标题
st.title("知识库更新服务")

# 添加文件 file_uploader
uploader_file = st.file_uploader(
    label="请上传txt文件",
    type=["txt"],
    accept_multiple_files=False,  # 仅接受单个文件的上传
)

# 创建知识库对象
session = st.session_state
if "service" not in session:
    session["service"] = KnowledgeBaseService()


if uploader_file is not None:
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024  # 转换为KB单位

    # .subheader 二级标题
    st.subheader(f"文件名：{file_name}")
    # .write 网页中显示正常大小的文本
    st.write(f"格式：{file_type}| 大小：{round(file_size, 2)} KB")



    # getvalue() 获取字节数据 需要解码为字符串
    text = uploader_file.getvalue().decode("utf-8")
    with st.spinner("文件加载中..."):
        # 转圈动画
        res = session["service"].upload_by_str(text, file_name)
        time.sleep(1)
        st.write(res)







