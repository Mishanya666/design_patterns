from Src.Models.settings_model import settings_model
from Src.Core.validator import validator, argument_exception, operation_exception
import json
import os

class settings_manager:
    def __init__(self):
        self.__settings = settings_model()
        self.__file_name = ""

    @property
    def settings(self):
        return self.__settings

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, value):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__file_name = full_file_name
        else:
            raise argument_exception(f"Файл {value} не найден!")

    def load(self):
        if not self.__file_name:
            raise operation_exception("Не указан файл настроек!")

        try:
            with open(self.__file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.__settings.response_format = data.get("response_format", "Json")
                return True
        except json.JSONDecodeError as e:
            raise operation_exception(f"Ошибка декодирования JSON: {str(e)}")
        except UnicodeDecodeError as e:
            raise operation_exception(f"Ошибка кодировки при чтении файла: {str(e)}")
        except Exception as e:
            raise operation_exception(f"Не удалось загрузить настройки: {str(e)}")