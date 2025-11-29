from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Core.validator import validator, operation_exception
from Src.reposity_manager import reposity_manager
from Src.Core.common import common
from Src.Logics.convert_factory import convert_factory
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto
from Src.Models.settings_model import settings_model
from Src.settings_manager import settings_manager
import uuid
import json
from datetime import datetime


class reference_service(abstract_logic):
    """
    CRUD-сервис для справочников с использованием паттерна Прототип
    и пост-обработкой через Observer
    """

    # Прототипы для клонирования / создания объектов
    _prototypes = {
        "nomenclature": nomenclature_dto,
        "range": range_dto,
        "category": category_dto,
        "storage": storage_dto
    }

    def __init__(self):
        super().__init__()
        observe_service.add(self)  # Подписываемся на события (на будущее)

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

    @staticmethod
    def _save_settings():
        """Сохранить настройки в appsettings.json после изменений"""
        try:
            settings = settings_manager().settings
            data = {
                "company": {
                    "name": settings.company.name,
                    "inn": settings.company.inn
                },
                "default_format": settings.default_response_format,
                "block_period": settings.block_period.strftime("%Y-%m-%d") if settings.block_period else None
            }
            with open("appsettings.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def _can_delete(self, ref_type: str, item_id: str) -> bool:
        """Проверка: можно ли удалить (есть ли зависимости)"""
        repo = reposity_manager()

        if ref_type == "nomenclature":
            transactions = repo.data.get("transaction", [])
            for t in transactions:
                if hasattr(t, "nomenclature_id") and str(t.nomenclature_id) == item_id:
                    return False

        return True


    def add(self, ref_type: str, data: dict):
        validator.validate(ref_type, str)
        validator.validate(data, dict)

        if ref_type not in self._prototypes:
            self.set_exception(operation_exception("Неподдерживаемый тип справочника"))
            return None

        prototype_class = self._prototypes[ref_type]
        prototype = prototype_class()

        new_item = prototype.create(data.copy())
        if new_item.is_error:
            self.set_exception(operation_exception(new_item.error_text))
            return None

        # Генерируем ID
        new_item.id = str(uuid.uuid4())

        # Добавляем в репозиторий
        repo_key = self._get_repo_key(ref_type)
        repo = reposity_manager()
        items = repo.data.get(repo_key, [])
        items.append(new_item)
        repo.data[repo_key] = items

        # Сохраняем настройки + уведомляем
        self._save_settings()
        observe_service.create_event(f"{ref_type}_created", convert_factory().serialize(new_item))

        return convert_factory().serialize(new_item)

    def update(self, ref_type: str, item_id: str, data: dict):
        validator.validate(ref_type, str)
        validator.validate(item_id, str)
        validator.validate(data, dict)

        repo_key = self._get_repo_key(ref_type)
        repo = reposity_manager()
        items = repo.data.get(repo_key, [])

        item = next((x for x in items if str(x.id) == item_id), None)
        if not item:
            self.set_exception(operation_exception("Элемент не найден"))
            return None

        prototype_class = self._prototypes[ref_type]
        updated_item = prototype_class().create(data.copy())
        if updated_item.is_error:
            self.set_exception(operation_exception(updated_item.error_text))
            return None

        updated_item.id = item_id  # Сохраняем ID

        index = items.index(item)
        items[index] = updated_item

        self._save_settings()
        observe_service.create_event(f"{ref_type}_updated", {
            "old": convert_factory().serialize(item),
            "new": convert_factory().serialize(updated_item)
        })

        # Пересчёт остатков при изменении номенклатуры
        if ref_type == "nomenclature":
            observe_service.create_event("recalculate_rests", {"item_id": item_id})

        return convert_factory().serialize(updated_item)

    def delete(self, ref_type: str, item_id: str) -> bool:
        validator.validate(ref_type, str)
        validator.validate(item_id, str)

        if not self._can_delete(ref_type, item_id):
            self.set_exception(operation_exception("Удаление запрещено: есть зависимости в оборотах или рецептах"))
            return False

        repo_key = self._get_repo_key(ref_type)
        repo = reposity_manager()
        items = repo.data.get(repo_key, [])

        item = next((x for x in items if str(x.id) == item_id), None)
        if not item:
            self.set_exception(operation_exception("Элемент не найден"))
            return False

        repo.data[repo_key] = [x for x in items if str(x.id) != item_id]

        self._save_settings()
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
