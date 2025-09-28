from Src.Models.abstract_reference import abstract_reference
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.unit_model import unit_model
from Src.exceptions import argument_exception

class nomenclature_model(abstract_reference):
    def __init__(self, name: str, full_name: str = "", group: nomenclature_group_model = None, unit: unit_model = None):
        super().__init__(name)
        full_name = full_name.strip()
        if len(full_name) > 255:
            raise argument_exception("Полное наименование не может превышать 255 символов")
        self._full_name = full_name
        self._group = group
        self._unit = unit

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def group(self) -> nomenclature_group_model:
        return self._group

    @property
    def unit(self) -> unit_model:
        return self._unit