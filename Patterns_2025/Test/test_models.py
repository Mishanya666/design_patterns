import sys
import os
import unittest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, project_root)

from Src.settings_manager import settings_manager
from Src.Models.abstract_reference import abstract_reference
from Src.Models.organization_model import organization_model
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.exceptions import argument_exception, operation_exception

class test_models(unittest.TestCase):

    def test_abstract_reference_name_limit(self):
        with self.assertRaises(argument_exception):
            abstract_reference("a" * 51)  # >50

        model = abstract_reference("Valid name")
        self.assertEqual(model.name, "Valid name")

    def test_organization_model_create_with_settings(self):
        manager = settings_manager()
        manager.open(os.path.join(project_root, "settings.json"))
        org = organization_model(manager.settings)
        self.assertEqual(org.name, "Рога и копыта")
        self.assertEqual(len(org.inn), 12)  # Проверяем валидацию

    def test_organization_model_create_without_settings(self):
        org = organization_model()
        self.assertEqual(org.name, "Default Org")
        with self.assertRaises(argument_exception):
            org.inn = "invalid"  # Не 12 символов

    def test_load_settings_and_create_organization(self):
        manager = settings_manager()
        manager.open(os.path.join(project_root, "settings.json"))
        org = organization_model(manager.settings)
        self.assertIsInstance(org, organization_model)
        self.assertEqual(org.name, manager.settings.name)

    def test_unit_model_create_base(self):
        base_unit = unit_model("грамм", 1.0)
        self.assertEqual(base_unit.coefficient, 1.0)
        self.assertEqual(base_unit.base_unit, base_unit)

    def test_unit_model_create_derived(self):
        base_unit = unit_model("грамм", 1.0)
        kg_unit = unit_model("кг", 1000.0, base_unit)
        self.assertEqual(kg_unit.coefficient, 1000.0)
        self.assertEqual(kg_unit.base_unit, base_unit)

    def test_unit_model_invalid_coefficient(self):
        with self.assertRaises(argument_exception):
            unit_model("invalid", -1.0)  # Отрицательный коэффициент

    def test_nomenclature_group_model_create(self):
        group = nomenclature_group_model("Группа1")
        self.assertEqual(group.name, "Группа1")

    def test_nomenclature_model_create_full(self):
        group = nomenclature_group_model("Группа")
        unit = unit_model("шт", 1.0)
        full_desc = "Полное наименование " * 10
        nom = nomenclature_model("Товар", full_desc, group, unit)
        self.assertEqual(nom.full_name, full_desc.strip())  # Добавьте .strip() для совпадения
        self.assertEqual(nom.group, group)
        self.assertEqual(nom.unit, unit)

    def test_nomenclature_model_full_name_limit(self):
        with self.assertRaises(argument_exception):
            nomenclature_model("Товар", "a" * 256)  # >255

    def test_storage_model_create(self):
        storage = storage_model("Склад1")
        self.assertEqual(storage.name, "Склад1")

    def test_all_models_variations(self):
        org_min = organization_model()
        unit_min = unit_model("мин")
        group_min = nomenclature_group_model("мин")
        nom_min = nomenclature_model("мин")
        storage_min = storage_model("мин")
        self.assertIsInstance(org_min, organization_model)
        self.assertIsInstance(unit_min, unit_model)

        # Вариант 2: Полные параметры
        base_unit = unit_model("base", 1.0)
        derived_unit = unit_model("derived", 2.0, base_unit)
        group = nomenclature_group_model("full group")
        nom_full = nomenclature_model("full nom", "full desc", group, derived_unit)
        self.assertEqual(nom_full.unit.base_unit, base_unit)

if __name__ == '__main__':
    unittest.main()