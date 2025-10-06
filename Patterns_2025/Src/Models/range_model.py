from Src.Core.entity_model import entity_model
from Src.Core.validator import validator, argument_exception

class range_model(entity_model):
    __value: int = 1
    __base: 'range_model' = None

    """
    Значение коэффициента пересчета
    """
    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: int):
        validator.validate(value, int)
        if value <= 0:
            raise argument_exception("Некорректный аргумент!")
        self.__value = value

    """
    Базовая единица измерения
    """
    @property
    def base(self):
        return self.__base

    @base.setter
    def base(self, value):
        if value is not None:
            validator.validate(value, range_model)
        self.__base = value

    """
    Килограмм (в терминах грамма как базовой)
    """
    @staticmethod
    def create_kill():
        inner_gramm = range_model.create_gramm()
        return range_model.create("килограмм", inner_gramm)

    """
    Грамм
    """
    @staticmethod
    def create_gramm():
        return range_model.create("грамм")

    """
    Универсальный метод - фабричный
    """
    @staticmethod
    def create(name: str, base=None):
        validator.validate(name, str)
        inner_base = None
        if base is not None:
            validator.validate(base, range_model)
            inner_base = base
        item = range_model()
        item.name = name
        item.base = inner_base
        return item
