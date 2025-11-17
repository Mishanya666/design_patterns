from Src.Core.prototype import IPrototype
from Src.Dtos.filter_dto import filter_dto
from typing import List, Dict, Callable, Optional, Any
from copy import deepcopy

class DataPrototype(IPrototype):
    def __init__(self, settings=None):
        self._data: List[dict] = []
        self._filter_func: Optional[Callable[[dict, filter_dto], bool]] = None
        self._nested_lookup: Optional[Callable[[dict, str], Any]] = None
        self._result_mapper: Optional[Callable[[dict], dict]] = None
        self._settings = settings  # <-- ВНЕШНИЕ НАСТРОЙКИ

    # Настройка
    def set_data(self, data: List[dict]) -> 'DataPrototype':
        self._data = data
        return self

    def set_filter(self, func: Callable[[dict, filter_dto], bool]) -> 'DataPrototype':
        self._filter_func = func
        return self

    def set_nested_lookup(self, func: Callable[[dict, str], Any]) -> 'DataPrototype':
        self._nested_lookup = func
        return self

    def set_result_mapper(self, func: Callable[[dict], dict]) -> 'DataPrototype':
        self._result_mapper = func
        return self

    # КЛОНИРОВАНИЕ
    def clone(self) -> 'DataPrototype':
        return deepcopy(self)

    # ВЫПОЛНЕНИЕ
    def execute(self, data: Optional[List[dict]] = None, filter_dto: filter_dto = None) -> List[dict]:
        if data is not None:
            self._data = data

        if not self._filter_func or not filter_dto:
            return [self._result_mapper(item) if self._result_mapper else item for item in self._data]

        result = []
        for item in self._data:
            if self._apply_filters(item, filter_dto):
                mapped = self._result_mapper(item) if self._result_mapper else item
                result.append(mapped)
        return result

    def _apply_filters(self, item: dict, dto: filter_dto) -> bool:
        if not self._filter_func(item, dto):
            return False

        if dto.base_id and self._nested_lookup:
            current_range_id = self._nested_lookup(item, "range_id")
            if not self._check_base_recursive(current_range_id, dto.base_id):
                return False

        return True

    def _check_base_recursive(self, range_id: str, target_id: str) -> bool:
        if range_id == target_id:
            return True

        if not self._settings:
            return False

        ranges = self._settings.get("default_refenences", {}).get("ranges", [])
        range_item = next((r for r in ranges if r["id"] == range_id), None)
        if not range_item or not range_item.get("base_id"):
            return False

        return self._check_base_recursive(range_item["base_id"], target_id)