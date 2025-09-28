from Src.Models.organization_model import organization_model
import os
import json
from Src.exceptions import operation_exception

class settings_manager:
    __instance = None
    __file_name: str = ""
    __settings: organization_model = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(settings_manager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.set_default()

    @property
    def settings(self):
        return self.__settings

    def open(self, file_name: str):
        self.file_name = file_name
        self.load()

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        absolute_path = os.path.abspath(value.strip())
        if not os.path.exists(absolute_path):
            raise operation_exception("Файл настроек не найден")
        self.__file_name = absolute_path

    def load(self) -> bool:
        try:
            with open(self.__file_name, 'r') as f:
                data = json.load(f)
            if "company" in data:
                item = data["company"]
                self.__settings = organization_model()
                self.__settings.name = item.get("name", "")
                self.__settings.inn = item.get("inn", "")
                self.__settings.bik = item.get("bik", "")
                self.__settings.account = item.get("account", "")
                self.__settings.ownership_type = item.get("ownership_type", "")
                return True
            return False
        except Exception as e:
            raise operation_exception(f"Ошибка загрузки: {str(e)}")

    def set_default(self):
        self.__settings = organization_model()
        self.__settings.name = "Рога и копыта"