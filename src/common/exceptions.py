

class InvalidID(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MissingCountry(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidCountry(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
