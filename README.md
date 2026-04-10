# 一个简易的RAG网页问答AI __『奇迹与你』__
___
## 简介：
&ensp;&ensp;&ensp;&ensp;这是一个基于langchain实现的增强检索生成AI（RAG），你可以将文本数据加载到知识库中，为ai提供相应的专业知识参考，接着，ai可以根据你的知识库内容对你进行专门的解答；
## 如何获取：
在终端执行
```bash
cd "安装目录"
git clone https://github.com/tftz-ll/RAG-Simple-Customer-Service-AI.git
```
## 使用方法
**提示**：在使用之前请先确认您拥有相应的配置软件，详细部分见后文的_使用前的注意事项_  
**提示**：本项目包含以下几种基础文件，其余部分文件为代码测试时产生，或者为可抛弃文件，建议删除：
### 文件介绍
+ app_file_uploader.py :
此文件可以为你创建一个用于加载知识库资料的web页面
使用方法：将终端切换到此文件所在目录，输入__"streamlit run app_file_uploader.py"__
```bash
cd "D:\04RAG项目开发"
streamlit run app_file_uploader.py
```
+ app_qa.py: 
此文件可以创建一个用于与大模型对话的web界面
使用方法：将终端切换到此文件所在目录，输入__"app_qa.py"__
```bash
cd "D:\04RAG项目开发"
streamlit run app_qa.py
```
+ chat_history_story.py:
大模型长期记忆功能实现模块，接入了MongoDB数据库，端口号等参数可在config_data配置文件中进行更改。
+ knowledge_base.py:
此文件实现了知识库加载的功能，通过redis去重，再通过chroma数据库存储向量化数据。
文件载入后，会根据config_data文件中的配置信息，将数据存放到对应目录，config_data中可以设置redis端口号等信息。
+ vectory_stores.py:
创建了一个可加入chain的retriever工具
+ rag.py:
核心文件：创建了一个加强检索的长期记忆模型。
+ config_data:
核心配置文件：配置了各类文件存放，数据库连接参数，模型切换等信息。您可以根据个人实际情况进行更改
## 使用前的注意事项
1. 使用前请先确保您已经下载了相应的库
```bash
pip install langchain_community langchain_chroma langchain_text_splitters redis streamlit langchain_core typing pymongo langchain_ollama langchain_openai
```
2. 第一次上传的版本用文件读取的方法替代了redis，Mongodb数据库
3. 请不要在一个问题的回答结束前连续提问第二个问题，当前并未解决这个问题
4. ollama的本地模型需要额外的配置，您可以参考教程：


