from abc import ABC
from datetime import date
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.range_model import range_model

class abstract_model(ABC):
    """
    Абстрактный базовый класс для всех моделей.
    """
    @property
    def unique_code(self) -> str:
        raise NotImplementedError()

class transaction_model(abstract_model):
    """
    Модель транзакции. Хранит количество в базовой единице.
    """
    def __init__(self, nomenclature: nomenclature_model, storage: storage_model,
                 quantity_base: float, date: date, range: range_model):
        self.nomenclature = nomenclature
        self.storage = storage
        self.quantity_base = quantity_base
        self.date = date
        self.range = range
        self._unique_code = f"{nomenclature.unique_code}_{storage.unique_code}_{date}"

    @property
    def unique_code(self) -> str:
        return self._unique_code