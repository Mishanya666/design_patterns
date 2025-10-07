import unittest
from Src.start_service import start_service
from Src.storage_reposity import storage_reposity

class TestStartService(unittest.TestCase):

    def setUp(self):
        # Получаем singletone и генерируем данные заново
        self.service = start_service()
        # для idempotency очистим репозиторий и пересоздадим
        self.service._start_service__repo = storage_reposity()
        self.service.create()

    def test_ranges_exist(self):
        data = self.service.data()
        ranges = data.get(storage_reposity.range_key(), [])
        self.assertTrue(len(ranges) >= 1, "Единицы измерения должны быть сгенерированы")

    def test_groups_exist(self):
        data = self.service.data()
        groups = data.get(storage_reposity.group_key(), [])
        self.assertTrue(len(groups) >= 1, "Группы должны быть сгенерированы")

    def test_nomenclature_exist(self):
        data = self.service.data()
        noms = data.get(storage_reposity.nomenclature_key(), [])
        self.assertTrue(len(noms) >= 1, "Номенклатура должна быть сгенерирована")

    def test_receipts_exist(self):
        data = self.service.data()
        receipts = data.get(storage_reposity.receipts_key(), [])
        self.assertTrue(len(receipts) >= 1, "Рецепты должны быть сгенерированы")

if __name__ == "__main__":
    unittest.main()
