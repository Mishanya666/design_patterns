from enum import Enum
from Src.Models.company_model import company_model
from Src.Core.validator import validator, argument_exception


######################################
# Перечисление для форматов ответа
class ResponseFormat(Enum):
    CSV = "CSV"
    MARKDOWN = "Markdown"
    JSON = "Json"
    XML = "XML"

######################################
# Модель настроек приложения
class settings_model:
    __company: company_model = None
    __response_format: ResponseFormat = ResponseFormat.JSON

    @property
    def company(self) -> company_model:
        return self.__company

    @company.setter
    def company(self, value: company_model):
        validator.validate(value, company_model)
        self.__company = value

    @property
    def response_format(self) -> ResponseFormat:
        return self.__response_format

    @response_format.setter
    def response_format(self, value: ResponseFormat):
        validator.validate(value, ResponseFormat)
        self.__response_format = value

    def __init__(self):
        self.company = company_model()
        self.response_format = ResponseFormat.JSON
        self.first_start = True