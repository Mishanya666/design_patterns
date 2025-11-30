from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.reposity_manager import reposity_manager
from Src.Core.validator import operation_exception


class reference_dependency_checker(abstract_logic):
    """
    Сервис проверяет — можно ли удалять справочник.
    Использует Observer: другие модули могут подписаться и добавить свои проверки.
    """

    def __init__(self):
        super().__init__()
        observe_service.add(self)

    def can_delete(self, ref_type: str, item_id: str) -> bool:
        """
        Запускаем проверку — можно ли удалить.
        Вместо прямого доступа — кидаем событие!
        """
        # Создаём событие: "проверяем, можно ли удалить"
        result = {"can_delete": True, "reason": ""}

        observe_service.create_event(
            f"check_can_delete_{ref_type}",
            {"item_id": item_id, "result": result}
        )

        return result["can_delete"]

    def handle(self, event: str, params):
        if not event.startswith("check_can_delete_"):
            return

        ref_type = event.split("_")[-1]  # nomenclature, range и т.д.
        item_id = params["item_id"]
        result_container = params["result"]

        if ref_type == "nomenclature":
            repo = reposity_manager()
            transactions = repo.data.get("transaction", [])
            for t in transactions:
                if hasattr(t, "nomenclature_id") and str(t.nomenclature_id) == str(item_id):
                    result_container["can_delete"] = False
                    result_container["reason"] = "Номенклатура используется в оборотах"
                    return
