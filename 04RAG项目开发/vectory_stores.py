"""
作用：获得集成检索器 retriever，将用户提问进行向量化，进入向量库中查询相应的知识


疑问：每次提问都要从向量库中进行查询，这似乎有点消耗资源，能否做到控制是否进入向量库中查询？

"""
from langchain_chroma import Chroma
# from langchain_community.embeddings import
import config_data


class VectoryStoreService(object):
    """获取一个可加入 chain 的 retriever 工具"""

    def __init__(self, embedding):
        self.embedding = embedding
        self.vectory_story = Chroma(
            collection_name=config_data.collection_name,
            persist_directory=config_data.persist_directory,
            embedding_function=self.embedding
        )

    def get_retriever(self):
        vectory_retriever = self.vectory_story.as_retriever(
            search_kwargs={"k": config_data.similarity_k}
        )

        return vectory_retriever


if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever = VectoryStoreService(
        DashScopeEmbeddings(model="text-embedding-v4")
    )

    client = retriever.vectory_story._client
    collection = client.get_collection(config_data.collection_name)
    res = collection.get()
    print(res)








