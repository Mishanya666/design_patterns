import json
import os
from Src.reposity import reposity
from Src.Logics.convert_factory import convert_factory

class data_persistence:
    """
    Класс для сохранения данных репозитория в JSON.
    """
    def __init__(self, file_path: str = "data.json"):
        self.file_path = file_path
        self.repo = reposity()
        self.converter = convert_factory()

    def save(self) -> bool:
        """
        Сохраняет все данные репозитория в JSON.
        """
        try:
            data_to_save = {}
            for key in reposity.keys():
                items = self.repo.data.get(key, [])
                data_to_save[key] = self.converter.convert(items)

            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False, default=str)
            return True
        except Exception:
            return False