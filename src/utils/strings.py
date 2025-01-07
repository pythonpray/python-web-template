import re


def camel_to_snake(camel_str: str):
    """
    将驼峰字符串转换成蛇形字符串的函数
    """
    snake_str = ""
    for i, char in enumerate(camel_str):
        if char.isupper() and i > 0:
            snake_str += "_" + char.lower()
        else:
            snake_str += char.lower()
    return snake_str


def snake_to_camel(snake_str: str, is_big_camel: bool = False):
    return re.sub(
        "_([a-zA-Z0-9])",
        lambda m: m.group(1).upper(),
        f"_{snake_str}" if is_big_camel else snake_str,
    )


def dict_camel_to_snake(d: dict):
    return {camel_to_snake(k): v for k, v in d.items()}


def dict_snake_to_camel(d: dict):
    return {snake_to_camel(k): v for k, v in d.items()}
