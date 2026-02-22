from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
import os
import json
import random
rag=RagSummarizeService()
user_ids=["U001","U002","U003","U004"]
month_arr=["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]
external_data={}
@tool(description="使用RAG模型进行摘要")
def rag_summarize(text:str)->str:
    return rag.rag_summarize(text)
@tool(description="获取指定城市的天气")
def get_weather(city:str)->str:
    return f"城市{city}的天气是晴天,气温26摄氏度,空气湿度为50%"
@tool(description="获取该用户所在城市的名称,以纯字符串形式返回")
def get_user_location()->str:
    return random.choice(["北京","上海","广州","深圳"])
@tool(description="获取用户的ID,以纯字符串形式返回")
def get_user_id()->str:
    return random.choice(user_ids)
@tool(description="获取当前月份,以纯字符串形式返回")
def get_current_month()->str:
    return random.choice(month_arr)   
def generate_external_data():
  if not external_data:
    external_data_path = get_abs_path(agent_conf["external_data_path"])
    if not os.path.exists(external_data_path):
        raise FileNotFoundError(f"外部数据文件不存在:{external_data_path}")
    with open(external_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for user in data['users']:
        user_id = user['user_id']
        queries = [item['query'] for item in user['queries']]
        external_data[user_id] = queries
@tool(description="从外部系统中获取用户的使用记录,以纯字符串形式返回,如果未检索到返回空字符串")
def fetch_external_data(user_id: str) -> str:
    generate_external_data()
    
    try:
        return external_data[user_id]
    except KeyError:
        logger.warning(f"[获取外部数据]{user_id}未检索到使用记录")
        return ""
@tool(description="无入参,无返回值,调用后触发中间件自动为报告生成的场景动态注入上下文信息,为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已被调用"
if __name__ == "__main__":
    result = fetch_external_data.invoke("U001")
    print(result)