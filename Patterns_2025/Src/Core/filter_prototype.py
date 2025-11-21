from abc import ABC, abstractmethod
from typing import List, Any

from Src.Core.filter_type import FilterType
from Src.Dtos.filter_dto import filter_dto

class IFilterPrototype(ABC):
    @abstractmethod
    def filter(self, items: List[Any], filter_dto: filter_dto) -> List[Any]:
        pass

    def _matches(self, value: str, pattern: str, filter_type: 'FilterType') -> bool:
        if pattern is None:
            return True
        if value is None:
            return False
        value_str = str(value).strip().lower()
        pattern_str = pattern.strip().lower()
        if filter_type == FilterType.EQUALS:
            return value_str == pattern_str
        elif filter_type == FilterType.LIKE:
            return pattern_str in value_str
        return False