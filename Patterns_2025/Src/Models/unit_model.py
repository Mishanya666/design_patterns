from Src.Models.abstract_reference import abstract_reference
from Src.exceptions import argument_exception

class unit_model(abstract_reference):
    def __init__(self, name: str, coefficient: float = 1.0, base_unit=None):
        super().__init__(name)
        if coefficient <= 0:
            raise argument_exception("Коэффициент должен быть положительным")
        self._coefficient = coefficient
        self._base_unit = base_unit or self  # Если нет базовой, то сама себе базовая

    @property
    def coefficient(self) -> float:
        return self._coefficient

    @property
    def base_unit(self):
        return self._base_unit