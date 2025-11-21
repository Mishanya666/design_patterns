from Src.Models.company_model import company_model
from Src.Core.validator import validator, argument_exception
from Src.Core.response_formats import response_formats
from datetime import date
from typing import Optional
######################################
# Модель настроек приложения
class settings_model:
    def __init__(self):
        self.company = None
        self.default_refenences = {}
        self.default_transactions = []
        self.default_receipt = {}
        self.default_response_format = "json"
        self._block_period: Optional[date] = None  # НОВАЯ настройка

    @property
    def block_period(self) -> Optional[date]:
        return self._block_period or date(1900, 1, 1)

    @block_period.setter
    def block_period(self, value: str):
        from datetime import datetime
        self._block_period = datetime.strptime(value, "%Y-%m-%d").date()

    __company: company_model = None
    __default_response_format:str =  response_formats.csv()

    # Текущая организация
    @property
    def company(self) -> company_model:
        return self.__company
    
    @company.setter
    def company(self, value: company_model):
        validator.validate(value, company_model)
        self.__company = value


    @property
    def default_response_format(self) -> str:
        return self.__default_response_format

    # Формат ответа по умолчанию
    @default_response_format.setter
    def default_response_format(self, value:str):
        validator.validate(value, str)
        if value not in response_formats.list_all_formats():
            raise argument_exception("Некорректно указан тип формата!")
        
        self.__default_response_format = value


