from Src.Logics.abstract_converter import abstract_converter
from typing import Any, Dict
from datetime import datetime
from Src.Core.validator import validator


class datetime_converter(abstract_converter):
    """
    Конвертер для типа datetime.
    """

    def convert(self, obj: Any) -> Dict[str, Any]:
        """
        Конвертирует datetime в словарь с ISO строкой.
        """
        validator.validate(obj, datetime)
        return {'isoformat': obj.isoformat()}