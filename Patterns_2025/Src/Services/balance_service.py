from datetime import date, datetime
from typing import Dict, List
from collections import defaultdict
import json
import os

class BalanceService:
    CACHE_FILE = "cache/blocked_turnover.json"

    def __init__(self, settings):
        self.settings = settings
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        os.makedirs(os.path.dirname(self.CACHE_FILE), exist_ok=True)

    def _load_blocked_turnover(self) -> Dict[str, float]:
        if not os.path.exists(self.CACHE_FILE):
            return {}
        try:
            with open(self.CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def _save_blocked_turnover(self, data: Dict[str, float]):
        with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def recalculate_blocked_turnover(self):
        """Пересчитать и сохранить обороты до block_period"""
        block_date = self.settings.block_period
        transactions = self.settings.default_transactions

        turnover = defaultdict(float)
        for t in transactions:
            t_date = datetime.strptime(t["period"], "%Y-%m-%d").date()
            if t_date < block_date:
                key = f"{t['nomenclature_id']}|{t['storage_id']}"
                turnover[key] += t["value"]

        self._save_blocked_turnover(turnover)
        print(f"Обороты до {block_date} пересчитаны и сохранены.")

    def get_balance(self, as_of_date: date) -> List[dict]:
        block_date = self.settings.block_period
        all_tx = self.settings.default_transactions
        nom_map = {n["id"]: n["name"] for n in self.settings.default_refenences.get("nomenclatures", [])}
        range_map = {r["id"]: r["name"] for r in self.settings.default_refenences.get("ranges", [])}

        #Берём сохранённые обороты до block_date
        blocked = self._load_blocked_turnover()
        balance = defaultdict(float)
        for key, value in blocked.items():
            nom_id, storage_id = key.split("|")
            balance[(nom_id, storage_id)] = value

        #Добавляем транзакции от block_date до as_of_date
        for t in all_tx:
            t_date = datetime.strptime(t["period"], "%Y-%m-%d").date()
            if block_date <= t_date <= as_of_date:
                key = (t["nomenclature_id"], t["storage_id"])
                balance[key] += t["value"]

        #Формируем результат
        result = []
        for (nom_id, storage_id), saldo in balance.items():
            if saldo == 0:
                continue
            result.append({
                "nomenclature_id": nom_id,
                "nomenclature": nom_map.get(nom_id, "Неизвестно"),
                "storage": "Общий склад",
                "saldo": round(saldo, 3),
                "unit": range_map.get(
                    next((n for n in self.settings.default_refenences["nomenclatures"] if n["id"] == nom_id), {}).get("range_id", ""),
                    "шт"
                )
            })
        return sorted(result, key=lambda x: x["nomenclature"])