from Src.Core.abstract_response import abstract_response
from Src.Core.validator import validator
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_model import receipt_model


class response_xml(abstract_response):
    def build(self, format: str, data: list) -> str:
        validator.validate(format, str)
        validator.validate(data, list)

        if not data:
            return "<items></items>"

        result = ["<items>"]
        for item in data:
            if isinstance(item, range_model):
                result.append("  <range>")
                result.append(f"    <name>{item.name}</name>")
                result.append(f"    <base_id>{item.base.unique_code if item.base else ''}</base_id>")
                result.append(f"    <value>{item.value}</value>")
                result.append(f"    <unique_code>{item.unique_code}</unique_code>")
                result.append("  </range>")
            elif isinstance(item, group_model):
                result.append("  <group>")
                result.append(f"    <name>{item.name}</name>")
                result.append(f"    <unique_code>{item.unique_code}</unique_code>")
                result.append("  </group>")
            elif isinstance(item, nomenclature_model):
                result.append("  <nomenclature>")
                result.append(f"    <name>{item.name}</name>")
                result.append(f"    <group_id>{item.group.unique_code if item.group else ''}</group_id>")
                result.append(f"    <range_id>{item.range.unique_code if item.range else ''}</range_id>")
                result.append(f"    <unique_code>{item.unique_code}</unique_code>")
                result.append("  </nomenclature>")
            elif isinstance(item, receipt_model):
                result.append("  <receipt>")
                result.append(f"    <name>{item.name}</name>")
                result.append(f"    <cooking_time>{item.cooking_time}</cooking_time>")
                result.append(f"    <portions>{item.portions}</portions>")
                result.append("    <composition>")
                for comp in item.composition:
                    result.append("      <item>")
                    result.append(
                        f"        <nomenclature_id>{comp.nomenclature.unique_code if comp.nomenclature else ''}</nomenclature_id>")
                    result.append(f"        <range_id>{comp.range.unique_code if comp.range else ''}</range_id>")
                    result.append(f"        <value>{comp.value}</value>")
                    result.append("      </item>")
                result.append("    </composition>")
                result.append("    <steps>")
                for step in item.steps:
                    result.append(f"      <step>{step}</step>")
                result.append("    </steps>")
                result.append("  </receipt>")
        result.append("</items>")

        return "\n".join(result)