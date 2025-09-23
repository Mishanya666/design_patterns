class settings:
    __name: str = ""
    __inn: str = ""
    __account: str = ""
    __corr_account: str = ""
    __bik: str = ""
    __ownership_type: str = ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if value.strip() != "":
            self.__name = value.strip()

    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        value = value.strip()
        if len(value) != 12:
            raise ValueError("ИНН должен состоять из 12 символов")
        self.__inn = value

    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value: str):
        value = value.strip()
        if len(value) != 11:
            raise ValueError("Счет должен состоять из 11 символов")
        self.__account = value

    @property
    def corr_account(self) -> str:
        return self.__corr_account

    @corr_account.setter
    def corr_account(self, value: str):
        value = value.strip()
        if len(value) != 11:
            raise ValueError("Корреспондентский счет должен состоять из 11 символов")
        self.__corr_account = value

    @property
    def bik(self) -> str:
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        value = value.strip()
        if len(value) != 9:
            raise ValueError("БИК должен состоять из 9 символов")
        self.__bik = value

    @property
    def ownership_type(self) -> str:
        return self.__ownership_type

    @ownership_type.setter
    def ownership_type(self, value: str):
        value = value.strip()
        if len(value) != 5:
            raise ValueError("Вид собственности должен состоять из 5 символов")
        self.__ownership_type = value