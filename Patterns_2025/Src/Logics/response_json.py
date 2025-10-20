from Src.Core.abstract_response import abstract_response
from Src.Core.validator import validator
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_model import receipt_model
import json


class response_json(abstract_response):
    def build(self, format: str, data: list) -> str:
        validator.validate(format, str)
        validator.validate(data, list)

        if not data:
            return "[]"

        result = []
        for item in data:
            if isinstance(item, range_model):
                result.append({
                    "name": item.name,
                    "base_id": item.base.unique_code if item.base else None,
                    "value": item.value,
                    "unique_code": item.unique_code
                })
            elif isinstance(item, group_model):
                result.append({
                    "name": item.name,
                    "unique_code": item.unique_code
                })
            elif isinstance(item, nomenclature_model):
                result.append({
                    "name": item.name,
                    "group_id": item.group.unique_code if item.group else None,
                    "range_id": item.range.unique_code if item.range else None,
                    "unique_code": item.unique_code
                })
            elif isinstance(item, receipt_model):
                composition = [{
                    "nomenclature_id": comp.nomenclature.unique_code if comp.nomenclature else None,
                    "range_id": comp.range.unique_code if comp.range else None,
                    "value": comp.value
                } for comp in item.composition]
                result.append({
                    "name": item.name,
                    "cooking_time": item.cooking_time,
                    "portions": item.portions,
                    "composition": composition,
                    "steps": item.steps
                })

        return json.dumps(result, ensure_ascii=False, indent=2)