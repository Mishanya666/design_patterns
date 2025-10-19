from Src.Core.response_format import response_formats
from Src.Core.validator import validator, operation_exception
from Src.Models.receipt_model import receipt_model

class response_csv(response_formats):
    def build(self, format: str, data: list) -> str:
        validator.validate(format, str)
        validator.validate(data, list)

        if format != "CSV":
            raise operation_exception("Формат должен быть CSV!")

        result = []
        for item in data:
            if isinstance(item, receipt_model):
                # Формируем данные для рецепта
                composition = ";".join([
                    f"{comp.nomenclature.name if comp.nomenclature else 'Неизвестно'},{comp.range.name if comp.range else 'Неизвестно'},{comp.value}"
                    for comp in item.composition
                ])
                result.append(
                    f"{item.name};{item.cooking_time};{item.portions};[{composition}];[{';'.join(item.steps)}]"
                )
            else:
                # Обработка других типов данных (range_model, group_model, nomenclature_model)
                result.append(f"{item.name};{item.unique_code}")

        return "\n".join(result)