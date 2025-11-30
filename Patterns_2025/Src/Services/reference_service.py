# Src/Services/reference_service.py
from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core.validator import validator, operation_exception
from Src.reposity_manager import reposity_manager
from Src.Logics.convert_factory import convert_factory
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto
from Src.Services.reference_dependency_checker import reference_dependency_checker
import uuid


class reference_service(abstract_logic):
    """
    CRUD-сервис для справочников.
    Использует:
    - Паттерн Прототип (через DTO.create())
    - Паттерн Наблюдатель (события: *_created, *_updated, *_deleted, recalculate_rests)
    - SRP: не сохраняет файлы, не проверяет зависимости напрямую
    """

    _prototypes = {
        "nomenclature": nomenclature_dto,
        "range": range_dto,
        "category": category_dto,
        "storage": storage_dto
    }

    def __init__(self):
        super().__init__()

    # region === Вспомогательные методы ===

    @staticmethod
    def _get_repo_key(ref_type: str) -> str:
        mapping = {
            "nomenclature": reposity_manager.nomenclature_key(),
            "range": reposity_manager.range_key(),
            "category": reposity_manager.category_key(),
            "storage": reposity_manager.storage_key(),
        }
        if ref_type not in mapping:
            raise operation_exception(f"Неизвестный тип справочника: {ref_type}")
        return mapping[ref_type]

    # endregion

    # region === CRUD методы ===

    def add(self, ref_type: str, data: dict):
        validator.validate(ref_type, str)
        validator.validate(data, dict)

        if ref_type not in self._prototypes:
            self.set_exception(operation_exception("Неподдерживаемый тип справочника"))
            return None

        prototype_class = self._prototypes[ref_type]
        new_item = prototype_class().create(data.copy())
        if new_item.is_error:
            self.set_exception(operation_exception(new_item.error_text))
            return None

        new_item.id = str(uuid.uuid4())

        repo_key = self._get_repo_key(ref_type)
        repo = reposity_manager()
        items = repo.data.get(repo_key, [])
        items.append(new_item)
        repo.data[repo_key] = items

        # Уведомляем всех наблюдателей
        serialized = convert_factory().serialize(new_item)
        observe_service.create_event(f"{ref_type}_created", serialized)

        return serialized

    def update(self, ref_type: str, item_id: str, data: dict):
        validator.validate(ref_type, str)
        validator.validate(item_id, str)
        validator.validate(data, dict)

        repo_key = self._get_repo_key(ref_type)
        repo = reposity_manager()
        items = repo.data.get(repo_key, [])

        old_item = next((x for x in items if str(x.id) == item_id), None)
        if not old_item:
            self.set_exception(operation_exception("Элемент не найден"))
            return None

        prototype_class = self._prototypes[ref_type]
        updated_item = prototype_class().create(data.copy())
        if updated_item.is_error:
            self.set_exception(operation_exception(updated_item.error_text))
            return None

        updated_item.id = item_id
        index = items.index(old_item)
        items[index] = updated_item

        old_serialized = convert_factory().serialize(old_item)
        new_serialized = convert_factory().serialize(updated_item)

        observe_service.create_event(f"{ref_type}_updated", {
            "old": old_serialized,
            "new": new_serialized
        })

        # При изменении номенклатуры — пересчёт остатков
        if ref_type == "nomenclature":
            observe_service.create_event("recalculate_rests", {"item_id": item_id})

        return new_serialized

    def delete(self, ref_type: str, item_id: str) -> bool:
        validator.validate(ref_type, str)
        validator.validate(item_id, str)

        # Проверка через Observer
        checker = reference_dependency_checker()
        if not checker.can_delete(ref_type, item_id):
            self.set_exception(operation_exception("Удаление запрещено: элемент используется"))
            return False

        repo_key = self._get_repo_key(ref_type)
        repo = reposity_manager()
        items = repo.data.get(repo_key, [])

        item = next((x for x in items if str(x.id) == item_id), None)
        if not item:
            self.set_exception(operation_exception("Элемент не найден"))
            return False

        # Удаляем
        repo.data[repo_key] = [x for x in items if str(x.id) != item_id]

        # Уведомляем наблюдателей
        observe_service.create_event(f"{ref_type}_deleted", convert_factory().serialize(item))

        return True

    def get_by_id(self, ref_type: str, item_id: str):
        repo_key = self._get_repo_key(ref_type)
        items = reposity_manager().data.get(repo_key, [])
        item = next((x for x in items if str(x.id) == item_id), None)
        return convert_factory().serialize(item) if item else None

    def get_all(self, ref_type: str):
        repo_key = self._get_repo_key(ref_type)
        items = reposity_manager().data.get(repo_key, [])
        return [convert_factory().serialize(x) for x in items]

    # endregion