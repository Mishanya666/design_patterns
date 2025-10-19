from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import validator, argument_exception, operation_exception
import os
import json
from Src.Models.receipt_model import receipt_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto

class start_service:
    # Репозиторий
    __repo: reposity = reposity()

    # Рецепт по умолчанию
    __default_receipt: receipt_model

    # Словарь для кэширования объектов
    __cache = {}

    # Наименование файла (полный путь)
    __full_file_name: str = ""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__repo.initalize()

    # Текущий файл
    @property
    def file_name(self) -> str:
        return self.__full_file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value: str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if not self.__full_file_name:
            raise operation_exception("Не указан файл настроек!")

        if not os.path.exists(self.__full_file_name):
            raise operation_exception(f"Файл {self.__full_file_name} не существует!")

        try:
            with open(self.__full_file_name, 'r', encoding='utf-8') as file_instance:
                settings = json.load(file_instance)

                if "default_receipt" not in settings:
                    raise operation_exception("Ключ 'default_receipt' отсутствует в settings.json!")

                data = settings["default_receipt"]
                result = self.convert(data)
                if not result:
                    raise operation_exception("Ошибка при конвертации данных из default_receipt!")
                return True

        except json.JSONDecodeError as e:
            raise operation_exception(f"Ошибка декодирования JSON: {str(e)}")
        except UnicodeDecodeError as e:
            raise operation_exception(f"Ошибка кодировки при чтении файла: {str(e)}")
        except Exception as e:
            raise operation_exception(f"Ошибка при загрузке настроек: {str(e)}")

    # Сохранить элемент в репозитории
    def __save_item(self, key: str, dto, item):
        validator.validate(key, str)
        item.unique_code = dto.id
        self.__cache[dto.id] = item
        self.__repo.data[key].append(item)

    # Загрузить единицы измерений
    def __convert_ranges(self, data: dict) -> bool:
        validator.validate(data, dict)
        ranges = data.get('ranges', [])
        if not ranges:
            return False

        try:
            for range_data in ranges:
                dto = range_dto().create(range_data)
                item = range_model.from_dto(dto, self.__cache)
                self.__save_item(reposity.range_key(), dto, item)

            # Установить базовые единицы измерения
            for range_data in ranges:
                if range_data.get("base_id"):
                    item = self.__cache.get(range_data["id"])
                    if item and range_data["base_id"] in self.__cache:
                        item.base = self.__cache[range_data["base_id"]]
            return True
        except Exception as e:
            raise operation_exception(f"Ошибка при загрузке единиц измерения: {str(e)}")

    # Загрузить группы номенклатуры
    def __convert_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        categories = data.get('categories', [])
        if not categories:
            return False

        try:
            for category in categories:
                dto = category_dto().create(category)
                item = group_model.from_dto(dto, self.__cache)
                self.__save_item(reposity.group_key(), dto, item)
            return True
        except Exception as e:
            raise operation_exception(f"Ошибка при загрузке групп: {str(e)}")

    # Загрузить номенклатуру
    def __convert_nomenclatures(self, data: dict) -> bool:
        validator.validate(data, dict)
        nomenclatures = data.get('nomenclatures', [])
        if not nomenclatures:
            return False

        try:
            for nomenclature in nomenclatures:
                dto = nomenclature_dto().create(nomenclature)
                item = nomenclature_model.from_dto(dto, self.__cache)
                self.__save_item(reposity.nomenclature_key(), dto, item)
            return True
        except Exception as e:
            raise operation_exception(f"Ошибка при загрузке номенклатуры: {str(e)}")

    # Обработать полученный словарь
    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)

        try:
            # Создаем рецепт
            cooking_time = data.get('cooking_time', "")
            portions = int(data.get('portions', 0))
            name = data.get('name', "НЕ ИЗВЕСТНО")
            self.__default_receipt = receipt_model.create(name, cooking_time, portions)

            # Загружаем шаги приготовления
            steps = data.get('steps', [])
            for step in steps:
                if step.strip():
                    self.__default_receipt.steps.append(step)

            # Загружаем единицы измерения, группы и номенклатуру
            if not self.__convert_ranges(data):
                return False
            if not self.__convert_groups(data):
                return False
            if not self.__convert_nomenclatures(data):
                return False

            # Собираем состав рецепта
            compositions = data.get('composition', [])
            for composition in compositions:
                nomenclature_id = composition.get('nomenclature_id', "")
                range_id = composition.get('range_id', "")
                value = composition.get('value', 0)
                nomenclature = self.__cache.get(nomenclature_id)
                range_item = self.__cache.get(range_id)
                if not nomenclature or not range_item:
                    raise operation_exception(
                        f"Ошибка: Не найдены объекты для nomenclature_id={nomenclature_id} или range_id={range_id}. "
                        f"Доступные ключи в кэше: {list(self.__cache.keys())}"
                    )
                item = receipt_item_model.create(nomenclature, range_item, value)
                self.__default_receipt.composition.append(item)

            # Сохраняем рецепт
            self.__repo.data[reposity.receipt_key()].append(self.__default_receipt)
            return True

        except Exception as e:
            raise operation_exception(f"Ошибка при конвертации данных: {str(e)}")

    @property
    def data(self):
        return self.__repo.data

    def start(self):
        self.file_name = "settings.json"
        if not self.load():
            raise operation_exception("Невозможно сформировать стартовый набор данных!")