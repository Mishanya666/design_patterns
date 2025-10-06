from Src.Models.abstract_reference import abstract_reference

class nomenclature_group_model(abstract_reference):
    def __init__(self, name: str):
        super().__init__(name)