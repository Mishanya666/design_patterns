class argument_exception(Exception):
    pass

class operation_exception(Exception):
    pass

class validator:

    @staticmethod
    def validate(value, type_, len_=None):


        if value is None:
            raise argument_exception("Пустой аргумент")

        # Проверка типа (поддерживаем передавать класс/tuple)
        if not isinstance(value, type_):
            raise argument_exception(f"Некорректный тип!\nОжидается {type_}. Текущий тип {type(value)}")

        # Проверка аргумента на пустоту (строки/числа)
        if isinstance(value, str) and len(value.strip()) == 0:
            raise argument_exception("Пустой аргумент")

        if len_ is not None:
            # Преобразуем в строку и проверяем длину
            if len(str(value).strip()) == 0:
                raise argument_exception("Пустой аргумент")
            if len(str(value).strip()) > len_:
                raise argument_exception("Некорректная длина аргумента")

        return True
