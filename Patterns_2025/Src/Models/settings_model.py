from Src.Core.validator import validator, argument_exception

class settings_model:
    def __init__(self):
        self.__response_format = "Json"

    @property
    def response_format(self):
        return self.__response_format

    @response_format.setter
    def response_format(self, value):
        validator.validate(value, str)
        if value not in ["CSV", "Json", "Markdown", "XML"]:
            raise argument_exception(f"Формат {value} не поддерживается!")
        self.__response_format = value

    def __eq__(self, other):
        if not isinstance(other, settings_model):
            return False
        return self.__response_format == other.response_format