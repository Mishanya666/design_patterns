from Src.Core.response_format import response_formats
from Src.Logics.response_csv import response_csv
from Src.Logics.response_json import response_json
from Src.Logics.response_markdown import response_markdown
from Src.Logics.response_xml import response_xml
from Src.Core.validator import operation_exception

class factory_entities:
    @staticmethod
    def create(format: str) -> response_formats:
        formats = {
            "CSV": response_csv(),
            "Json": response_json(),
            "Markdown": response_markdown(),
            "XML": response_xml()
        }
        if format not in formats:
            raise operation_exception(f"Формат {format} не поддерживается!")
        return formats[format]