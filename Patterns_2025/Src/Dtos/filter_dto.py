from Src.Core.abstract_dto import abstract_dto
from Src.Core.filter_type import FilterType
from typing import Optional

class filter_dto(abstract_dto):
    __name: Optional[str] = None
    __name_filter: FilterType = FilterType.LIKE

    __code: Optional[str] = None
    __code_filter: FilterType = FilterType.EQUALS

    __base_id: Optional[str] = None
    __parent_id: Optional[str] = None

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @name.setter
    def name(self, value: Optional[str]):
        self.__name = value

    @property
    def name_filter(self) -> FilterType:
        return self.__name_filter

    @name_filter.setter
    def name_filter(self, value: FilterType):
        self.__name_filter = value

    @property
    def code(self) -> Optional[str]:
        return self.__code

    @code.setter
    def code(self, value: Optional[str]):
        self.__code = value

    @property
    def code_filter(self) -> FilterType:
        return self.__code_filter

    @code_filter.setter
    def code_filter(self, value: FilterType):
        self.__code_filter = value

    @property
    def base_id(self) -> Optional[str]:
        return self.__base_id

    @base_id.setter
    def base_id(self, value: Optional[str]):
        self.__base_id = value

    @property
    def parent_id(self) -> Optional[str]:
        return self.__parent_id

    @parent_id.setter
    def parent_id(self, value: Optional[str]):
        self.__parent_id = value