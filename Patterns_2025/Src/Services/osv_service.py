from Src.Core.osv_prototype import IOSVPrototype
from Src.Dtos.filter_dto import filter_dto
from typing import List, Dict
from collections import defaultdict
from datetime import datetime

class OSVService(IOSVPrototype):
    def __init__(self, settings_data):
        self._transactions = settings_data.get("default_transactions", [])
        self._nomenclatures = {n["id"]: n for n in settings_data.get("default_nomenclatures", [])}
        self._ranges = {r["id"]: r for r in settings_data.get("ranges", [])}

    def calculate(self, transactions: List[Dict], filter_dto: filter_dto) -> List[Dict]:
        filtered = self._filter_transactions(transactions, filter_dto)
        balance = defaultdict(float)

        for t in sorted(filtered, key=lambda x: x["period"]):
            key = (t["nomenclature_id"], t["storage_id"])
            balance[key] += t["value"]

        result = []
        for (nom_id, storage_id), saldo in balance.items():
            nom = next((n for n in self._nomenclatures if n["id"] == nom_id), {})
            result.append({
                "nomenclature": nom.get("name", "Неизвестно"),
                "storage": "Общий склад",
                "saldo": round(saldo, 3),
                "unit": self._get_unit_name(nom.get("range_id"))
            })
        return result

    def _filter_transactions(self, txs: List[Dict], dto: filter_dto) -> List[Dict]:
        res = []
        for t in txs:
            nom = next((n for n in self._nomenclatures if n["id"] == t["nomenclature_id"]), {})
            if dto.name and not self._like(nom.get("name", ""), dto.name):
                continue
            if dto.code and not self._equals(nom.get("code", ""), dto.code):
                continue
            res.append(t)
        return res

    def _like(self, a: str, b: str) -> bool:
        return b.lower() in a.lower() if a and b else True

    def _equals(self, a: str, b: str) -> bool:
        return a == b if a and b else True

    def _get_unit_name(self, range_id: str) -> str:
        r = self._ranges.get(range_id)
        return r["name"] if r else ""