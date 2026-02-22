from abc import ABC, abstractmethod
from typing import Optional
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.embeddings import Embeddings
from utils.config_handler import rag_conf
from langchain_core.language_models.chat_models import BaseChatModel
class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) ->[Embeddings | BaseChatModel]:
        pass
class ChatModelFactory(BaseModelFactory):
    def generator(self) ->[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_conf["chat_model_name"])# TODO: 从配置文件中读取模型
class EmbeddingsFactory(BaseModelFactory):
    def generator(self) ->[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])# TODO: 从配置文件中读取模型
chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()