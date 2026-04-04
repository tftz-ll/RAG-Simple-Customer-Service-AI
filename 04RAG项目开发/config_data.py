"""
存放配置文件
"""

# MD5数据存放地址
md5_path = "./md5.text"

# chroma 数据存放
# collection_name = "rag_test"
collection_name = "rag_test_sister"
# persist_directory = "./chroma_db_test"
persist_directory = "./chroma_db_test_sister"

# spliter 相关参数
chunk_size = 500
chunk_overlap = 100
separators = [",", ".", "?", "!", "，", "。", "？", "！", " "]
# 只有当文本大于1000时才需要分割
min_spliter_number = 1000

# retriever 相关参数
similarity_k = 3  # 最大文本匹配数

# rag 相关参数
model_name = "qwen3.5-flash"
embedding_name = "text-embedding-v4"

# 历史会话存储
chat_store_path = r".\chat_history"
config = {
    "configurable": {
        "session_id": "user_001"
    }
}

a = {'input': {'input': '我身高175，体重55公斤，推荐我什么尺码的衣服？', 'history': []},
     'history': {'input': '我身高175，体重55公斤，推荐我什么尺码的衣服？', 'history': []},
     'context': "[文档知识:身高：155-165cm， 体重：75-95 斤，建议尺码S。\n身高：160-170cm， 体重：90-115斤，建议尺码M。\n身高：165-175cm， 体重：115-135斤，建议尺码L。\n身高：170-178cm， 体重：130-150斤，建议尺码XL。\n身高：175-182cm， 体重：145-165斤，建议尺码2XL。\n身高：178-185cm， 体重：160-180斤，建议尺码3XL。\n身高：180-190cm， 体重：180-210斤，建议尺码4XL。\n身高：190cm+，体重：210斤+，建议尺码5XL。, medata{'source': '尺码推荐.txt', 'operator': 'deepseek', 'create_time': '2026-03-31 11:01:04'}\n]"
     }













