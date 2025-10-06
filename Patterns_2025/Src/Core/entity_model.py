from Src.Core.abstract_model import abstact_model
from Src.Core.validator import validator


"""
Общий класс для наследования. Содержит стандартное определение: код, наименование
"""
class entity_model(abstact_model):
    __name: str = ""

    def __init__(self, name: str = ""):

        super().__init__()
        if name:
            validator.validate(name, str)
            self.__name = name.strip()
        else:
            self.__name = ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str)
        self.__name = value.strip()
