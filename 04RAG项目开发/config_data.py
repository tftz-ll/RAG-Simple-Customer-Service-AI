"""
存放配置文件
"""

# MD5数据存放地址
md5_path = "./md5.text"

# redis 服务
redis_host = "localhost"
redis_password = ""
redis_port = 6379
redis_db = 0

# chroma 数据存放
collection_name = "rag_test"
# persist_directory = "./chroma_db_test"
persist_directory = "./chroma_db_test_0"

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
        "session_id": "user_000"
    }
}

# MongoDB数据库配置文件

mongodb_name = r"chat_histories"
mongodb_host = "localhost"
mongodb_port = 27017













