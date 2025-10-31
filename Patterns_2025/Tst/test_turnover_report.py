import sys
import os
import unittest
from datetime import date
import matplotlib.pyplot as plt

# Добавляем корень проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Src.reposity import reposity
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
from Src.Logics.turnover_report import turnover_report
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


class TestTurnoverReport(unittest.TestCase):

    def setUp(self):
        self.repo = reposity()
        self.repo.initalize()

        self.storage1 = storage_model("Склад 1")

        # Единица измерения
        self.unit_kg = range_model.__new__(range_model)
        self.unit_kg.name = "kg"
        self.unit_kg._abstact_model__unique_code = "RANGE_KG"

        # Номенклатура
        self.nom1 = nomenclature_model.__new__(nomenclature_model)
        self.nom1.name = "Яблоко"
        self.nom1.base_unit = "kg"
        self.nom1._abstact_model__unique_code = "NOM_APPLE"

        self.nom2 = nomenclature_model.__new__(nomenclature_model)
        self.nom2.name = "Банан"
        self.nom2.base_unit = "kg"
        self.nom2._abstact_model__unique_code = "NOM_BANANA"

        # Репозиторий
        self.repo.data[reposity.nomenclature_key()] = [self.nom1, self.nom2]
        self.repo.data[reposity.range_key()] = [self.unit_kg]
        self.repo.data[reposity.storage_key()] = [self.storage1]

        # Транзакции
        self.repo.data[reposity.transaction_key()] = [
            transaction_model(date(2025, 10, 1), "TX1", self.nom1, self.storage1, 100.0, self.unit_kg),
            transaction_model(date(2025, 10, 2), "TX2", self.nom1, self.storage1, -20.0, self.unit_kg),
            transaction_model(date(2025, 9, 30), "TX0", self.nom1, self.storage1, 10.0, self.unit_kg),
        ]

    def test_generate_image(self):
        report = turnover_report.generate(
            start_date=date(2025, 10, 1),
            end_date=date(2025, 10, 31),
            storage_code=self.storage1.unique_code
        )

        os.makedirs("generated_data", exist_ok=True)

        fig, ax = plt.subplots(figsize=(15, len(report) * 0.8 + 2))
        ax.axis('off')

        headers = ["Номенклатура", "Ед.изм.", "Нач. остаток", "Приход", "Расход", "Кон. остаток"]
        table_data = [[
            r.get("nomenclature", "—"),
            r.get("unit", "—"),
            f"{r.get('initial_balance', 0):.2f}",
            f"{r.get('income', 0):.2f}",
            f"{r.get('expense', 0):.2f}",
            f"{r.get('final_balance', 0):.2f}"
        ] for r in report]

        table = ax.table(cellText=table_data, colLabels=headers, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.3, 2.5)

        plt.suptitle("Оборотно-сальдовая ведомость (ОСВ)", fontsize=16, y=0.98)
        plt.tight_layout()
        path = 'generated_data/osv_report.png'
        plt.savefig(path, bbox_inches='tight', dpi=200)
        plt.close(fig)

        self.assertTrue(os.path.exists(path))
        print(f"\nГОТОВО! Картинка ОСВ сохранена: {path}")


if __name__ == '__main__':
    unittest.main()