# Src/start_service.py
from Src.storage_reposity import storage_reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_model import receipt_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.step_model import step_model

class start_service:
    __repo: storage_reposity = None

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

    def __init__(self):

        if self.__repo is None:
            self.__repo = storage_reposity()

    """
    Возвращает текущие данные (словарь)
    """
    def data(self):
        return self.__repo.data

    """
    Внутренние стандартные единицы
    """
    def __default_create_ranges(self):
        gram = range_model.create_gramm()
        kilogram = range_model.create_kill()
        # Для наглядности установим value (коэффициент) — грамм базовый: грамм.value = 1, килограмм.value = 1000
        gram.value = 1
        kilogram.value = 1000
        kilogram.base = gram

        self.__repo.add_range(gram)
        self.__repo.add_range(kilogram)

    """
    Стандартные группы номенклатуры
    """
    def __default_create_groups(self):
        g_food = group_model()
        g_food.name = "Продукты"
        g_ing = group_model()
        g_ing.name = "Ингредиенты"

        self.__repo.add_group(g_food)
        self.__repo.add_group(g_ing)

    """
    Простейшая номенклатура (несколько позиций)
    """
    def __default_create_nomenclature(self):
        from Src.Models.range_model import range_model as rm
        ranges = self.__repo.data.get(storage_reposity.range_key(), [])
        # ищем грамм
        gram = None
        for r in ranges:
            if r.name == "грамм":
                gram = r
                break
        if gram is None and len(ranges) > 0:
            gram = ranges[0]

        groups = self.__repo.data.get(storage_reposity.group_key(), [])
        group_products = groups[0] if len(groups) > 0 else None

        # создаём пример номенклатуры
        if group_products is not None:
            flour = nomenclature_model()
            flour.name = "Пшеничная мука"
            flour.group = group_products
            flour.range = gram
            self.__repo.add_nomenclature(flour)

            sugar = nomenclature_model()
            sugar.name = "Сахар"
            sugar.group = group_products
            sugar.range = gram
            self.__repo.add_nomenclature(sugar)

    """
    Создать рецепты (фабрика рецептов). Добавляем рецепт из задания и примерный второй рецепт.
    """
    def create_receipts(self):

        rec = receipt_model()
        rec.title = "Вафли хрустящие в вафельнице"
        rec.portions = 10

        # Для единиц: найдём грамм в репозитории
        grams = None
        for r in self.__repo.data.get(storage_reposity.range_key(), []):
            if r.name == "грамм":
                grams = r
                break

        # Ингредиенты (частично берем из задания)
        ing1 = ingredient_model()
        ing1.name = "Пшеничная мука"
        ing1.amount = 250
        if grams:
            ing1.unit = grams
        rec.add_ingredient(ing1)

        ing2 = ingredient_model()
        ing2.name = "Сахар"
        ing2.amount = 30
        if grams:
            ing2.unit = grams
        rec.add_ingredient(ing2)

        ing3 = ingredient_model()
        ing3.name = "Сливочное масло"
        ing3.amount = 40
        if grams:
            ing3.unit = grams
        rec.add_ingredient(ing3)

        ing4 = ingredient_model()
        ing4.name = "Яйца"
        ing4.amount = 2
        # единица — штука, можно не указывать range
        rec.add_ingredient(ing4)

        ing5 = ingredient_model()
        ing5.name = "Соль"
        ing5.amount = 1
        if grams:
            ing5.unit = grams
        rec.add_ingredient(ing5)

        # Шаги
        s1 = step_model()
        s1.name = "Подготовка"
        s1.description = "Растопите масло, смешайте с сахаром, добавьте яйцо, муку."
        rec.add_step(s1)

        s2 = step_model()
        s2.name = "Выпечка"
        s2.description = "Разогрейте сковороду, выпекайте блины до золотистого цвета с обеих сторон."
        rec.add_step(s2)

        self.__repo.add_receipt(rec)

        rec2 = receipt_model()
        rec2.title = "Тестовый рецепт"
        rec2.portions = 1
        self.__repo.add_receipt(rec2)

    """
    Основной метод для генерации эталонных данных
    """
    def create(self):
        # создаём справочники
        self.__default_create_ranges()
        self.__default_create_groups()
        self.__default_create_nomenclature()
        # рецепты
        self.create_receipts()
