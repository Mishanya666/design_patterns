import unittest
from Src.start_service import start_service
from Src.Logics.factory_entities import factory_entities
from Src.Logics.response_csv import response_csv
from Src.Logics.response_markdown import response_markdown
from Src.Logics.response_json import response_json
from Src.Logics.response_xml import response_xml
from Src.reposity import reposity
import os
import json

class test_response_formats(unittest.TestCase):
    def setUp(self):
        self.start = start_service()
        self.start.start()
        self.repo = self.start.data
        self.factory = factory_entities()

    def test_csv_format(self):
        logic = self.factory.create("CSV")
        data = self.repo[reposity.nomenclature_key()]
        result = logic.build("CSV", data)
        self.assertIn("name,group,range,unique_code", result)
        self.assertGreater(len(result.splitlines()), 1)

    def test_markdown_format(self):
        logic = self.factory.create("Markdown")
        data = self.repo[reposity.range_key()]
        result = logic.build("Markdown", data)
        self.assertIn("| name | base | value | unique_code |", result)
        self.assertIn("Грамм", result)

    def test_json_format(self):
        logic = self.factory.create("Json")
        data = self.repo[reposity.group_key()]
        result = logic.build("Json", data)
        parsed = json.loads(result)
        self.assertIsInstance(parsed, list)
        self.assertGreater(len(parsed), 0)
        self.assertIn("name", parsed[0])

    def test_xml_format(self):
        logic = self.factory.create("XML")
        data = self.repo[reposity.receipt_key()]
        result = logic.build("XML", data)
        self.assertIn("<items>", result)
        self.assertIn("<name>ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ</name>", result)

    def test_create_default(self):
        logic = self.factory.create_default()
        self.assertIsInstance(logic, response_csv)

    def test_generate_files(self):
        formats = ["CSV", "Markdown", "Json", "XML"]
        types = {
            "nomenclature": reposity.nomenclature_key(),
            "range": reposity.range_key(),
            "group": reposity.group_key(),
            "receipt": reposity.receipt_key()
        }

        for fmt in formats:
            logic = self.factory.create(fmt)
            for typ, key in types.items():
                data = self.repo[key]
                content = logic.build(fmt, data)
                file_ext = "md" if fmt == "Markdown" else fmt.lower()
                file_name = f"output/{typ}.{file_ext}"
                os.makedirs(os.path.dirname(file_name), exist_ok=True)
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(content)
                self.assertTrue(os.path.exists(file_name))

if __name__ == '__main__':
    unittest.main()