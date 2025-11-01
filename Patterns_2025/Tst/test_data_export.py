import unittest
import os
import json
from Src.start_service import start_service
from Src.Logics.data_persistence import data_persistence


class TestDataExport(unittest.TestCase):
    def test_auto_generate_data_json(self):
        # 1. Загружаем данные
        service = start_service()
        service.file_name = "settings.json"
        service.start()

        # 2. Сохраняем
        file_path = "generated_data/data.json"
        persistence = data_persistence(file_path)
        self.assertTrue(persistence.save())

        # 3. Проверяем существование и содержимое
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertIn("nomenclature_model", data)
        self.assertIn("range_model", data)
        self.assertGreater(len(data["nomenclature_model"]), 0)

        print(f"Сгенерирован файл: {file_path}")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:500] + "...")


if __name__ == '__main__':
    unittest.main()