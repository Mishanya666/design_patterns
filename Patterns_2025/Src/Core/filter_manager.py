from Src.Core.filter_prototype import IFilterPrototype
from Src.Dtos.filter_dto import filter_dto
from typing import Dict, Type, List, Any

class filter_manager:
    _filters: Dict[str, IFilterPrototype] = {}

    @classmethod
    def register(cls, model_type: str, filter_instance: IFilterPrototype):
        cls._filters[model_type] = filter_instance

    @classmethod
    def apply(cls, model_type: str, items: List[Any], dto: filter_dto) -> List[Any]:
        filter_obj = cls._filters.get(model_type)
        if not filter_obj:
            raise ValueError(f"Фильтр для модели {model_type} не зарегистрирован")
        return filter_obj.filter(items, dto)