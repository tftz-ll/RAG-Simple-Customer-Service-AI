import json
import os
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
import config_data


class FileChatMessageHistory(BaseChatMessageHistory):
    """先理清思路：
        1、文件以json数据形式保存
        2、读取时需要转换成messages
        3、保存时需要转列表信息为json数据保存
    """
    storage_path: str
    session_id: str

    def __init__(self, storage_path, session_id):
        self.storage_path = storage_path
        self.session_id = session_id

        self.file_path = os.path.join(self.storage_path, self.session_id)

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    @property
    def messages(self) -> list[BaseMessage]:
        """将信息从文件中取出"""
        print("messages运行")
        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """复制现有消息，添加新消息至现有消息中，转换信息类型，保存现有消息"""
        print("add_messages运行")
        all_messages = list(self.messages)
        all_messages.extend(messages)

        series_messages = [message_to_dict(message) for message in all_messages]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(series_messages, f)

    def clear(self) -> None:
        print("clear运行")
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)


def get_session_id(session_id):
    return FileChatMessageHistory(session_id, config_data.chat_store_path)

















