from Src.Core.abstract_model import abstact_model
from Src.Core.validator import validator
from Src.Models.ingredient_model import ingredient_model
from Src.Models.step_model import step_model

class receipt_model(abstact_model):
    __title: str = ""
    __portions: int = 1
    __ingredients: list = None
    __steps: list = None

    def __init__(self):
        super().__init__()
        self.__ingredients = []
        self.__steps = []

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        validator.validate(value, str)
        self.__title = value.strip()

    @property
    def portions(self) -> int:
        return self.__portions

    @portions.setter
    def portions(self, value: int):
        validator.validate(value, int)
        if value <= 0:
            raise Exception("Некорректное количество порций")
        self.__portions = value

    @property
    def ingredients(self) -> list:
        return self.__ingredients

    def add_ingredient(self, ingredient: ingredient_model):
        validator.validate(ingredient, ingredient_model)
        self.__ingredients.append(ingredient)

    @property
    def steps(self) -> list:
        return self.__steps

    def add_step(self, step: step_model):
        validator.validate(step, step_model)
        self.__steps.append(step)
