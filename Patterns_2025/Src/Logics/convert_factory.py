from typing import Any, Dict, List
from Src.Logics.abstract_converter import abstract_converter
from Src.Logics.basic_converter import basic_converter
from Src.Logics.datetime_converter import datetime_converter
from Src.Logics.reference_converter import reference_converter
from datetime import datetime
from Src.Core.validator import validator


class convert_factory:
    """
    Фабрика для конвертации объектов в словари с использованием подходящих конвертеров.
    """

    def __init__(self):
        self.converters = {
            (int, float, str, bool): basic_converter(),
            datetime: datetime_converter(),
            object: reference_converter()  
        }

    def convert(self, obj: Any) -> Any:
        """
        Конвертирует объект в словарь или список словарей.
        """
        if isinstance(obj, list):
            return [self.convert(item) for item in obj]

        obj_type = type(obj)
        for types, converter in self.converters.items():
            if isinstance(types, tuple) and obj_type in types:
                return converter.convert(obj)
            elif obj_type == types:
                return converter.convert(obj)

        return reference_converter().convert(obj)