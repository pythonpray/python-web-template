class BaseDomainError(Exception):
    def __init__(self, err_code: int, message: str, **kwargs):
        super().__init__(**kwargs)
        self.err_code = err_code
        self.message = message
