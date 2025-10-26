from Src.Logics.abstract_converter import abstract_converter
from typing import Any, Dict
from Src.Core.validator import validator
from Src.Logics.convert_factory import convert_factory


class reference_converter(abstract_converter):
    """
    Конвертер для ссылочных типов (пользовательские классы).
    """

    def convert(self, obj: Any) -> Dict[str, Any]:
        """
        Конвертирует объект пользовательского класса в словарь с полями.
        """
        if not hasattr(obj, '__dict__'):
            raise ValueError("Object is not a reference type with __dict__")

        result = {}
        factory = convert_factory()
        for key, value in obj.__dict__.items():
            result[key] = factory.convert(value)
        return result