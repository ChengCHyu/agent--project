from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
def load_system_prompts():
    try:
        system_prompt_path =get_abs_path(prompts_conf['main_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yaml配置中没有main_prompt_path配置项")
        raise e
    try:
        return open(system_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_system_prompts]读取system_prompt_path失败，请检查路径是否正确，错误信息：{e}")
        raise e
def load_rag_prompts():
    try:
        system_prompt_path =get_abs_path(prompts_conf['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置中没有rag_summarize_prompt_path配置项")
        raise e
    try:
        return open(system_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]读取rag_summarize_prompt_path失败，请检查路径是否正确，错误信息：{e}")
        raise e
def load_report_prompts():
    try:
        report_prompt_path =get_abs_path(prompts_conf['report_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yaml配置中没有report_prompt_path配置项")
        raise e
    try:
        return open(report_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_report_prompts]读取report_prompt_path失败，请检查路径是否正确，错误信息：{e}")
        raise e
if __name__ == '__main__':
    print(load_system_prompts())
    print(load_rag_prompts())
    print(load_report_prompts())