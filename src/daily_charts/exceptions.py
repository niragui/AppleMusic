

class InvalidID(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class RecordNotSet(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidCountry(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidMatch(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)