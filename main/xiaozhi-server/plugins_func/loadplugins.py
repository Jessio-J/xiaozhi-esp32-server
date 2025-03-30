import importlib
import pkgutil
from config.logger import setup_logging

TAG = __name__

logger = setup_logging()

def auto_import_modules(package_name):
    """
    自动导入指定包内的所有模块。

    Args:
        package_name (str): 包的名称，如 'functions'。
    """
    # 定义白名单列表
    whitelist = [
        'handle_exit_intent',
        'get_time',
        'raise_and_lower_the_volume'
    ]

    # 获取包的路径
    package = importlib.import_module(package_name)
    package_path = package.__path__

    # 遍历包内的所有模块
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        # 检查模块是否在白名单中
        if module_name in whitelist:
            # 导入模块
            full_module_name = f"{package_name}.{module_name}"
            importlib.import_module(full_module_name)
            logger.bind(tag=TAG).info(f"模块  package_name:'{package_name}' ; module_name :'{module_name}'已加载")
        else:
            logger.bind(tag=TAG).info(f"模块 '{module_name}' 不在白名单中，跳过加载")

auto_import_modules('plugins_func.functions')