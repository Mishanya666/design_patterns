from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime

class IOSVPrototype(ABC):
    @abstractmethod
    def calculate(self, transactions: List[Dict], filter_dto) -> List[Dict]:
        pass