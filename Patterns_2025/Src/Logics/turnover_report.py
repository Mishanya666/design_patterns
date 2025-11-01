from datetime import date
from typing import List, Dict
from Src.reposity import reposity
from Src.Models.transaction_model import transaction_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Core.validator import validator, operation_exception


class turnover_report:
    """
    Класс для формирования оборотно-сальдовой ведомости (ОСВ).
    """

    @staticmethod
    def generate(self, start_date: date, end_date: date, storage_code: str) -> list:
        storage = self._cache.get(storage_code)
        if not storage:
            raise operation_exception("Склад не найден")

        result = []
        # Берём только транзакции по указанному складу
        storage_transactions = [t for t in self._transactions if t.storage == storage]

        # Группируем по номенклатуре
        nom_dict = {}
        for t in storage_transactions:
            nom = t.nomenclature
            if nom not in nom_dict:
                nom_dict[nom] = []
            nom_dict[nom].append(t)

        for nom, trans_list in nom_dict.items():
            # Только транзакции в периоде
            trans_period = [t for t in trans_list if start_date <= t.date <= end_date]
            trans_before = [t for t in trans_list if t.date < start_date]

            initial = sum(t.quantity_base for t in trans_before)
            income = sum(t.quantity_base for t in trans_period if t.quantity_base > 0)
            outcome = sum(abs(t.quantity_base) for t in trans_period if t.quantity_base < 0)
            final = initial + income - outcome

            result.append({
                "nomenclature": nom.name,
                "initial_balance": initial,
                "income": income,
                "outcome": outcome,
                "final_balance": final
            })

        return result