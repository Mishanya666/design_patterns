from Src.Core.validator import validator, argument_exception


class storage_model:
    """
    Модель склада.
    """

    def __init__(self, name: str):
        """
        :param name: Наименование склада.
        """

        validator.validate(name, str)
        if not name.strip():
            raise argument_exception("Наименование склада не может быть пустым!")

        self.name = name
        self.unique_code = f"STORAGE_{hash(name)}"