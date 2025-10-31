from abc import ABC, abstractmethod
from typing import Any, Dict


class abstract_converter(ABC):
    """
    Абстрактный класс для конвертации объектов в словарь.
    """

    @abstractmethod
    def convert(self, obj: Any) -> Dict[str, Any]:
        """
        Абстрактный метод для конвертации объекта в словарь {field_name: field_value}.
        """
        pass