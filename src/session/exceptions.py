

class ConnectionError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidToken(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)