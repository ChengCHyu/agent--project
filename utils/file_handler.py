import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
def get_file_md5_hex(file_path: str): #获取文件的md5值
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        return
    if not os.path.isfile(file_path):
        logger.error(f"文件路径不是文件路径: {file_path}")
        return
    md5_obj = hashlib.md5()
    chunk_size = 4096       #4kb分片,避免文件过大爆内存
    try:
        with open(file_path, 'rb') as f:  #必须二进制存取
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
                """
                等价于:
                chunk =f.read(chunk_size)
                while chunk:
                    md5_obj.update(chunk)
                    chunk = f.read(chunk_size)
                """
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"获取文件md5失败: {file_path}, 错误: {e}")
        return
def listdir_with_allowed_type(path: str, allowed_types: tuple[str]): #获取文件夹的文件列表(允许的文件后缀)
      files = []
      if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allowed_types
      for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))
      return tuple(files)
def pdf_loader(file_path: str,passwd=None)->list[Document]: #加载pdf文件
    return PyPDFLoader(file_path,passwd=passwd).load()
def text_loader(file_path: str)->list[Document]: #加载文本文件
    return TextLoader(file_path, encoding='utf-8').load()
