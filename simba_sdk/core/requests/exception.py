class RequestException(Exception):
    def __init__(self, status_code: int, message: str):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

    def __str__(self) -> str:
        return str(self.__dict__)


class EnsureException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
