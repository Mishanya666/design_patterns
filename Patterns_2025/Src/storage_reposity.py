from Src.reposity import reposity

class storage_reposity(reposity):
    def __init__(self):
        super().__init__()
        # Инициализируем обязательные секции
        self.data[reposity.range_key()] = []
        self.data[reposity.group_key()] = []
        self.data[reposity.nomenclature_key()] = []
        self.data[reposity.receipts_key()] = []

    # Утилиты добавления данных
    def add_range(self, item):
        self.data[reposity.range_key()].append(item)

    def add_group(self, item):
        self.data[reposity.group_key()].append(item)

    def add_nomenclature(self, item):
        self.data[reposity.nomenclature_key()].append(item)

    def add_receipt(self, item):
        self.data[reposity.receipts_key()].append(item)
