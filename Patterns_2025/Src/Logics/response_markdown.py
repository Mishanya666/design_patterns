from Src.Core.abstract_response import abstract_response
from Src.Core.validator import validator
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_model import receipt_model


class response_markdown(abstract_response):
    def build(self, format: str, data: list) -> str:
        validator.validate(format, str)
        validator.validate(data, list)

        if not data:
            return ""

        result = []

        if isinstance(data[0], range_model):
            headers = ["name", "base", "value", "unique_code"]
            result.append("| " + " | ".join(headers) + " |")
            result.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for item in data:
                base_name = item.base.name if item.base else ""
                result.append(f"| {item.name} | {base_name} | {item.value} | {item.unique_code} |")

        elif isinstance(data[0], group_model):
            headers = ["name", "unique_code"]
            result.append("| " + " | ".join(headers) + " |")
            result.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for item in data:
                result.append(f"| {item.name} | {item.unique_code} |")

        elif isinstance(data[0], nomenclature_model):
            headers = ["name", "group", "range", "unique_code"]
            result.append("| " + " | ".join(headers) + " |")
            result.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for item in data:
                group_name = item.group.name if item.group else ""
                range_name = item.range.name if item.range else ""
                result.append(f"| {item.name} | {group_name} | {range_name} | {item.unique_code} |")

        elif isinstance(data[0], receipt_model):
            result.append("# Receipt")
            for item in data:
                result.append(f"## {item.name}")
                result.append(f"- Cooking Time: {item.cooking_time}")
                result.append(f"- Portions: {item.portions}")
                result.append("### Composition")
                result.append("| Nomenclature | Range | Value |")
                result.append("| --- | --- | --- |")
                for comp in item.composition:
                    nom_name = comp.nomenclature.name if comp.nomenclature else ""
                    range_name = comp.range.name if comp.range else ""
                    result.append(f"| {nom_name} | {range_name} | {comp.value} |")
                result.append("### Steps")
                for i, step in enumerate(item.steps, 1):
                    result.append(f"{i}. {step}")

        return "\n".join(result)