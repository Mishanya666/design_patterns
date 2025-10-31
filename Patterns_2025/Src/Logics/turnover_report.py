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
    def generate(start_date: date, end_date: date, storage_code: str, t=None) -> List[Dict]:
        """
        Формирует ОСВ за период по складу.
        :param start_date: Дата начала.
        :param end_date: Дата окончания.
        :param storage_code: Уникальный код склада.
        :return: Список словарей с данными ОСВ.
        """
        validator.validate(start_date, date)
        validator.validate(end_date, date)
        validator.validate(storage_code, str)
        if start_date > end_date:
            raise operation_exception("Дата начала не может быть позже даты окончания!")

        repo = reposity()
        transactions: List[transaction_model] = repo.data.get(reposity.transaction_key(), [])
        nomenclatures: List[nomenclature_model] = repo.data.get(reposity.nomenclature_key(), [])
        storages: List[storage_model] = repo.data.get(reposity.storage_key(), [])

        storage = next((s for s in storages if s.unique_code == storage_code), None)
        if not storage:
            raise operation_exception(f"Склад с кодом {storage_code} не найден!")

        report = []
        for nom in nomenclatures:
            # Фильтр транзакций (все в базовых единицах, без конверсии)
            trans_before = [t for t in transactions if
                            t.nomenclature == nom and t.storage == storage and t.date < start_date]
            trans_period = [t for t in transactions if
                            t.nomenclature == nom and t.storage == storage and start_date <= t.date <= end_date]

            initial_balance = sum(t.quantity for t in trans_before)
            income = sum(t.quantity for t in trans_period if t.quantity > 0)
            expense = abs(sum(t.quantity for t in trans_period if t.quantity < 0))
            final_balance = initial_balance + income - expense

            report.append({
                "nomenclature": nom.name,
                "unit": nom.base_unit if hasattr(nom, 'base_unit') else t.unit.name if trans_period else 'base',
                # Базовая единица
                "initial_balance": initial_balance,
                "income": income,
                "expense": expense,
                "final_balance": final_balance
            })

        return report