import os


def get_env_var(var_name):
    """
    获取环境变量,如果环境变量不存在则抛出异常
    :param var_name: 环境变量名称
    :return: 获取到的环境变量
    """
    e = os.getenv(var_name)
    if e is None:
        raise EnvironmentError(f"环境变量{var_name}未设置")
    return e
