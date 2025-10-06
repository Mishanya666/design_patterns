from Src.Core.entity_model import entity_model
from Src.Core.validator import validator

class ingredient_model(entity_model):
    __amount: float = 0.0
    __unit: object = None  # range_model

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        validator.validate(value, (int, float))
        self.__amount = float(value)

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, value):

        from Src.Models.range_model import range_model
        validator.validate(value, range_model)
        self.__unit = value
