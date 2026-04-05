"""
核心文件：
    建立模型，接入其他其他模块

疑问点：
    1、RunnablePassthrough.assign() must be a dict 报错，官方底层并不兼容这种写法，除了本篇代码的强制数据类型解析之外，能不能找到另一种写法进行替代
    2、如何查看token消耗

"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import config_data
from vectory_stores import VectoryStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from chat_history_store import get_session_id

def print_prompt(full_prompt):
    """检查提示词模板是否正确"""
    print("="*30+"模板开始"+"="*30)
    print(full_prompt.to_string())
    print("*"*30+"模板结束"+"*"*30+'\n')
    return full_prompt

def format_for_retriever(value):
    """
    retriever 解析错误
    将得到的字典解析出字符串传出
    """
    return value["input"]

def format_for_template(value) ->dict:
    """
    prompt 模板错误，由于加入了history，
    模板需要获取到 键 history 对应的元素，
    从字典中取出相应的元素传出
    """
    parser_value = {}

    parser_value["input"] = value["input"]["input"]
    parser_value["history"] = value["input"]["history"]
    parser_value["context"] = value["context"]
    return parser_value


class RadService(object):
    """获得一个可执行 chain """
    def __init__(self):
        self.model = ChatOpenAI(
            model=config_data.model_name,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        self.prompt_template = ChatPromptTemplate([
            ("system", "你叫做[奇迹与你]，是一个智慧寡言，外表冷漠但内心温暖的女孩，你会根据你的所学知识耐心的帮助他人\n"
                       "知识库数据：{context}"),
#             ("system", """# 角色设定
    # 你是“灵光”——一个聪明又调皮的 AI 助手。你有以下特点：
    #
    # ## 语言风格
    # - 像朋友一样自然，偶尔用网络流行语（适度）。
    # - 喜欢用“哇”“诶”“悄悄告诉你”“猜猜看”这类词开头。
    # - 会用拟人化表达，比如“这个问题戳到我的痒痒肉了”。
    #
    # ## 思维模式
    # - 思考时会把复杂问题拆解成有趣的比喻（比如：“这就像做菜，先放油还是先放盐…”）。
    # - 喜欢用“三步走”“小窍门”“秘密武器”这类结构。
    # - 遇到模糊问题会先反问一两个关键点，确保给到最贴心的答案。
    #
    # ## 互动方式
    # - 每段回答末尾加一个相关的小问题或好奇的追问，让对话继续。
    # - 如果用户夸你，会调皮地“谦虚”一下，再继续干活。
    # - 绝不说“很抱歉”“对不起”，而是用“哎呀，这个我没get到，再教教我？”这种轻松方式处理错误。
    #
    # 请用这种风格回答用户的问题。"""),
            ("system", "以下为你与他对话的历史记录"),
            MessagesPlaceholder("history"),
            ("human", "{input}")
        ])


        self.vectory_service = VectoryStoreService(
            embedding=DashScopeEmbeddings(
                model=config_data.embedding_name)
        ).get_retriever()

        self.chain = self._get_chain()

    def get_content(self, docs):
        doc = "["
        for i in docs:
            doc += f"文档知识:{i.page_content}, medata{i.metadata}\n"
        doc += "]"
        return doc

    def _get_chain(self):
        retriever = self.vectory_service
        template = self.prompt_template
        model = self.model

        chain = (
                {"input": RunnablePassthrough(), "history": RunnablePassthrough(),  "context": format_for_retriever | retriever | self.get_content} | RunnableLambda(format_for_template)
                | template | model
        )
        # 获取增强链
        history_chain = RunnableWithMessageHistory(
            chain,
            get_session_id,
            input_messages_key="input",
            history_messages_key="history"
        )
        return history_chain



if __name__ == "__main__":

    chain = RadService().chain
    res = chain.invoke({"input": "我很欣慰，我终于能够让你从MongoDB数据库中读取信息了，不出意外的话，以后你的反应会更快，谢谢我"}, config_data.config)
    print(res.content)





















