from Src.Logics.abstract_converter import abstract_converter
from typing import Any, Dict
from Src.Core.validator import validator, operation_exception


class basic_converter(abstract_converter):
    """
    Конвертер для простых типов: int, float, str, bool.
    """

    def convert(self, obj: Any) -> Dict[str, Any]:
        """
        Конвертирует простые типы в словарь. Для простых типов возвращает {'value': obj}.
        """
        validator.validate(obj, (int, float, str, bool))
        return {'value': obj}