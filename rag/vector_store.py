from langchain_chroma import Chroma
from utils.config_handler import chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import pdf_loader,text_loader,get_file_md5_hex,listdir_with_allowed_type
from utils.logger_handler import logger
from utils.path_tool import get_abs_path
import os
class vectorstoreservice:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"],
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})
    def load_documents(self):
        #从数据文件夹内读取文件,转为向量存入向量库,计算md5做去重
        def check_md5_hex(md5_for_check:str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                return False
        def save_md5_hex(md5_for_save:str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_save+"\n")
        def get_file_documents(read_path:str):
            if read_path.endswith("txt"):
               return text_loader(read_path)
            if read_path.endswith("pdf"):
               return pdf_loader(read_path)
            return []
        allowed_files_path=listdir_with_allowed_type(chroma_conf["data_path"],tuple(chroma_conf["allowed_file_type"]))
        for path in allowed_files_path:
            md5_hex=get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已存在知识库内,跳过")
                continue
            try:
                doucuments=get_file_documents(path)
                if not doucuments:
                    logger.warning(f"[加载知识库]{path}内容为空,跳过")
                    continue
                split_document=self.spliter.split_documents(doucuments)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}内容为空,跳过")
                    continue
            #将内容放入向量库
                self.vector_store.add_documents(split_document)
            #记录这个已经处理的文件的md5
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库]{path}内容加载成功")
            except Exception as e:
                #exc_info=True,会记录详细的报错堆栈
                logger.error(f"[加载知识库]{path}内容加载失败,错误信息：{e}",exc_info=True)
                continue
if __name__ == '__main__':
    vectorstore=vectorstoreservice()
    vectorstore.load_documents()
    retriever=vectorstore.get_retriever()
    res = retriever.invoke("复试")
    for r in res:
        print(r.page_content)
        print("="*50)