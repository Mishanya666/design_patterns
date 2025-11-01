import os
import unittest

from Src.Logics.data_persistence import data_persistence


class TestDataPersistence(unittest.TestCase):
    def test_save_to_json(self):
        persistence = data_persistence("generated_data/test_data.json")
        self.assertTrue(persistence.save())
        self.assertTrue(os.path.exists("generated_data/test_data.json"))