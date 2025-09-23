from Src.settings_manager import settings_manager
from Src.Models.company_model import settings
import unittest
import os

class test_models(unittest.TestCase):

    def test_empty_createmodel_settings(self):

        model = settings()

        assert model.name == ""


    def test_notEmpty_createmodel_settings(self):

        model = settings()

        model.name = "test"

        assert model.name != ""

    def test_load_createmodel_settings(self):

        file_name = "C:/Users/dacko/OneDrive/Документы/GitHub/design_patterns/Patterns_2025/settings.json"
        manager = settings_manager()
        manager.file_name = file_name

        result = manager.load()

        assert result == True

    def test_loadCombo_createmodel_settings(self):

        file_name = "C:/Users/dacko/OneDrive/Документы/GitHub/design_patterns/Patterns_2025/settings.json"
        manager1 = settings_manager()
        manager1.file_name = file_name
        manager2 = settings_manager()

        manager1.load()

        # Проверки
        assert manager1.settings == manager2.settings

    def test_convert_load_all_properties(self):
        data = {
            "name": "Test Company",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "12345678901",
            "bik": "123456789",
            "ownership_type": "ABCDE"
        }
        manager = settings_manager()

        model = manager.convert(data)

        assert model.name == "Test Company"
        assert model.inn == "123456789012"
        assert model.account == "12345678901"
        assert model.corr_account == "12345678901"
        assert model.bik == "123456789"
        assert model.ownership_type == "ABCDE"


    def test_invalid_inn_length(self):
        model = settings()
        with self.assertRaises(ValueError):
            model.inn = "123"

    def test_invalid_account_length(self):
        model = settings()
        with self.assertRaises(ValueError):
            model.account = "123"

    def test_invalid_corr_account_length(self):
        model = settings()
        with self.assertRaises(ValueError):
            model.corr_account = "123"

    def test_invalid_bik_length(self):
        model = settings()
        with self.assertRaises(ValueError):
            model.bik = "123"

    def test_invalid_ownership_type_length(self):
        model = settings()
        with self.assertRaises(ValueError):
            model.ownership_type = "123"
  
if __name__ == '__main__':
    unittest.main()   