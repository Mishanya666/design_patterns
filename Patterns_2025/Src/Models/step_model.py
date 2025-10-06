from Src.Core.entity_model import entity_model
from Src.Core.validator import validator

class step_model(entity_model):
    __order: int = 0
    __description: str = ""

    def __init__(self, name: str = "", order: int = 0, description: str = ""):
        super().__init__(name)
        self.__order = order
        self.__description = description.strip() if description else ""

    @property
    def order(self) -> int:
        return self.__order

    @order.setter
    def order(self, value: int):
        validator.validate(value, int)
        self.__order = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        validator.validate(value, str)
        self.__description = value.strip()
