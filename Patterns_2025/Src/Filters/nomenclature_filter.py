from Src.Core.data_prototype import DataPrototype
from Src.Dtos.filter_dto import filter_dto

def nomenclature_filter(item: dict, dto: filter_dto) -> bool:
    if dto.name and dto.name_filter == "LIKE":
        if dto.name.lower() not in item["name"].lower():
            return False
    if dto.name and dto.name_filter == "EQUALS":
        if item["name"] != dto.name:
            return False
    if dto.code and item.get("id", "") != dto.code:
        return False
    return True

# Создаём базовый прототип
nomenclature_prototype = (
    DataPrototype()
    .set_filter(nomenclature_filter)
    .set_result_mapper(lambda x: {
        "id": x["id"],
        "name": x["name"],
        "range": x["range_id"]
    })
)