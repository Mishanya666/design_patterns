from Src.Models.company_model import settings
import os
import json

class settings_manager:
    __file_name: str = ""
    __settings: settings = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance 
    
    def __init__(self):
        self.set_default()

    @property
    def settings(self) -> settings:
        return self.__settings

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        if value.strip() == "":
            return

        absolute_path = os.path.abspath(value.strip())
        if os.path.exists(absolute_path):
            self.__file_name = absolute_path
        else:
            raise Exception("Не найден файл настроек!")

    def convert(self, data: dict) -> settings:
        result = settings()
        if "name" in data:
            result.name = data["name"]
        if "inn" in data:
            result.inn = data["inn"]
        if "account" in data:
            result.account = data["account"]
        if "corr_account" in data:
            result.corr_account = data["corr_account"]
        if "bik" in data:
            result.bik = data["bik"]
        if "ownership_type" in data:
            result.ownership_type = data["ownership_type"]
        return result

    def load(self) -> bool:
        if self.__file_name.strip() == "":
            raise Exception("Не найден файл настроек!")

        try:
            with open(self.__file_name.strip(), 'r') as file_instance:
                data = json.load(file_instance)

                if "company" in data.keys():
                    item = data["company"]
                    self.__settings = self.convert(item)
                    return True

            return False
        except Exception as ex:
            print(ex)
            return False

    def set_default(self):
        self.__settings = settings()
        self.__settings.name = "Рога и копыта"