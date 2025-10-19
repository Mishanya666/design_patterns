import unittest

from Src.Core import response_format
from Src.Logics.response_csv import response_csv  # Corrected from response_scv
from Src.Models.group_model import group_model
from Src.Logics.factory_entities import factory_entities
from Src.Core.response_format import response_formats
from Src.Core.validator import validator
from Src.Core.abstract_response import abstract_response
from Src.start_service import start_service
from main import factory


# Тесты для проверки логики
class test_logics(unittest.TestCase):

    # Проверим формирование CSV
    def test_notNone_response_csv_build(self):  # Updated method name for clarity
        # Подготовка
        response = response_csv()
        data = []
        entity = group_model.create("test")
        data.append(entity)

        # Действие
        result = response.build("CSV", data)

        # Проверка
        self.assertIsNotNone(result)

    def setUp(self):
        self.service = start_service()
        self.service.start()
        self.factory = factory_entities()

    def test_notNone_factory_create(self):
        formats = ["CSV", "Json", "Markdown", "XML"]
        for fmt in formats:
            instance = self.factory.create(fmt)
            validator.validate(instance, response_format)
            data = self.service.data[fmt.lower() + "_key"]()
            text = instance.build(fmt, data)
            self.assertGreater(len(text), 0, f"Формат {fmt} вернул пустую строку")

        # Действие
        logic = factory.create("CSV")  # Use string directly for simplicity

        # Проверка
        self.assertIsNotNone(logic)
        instance = logic  # No need for eval, as create returns instance
        validator.validate(instance, abstract_response)
        text = instance.build("CSV", data)
        self.assertGreater(len(text), 0)

if __name__ == '__main__':
    unittest.main()