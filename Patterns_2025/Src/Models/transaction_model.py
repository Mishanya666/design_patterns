from datetime import date as date_type  # Импортируем тип
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.range_model import range_model
from Src.Core.validator import validator, argument_exception


class transaction_model:
    """
    Модель транзакции.
    """

    def __init__(self, date: date_type, unique_number: str, nomenclature: nomenclature_model,
                 storage: storage_model, quantity: float, unit: range_model):
        """
        :param date: Дата транзакции.
        :param unique_number: Уникальный номер.
        :param nomenclature: Номенклатура.
        :param storage: Склад.
        :param quantity: Количество (+ приход, - расход).
        :param unit: Единица измерения.
        """
        validator.validate(date, date_type)
        validator.validate(unique_number, str)
        validator.validate(nomenclature, nomenclature_model)
        validator.validate(storage, storage_model)
        validator.validate(quantity, float)
        validator.validate(unit, range_model)

        if not unique_number.strip():
            raise argument_exception("Уникальный номер не может быть пустым!")

        self.date = date
        self.unique_number = unique_number
        self.nomenclature = nomenclature
        self.storage = storage
        self.quantity = quantity
        self.unit = unit