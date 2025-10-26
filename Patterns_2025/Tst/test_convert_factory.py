import unittest
from datetime import datetime
from Src.Logics.convert_factory import convert_factory
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model

class TestConvertFactory(unittest.TestCase):
    def test_convert_factory_simple(self):
        factory = convert_factory()
        self.assertEqual(factory.convert(42), {'value': 42})
        dt = datetime(2023, 10, 23)
        self.assertEqual(factory.convert(dt), {'isoformat': '2023-10-23T00:00:00'})

    def test_convert_factory_composite(self):
        factory = convert_factory()
        group = group_model("Fruits")
        range_ = range_model("kg")
        nom = nomenclature_model("Apple", group, range_)
        result = factory.convert(nom)
        self.assertIn('name', result)
        self.assertEqual(result['name'], {'value': 'Apple'})
        self.assertIn('group', result)
        self.assertEqual(result['group']['name'], {'value': 'Fruits'})

    def test_convert_factory_list(self):
        factory = convert_factory()
        items = [42, "test"]
        result = factory.convert(items)
        self.assertEqual(result, [{'value': 42}, {'value': "test"}])

if __name__ == '__main__':
    unittest.main()