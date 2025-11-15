from enum import Enum

class FilterType(Enum):
    EQUALS = "EQUALS"  # Полное совпадение
    LIKE = "LIKE"      # Вхождение подстроки