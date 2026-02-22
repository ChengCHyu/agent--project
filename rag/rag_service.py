#总结服务类:用户提问,搜索参考资料,将提问和参考资料提交给模型,让模型总结回复
from langchain_core.documents import Document
from rag.vector_store import vectorstoreservice
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
def print_prompt(prompt):
    print("="*50)
    print(prompt.to_string())
    print("="*50)
    return prompt
class RagSummarizeService(object):
    def __init__(self):
        self.vector_store=vectorstoreservice()
        self.retriever=self.vector_store.get_retriever()
        self.prompt_text=load_rag_prompts()
        self.prompt_template=PromptTemplate.from_template(self.prompt_text)
        self.model=chat_model
        self.chain=self._init_chain()
    def _init_chain(self):
        chain =self.prompt_template | print_prompt |self.model |StrOutputParser()
        return chain
    def retriever_docs(self,query:str)->list[Document]:
        docs=self.retriever.invoke(query)
        return docs
    def rag_summarize(self,query:str)->str:
        content_docs=self.retriever_docs(query)
        context=""
        counter=0
        for doc in content_docs:
            counter+=1
            context+=f"[参考资料]第{counter}段内容:参考资料:{doc.page_content}|参考元数据:{doc.metadata}\n"
        return self.chain.invoke({
            "question":query,
            "context":context,
        })
if __name__ == "__main__":
    rag_service=RagSummarizeService()
    print(rag_service.rag_summarize("考研3月干什么"))

