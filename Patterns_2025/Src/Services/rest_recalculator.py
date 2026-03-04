# Src/Services/rest_recalculator.py
from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service

class rest_recalculator(abstract_logic):
    """
    Сервис пересчёта остатков при изменении справочников
    """
    def __init__(self):
        super().__init__()
        observe_service.add(self)

    def handle(self, event: str, params):
        if event == "recalculate_rests":
            print(f"Пересчёт остатков по дате блокировки для номенклатуры {params.get('item_id')}...")

            pass