from Src.Core.data_prototype import DataPrototype
from Src.Dtos.filter_dto import filter_dto
from collections import defaultdict
from typing import List

def osv_filter(transaction: dict, dto: filter_dto, nom_map: dict) -> bool:
    nom = nom_map.get(transaction["nomenclature_id"], {})
    if dto.name and dto.name_filter == "LIKE":
        if dto.name.lower() not in nom.get("name", "").lower():
            return False
    if dto.name and dto.name_filter == "EQUALS":
        if nom.get("name") != dto.name:
            return False
    return True

def calculate_osv(transactions: List[dict], nom_map: dict, range_map: dict) -> List[dict]:
    balance = defaultdict(float)
    for t in transactions:
        key = (t["nomenclature_id"], t["storage_id"])
        balance[key] += t["value"]

    result = []
    for (nom_id, storage_id), saldo in balance.items():
        nom = nom_map.get(nom_id, {})
        range_name = range_map.get(nom.get("range_id"), {}).get("name", "")
        result.append({
            "nomenclature": nom.get("name", "Неизвестно"),
            "storage": "Общий склад",
            "saldo": round(saldo, 3),
            "unit": range_name
        })
    return result

# Прототип для ОСВ
osv_prototype = DataPrototype()