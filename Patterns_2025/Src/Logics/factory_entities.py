from Src.Core.abstract_response import abstract_response
from Src.Logics.response_csv import response_scv
from Src.Core.validator import operation_exception
from Src.settings_manager import settings_manager
from Src.Logics.response_json import response_json
from Src.Logics.response_xml import response_xml
from Src.Core.validator import operation_exception
from Src.Logics.response_markdown import response_markdown

class factory_entities:
    __match = {
        "csv":  response_scv,
        "Markdown": response_markdown,
        "Json": response_json,
        "XML": response_xml
    }

    # Получить нужный тип
    def create(self, format:str) -> abstract_response:
        if format not in self.__match.keys():
            raise operation_exception("Формат не верный")

        return self.__match[  format ]

    # Создать ответ в формате по умолчанию из настроек
    def create_default(self) -> abstract_response:
        format = self.__settings.settings.response_format
        if format not in self.__match.keys():
            raise operation_exception(f"Формат по умолчанию {format} не поддерживается!")
        return self.__match[format]()

