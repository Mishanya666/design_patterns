from Src.Logics.abstract_converter import abstract_converter
from typing import Any, Dict

class reference_converter(abstract_converter):
    """
    Конвертер для ссылочных типов (модели, DTO).
    Использует фабрику для рекурсивной конвертации полей.
    """

    def __init__(self, factory):

        self.factory = factory

    def convert(self, obj: Any) -> Dict[str, Any]:
        """
        Конвертирует объект в словарь {поле: значение}.
        Рекурсивно конвертирует все поля через фабрику.
        """
        if not hasattr(obj, '__dict__'):
            raise ValueError(f"Объект {obj} не является ссылочным типом (нет __dict__)")

        result = {}
        for key, value in obj.__dict__.items():

            if key.startswith('_'):
                continue
            result[key] = self.factory.convert(value)
        return result