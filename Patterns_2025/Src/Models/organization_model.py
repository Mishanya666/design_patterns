from Src.Models.abstract_reference import abstract_reference
from Src.exceptions import argument_exception, operation_exception

class organization_model(abstract_reference):
    def __init__(self, settings=None, name: str = ""):
        super().__init__(name or (settings.name if settings else "Default Org"))
        self._inn = ""
        self._bik = ""
        self._account = ""
        self._ownership_type = ""

        if settings:
            try:
                self.inn = settings.inn
                self.bik = settings.bik
                self.account = settings.account
                self.ownership_type = settings.ownership_type
            except Exception as e:
                raise operation_exception(f"Ошибка копирования настроек: {str(e)}")

    @property
    def inn(self) -> str:
        return self._inn

    @inn.setter
    def inn(self, value: str):
        value = value.strip()
        if len(value) != 12:
            raise argument_exception("ИНН должен быть 12 символов")
        self._inn = value

    @property
    def bik(self) -> str:
        return self._bik

    @bik.setter
    def bik(self, value: str):
        value = value.strip()
        if len(value) != 9:
            raise argument_exception("БИК должен быть 9 символов")
        self._bik = value

    @property
    def account(self) -> str:
        return self._account

    @account.setter
    def account(self, value: str):
        value = value.strip()
        if len(value) != 11:
            raise argument_exception("Счет должен быть 11 символов")
        self._account = value

    @property
    def ownership_type(self) -> str:
        return self._ownership_type

    @ownership_type.setter
    def ownership_type(self, value: str):
        value = value.strip()
        if len(value) != 5:
            raise argument_exception("Форма собственности должна быть 5 символов")
        self._ownership_type = value