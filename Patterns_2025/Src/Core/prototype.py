from Src.Core.validator import validator

from Src.Core.common import common
from abc import ABC, abstractmethod
from typing import List, Any, Optional
from copy import deepcopy
from Src.Dtos.filter_dto import filter_dto

class IPrototype(ABC):
    @abstractmethod
    def clone(self) -> 'IPrototype':
        pass

    @abstractmethod
    def execute(self, data: List[dict], filter_dto: filter_dto) -> List[dict]:
        pass
# Абстрактный класс - прототип
class prototype:
    __data = []

    # Набор данных
    @property
    def data(self):
        return self.__data

    def __init__(self, data:list):
        validator.validate(data, list)
        self.__data = data
        
    # Клонирование        
    def clone(self, data:list = None)-> "prototype":
        inner_data = None
        if data is None:
            inner_data = self.__data
        else:
            inner_data = data

        instance =  prototype(inner_data)
        return instance   
    
    # Универсальный фильтр
    @staticmethod
    def filter(data:list, filter:filter_dto ) -> list:
        if len(data) == 0:
            return data
        
        result = []
        first_item = data[0]
        for field in common.get_fields(first_item):
            for item in data:
                if field == filter.field_name:
                    value = str( getattr(item, field))
                    if value == filter.value:
                        result.append(item)

        return result

                