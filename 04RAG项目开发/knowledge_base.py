"""
建立知识库

主要任务：
    md5去重 为什么？ 因为它就32位，快，省空间
    向量库存入
    维护类

【注意：做好功能分隔的项目才是合格的项目，数据处理归数据处理，页面搭建归页面搭建....】
"""
"""
疑问部分：
    1、check_md5 中 readlines 一行行匹配查重的方法感觉有点怪
    2、get_string_md5 中 为什么要先将字符串转换为字节数组，然后再转十六进制字符串，不能字符串直接转换吗？
        答：md5哈希接受字节数据，不接受字符串
    3、upload_by_str 中判断字符串大小是否超过1000，再进行分割是不是多余？RecursiveCharacterTextSplitter设置的时候不是已经写好了吗
    4、想删除知识库知识怎么办？
        可尝试的解法：将知识文档id提取出来，做一个想要web界面删除id的函数

可改进部分：
    1、数据存入数据库中
    2、DashScopeEmbeddings可能会过期，考虑换成本地模型
    3、在以后的项目实现【小说、ai女友/男友】要把文本嵌入中的方法改掉，改成使用spliter_documents 而不是简陋的字符串 
        原因：
            手里只有纯文本字符串，不需要维护元数据	split_text
            需要将分割后的文本块与原始文档信息（如文件名、页码、标题）关联起来	split_documents
            正在构建一个 RAG 管道，后续需要根据文档块定位来源	split_documents
"""
import hashlib
import os
import config_data as config
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def get_string_md5(input_str: str, encoding="utf-8"):
    """将传入的字符串转为MD5字符串"""
    # 将字符串转换为字节数组
    str_bytes = input_str.encode(encoding=encoding)

    # 创建md5哈希对象
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)  # 传入即将要转换的字节数组
    md5_hex = md5_obj.hexdigest()  # 得到MD5十六进制字符

    return md5_hex


def check_md5(md5_str: str):
    """检查传入md5 数据检查是否重复
        文件存在返回True
        不存在返回False
        """
    if not os.path.exists(config.md5_path):
        # 文件路径检查，查看当前文件存放的路径是否存在文件，不在创建文件
        open(config.md5_path, "w", encoding="utf-8").close()
        return False
    else:
        # 文件已存在, 查找文件内容
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            line = line.strip()  # 删除无效空格和换行符
            if line == md5_str:
                return True
    return False


def save_md5(md5_str: str):
    """将传入的字符串记录到文件中保存"""
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + '\n')
    pass


class KnowledgeBaseService(object):
    """对数据向量化处理的库"""
    def __init__(self):
        # # 创建目录文件，允许存在则跳过
        # os.makedirs(config.md5_path, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,  # 数据库表名
            embedding_function=DashScopeEmbeddings(
                model="text-embedding-v4"
            ),
            persist_directory=config.persist_directory
        )  # 向量存储的实例化 Chroma 对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        )  # 文本分割器的对象


    def upload_by_str(self, data: str, file_name):
        """将存入的数据向量化，存入向量数据库中"""
        # 在这里联系起本项目中的函数进行处理
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "[跳过]内容已存在知识库中"

        if len(data) > config.min_spliter_number:
            # list[str] 是根据 split_text 的返回值拿出来的
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            # 不分割时直接放进列表 和 list[str] 统一格式
            knowledge_chunks = [data]
        metadata = {  # 定义元数据 来源等信息 字典形式
            "source": file_name,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "deepseek"
        }

        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        save_md5(md5_hex)

        return "[成功]内容已经成功载入知识库"


if __name__ == "__main__":
    pass

