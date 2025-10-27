import unittest
from datetime import datetime
from Src.Logics.basic_converter import basic_converter
from Src.Logics.datetime_converter import datetime_converter
from Src.Logics.reference_converter import reference_converter
from Src.Models.range_model import range_model  # Пример существующей модели для теста

class TestConverters(unittest.TestCase):
    def test_basic_converter_simple_types(self):
        converter = basic_converter()
        self.assertEqual(converter.convert(42), {'value': 42})
        self.assertEqual(converter.convert(3.14), {'value': 3.14})
        self.assertEqual(converter.convert("test"), {'value': "test"})
        self.assertEqual(converter.convert(True), {'value': True})

    def test_datetime_converter(self):
        converter = datetime_converter()
        dt = datetime(2023, 10, 23, 12, 0, 0)
        self.assertEqual(converter.convert(dt), {'isoformat': '2023-10-23T12:00:00'})

    def test_reference_converter_composite(self):
        converter = reference_converter()
        obj = range_model("kg")  
        result = converter.convert(obj)
        self.assertIn('name', result)
        self.assertEqual(result['name'], {'value': 'kg'})

if __name__ == '__main__':
    unittest.main()