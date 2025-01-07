


class BadRequest(Exception):
    def __init__(self, message, error_code=400):
        super().__init__(message)  # 调用父类的构造函数并传递异常消息
        self.error_code = error_code  # 添加自定义属性 error_code
        self.message = message  # 添加自定义属性 message
        self.status_code = 400  # 添加自定义属性 status_code

    def log_error(self):
        # 添加自定义方法来记录错误
        logger.warning(f"{self.__class__.__name__} ({self.error_code}): {self.args[0]}")


class Forbidden(Exception):
    def __init__(self, message, error_code=403):
        super().__init__(message)  # 调用父类的构造函数并传递异常消息
        self.error_code = error_code  # 添加自定义属性 error_code
        self.message = message  # 添加自定义属性 message
        self.status_code = 403  # 添加自定义属性 status_code

    def log_error(self):
        # 添加自定义方法来记录错误
        logger.warning(f"{self.__class__.__name__} ({self.error_code}): {self.args[0]}")