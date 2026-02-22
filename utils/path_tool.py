import os

def get_project_root():
    """
    获取项目根目录
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    

def get_abs_path(relative_path: str) -> str:
    """
    获取绝对路径
    """
    return os.path.join(get_project_root(), relative_path)


if __name__ == '__main__':
    print(get_abs_path("config/config.txt"))