class reposity:
    def __init__(self):
        # Словарь списков, ключ — строка
        self.__data = {}

    @property
    def data(self):
        return self.__data

    @staticmethod
    def range_key():
        return "range_model"

    @staticmethod
    def group_key():
        return "group_model"

    @staticmethod
    def nomenclature_key():
        return "nomenclature_model"

    @staticmethod
    def receipts_key():
        return "receipt_model"
