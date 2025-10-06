from Src.exceptions import argument_exception

class abstract_reference:
    def __init__(self, name: str = ""):
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        value = value.strip()
        if len(value) > 50:
            raise argument_exception("Наименование не может превышать 50 символов")
        self._name = value