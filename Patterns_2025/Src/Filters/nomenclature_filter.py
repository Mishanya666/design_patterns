from Src.Core.filter_prototype import IFilterPrototype
from Src.Dtos.filter_dto import filter_dto
from typing import List
from Src.Models.nomenclature_model import nomenclature_model

class NomenclatureFilter(IFilterPrototype):
    def __init__(self, data_source):
        self._nomenclatures = data_source["nomenclatures"]
        self._ranges = {r["id"]: r for r in data_source["ranges"]}

    def filter(self, items: List[nomenclature_model], dto: filter_dto) -> List[nomenclature_model]:
        result = []
        for item in items:
            if not self._matches(item.name, dto.name, dto.name_filter):
                continue
            if not self._matches(item.code, dto.code, dto.code_filter):
                continue

            # Проверка по базовой единице измерения
            if dto.base_id:
                nom_data = next((n for n in self._nomenclatures if n["id"] == item.id), None)
                if not nom_data or not self._check_base_range(nom_data["range_id"], dto.base_id):
                    continue

            result.append(item)
        return result

    def _check_base_range(self, range_id: str, target_base_id: str) -> bool:
        range_item = self._ranges.get(range_id)
        if not range_item:
            return False
        if range_item["base_id"] == target_base_id:
            return True
        if range_item["base_id"] is None:
            return False
        return self._check_base_range(range_item["base_id"], target_base_id)