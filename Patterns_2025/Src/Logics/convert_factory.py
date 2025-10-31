from typing import Any, Dict, List
from Src.Logics.abstract_converter import abstract_converter
from Src.Logics.basic_converter import basic_converter
from Src.Logics.datetime_converter import datetime_converter
from Src.Logics.reference_converter import reference_converter
from datetime import datetime
from Src.Core.validator import validator


class convert_factory:
    """
    Фабрика для конвертации объектов в словари.
    """

    def __init__(self):
        # Конвертеры по типам
        self.converters: Dict[type, abstract_converter] = {
            int: basic_converter(),
            float: basic_converter(),
            str: basic_converter(),
            bool: basic_converter(),
            datetime: datetime_converter()
        }

    def convert(self, obj: Any) -> Any:
        """
        Конвертирует любой объект в словарь или список словарей.
        """
        # 1. Обработка None
        if obj is None:
            return None

        # 2. Обработка списков
        if isinstance(obj, list):
            return [self.convert(item) for item in obj]

        # 3. Обработка словарей
        if isinstance(obj, dict):
            return {key: self.convert(value) for key, value in obj.items()}

        # 4. Поиск подходящего конвертера по типу объекта
        obj_type = type(obj)
        if obj_type in self.converters:
            return self.converters[obj_type].convert(obj)

        # 5. Все остальные объекты — ссылочные (модели, DTO)
        # Используем reference_converter через фабрику (рекурсия!)
        from Src.Logics.reference_converter import reference_converter
        return reference_converter(self).convert(obj)