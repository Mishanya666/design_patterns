class argument_exception(Exception):
    """Исключение для неверных аргументов"""
    pass

class operation_exception(Exception):
    """Исключение для ошибок операций"""
    pass

class error_proxy:
    """Прокси для ошибок, чтобы логировать или обрабатывать"""
    def __init__(self, original_error):
        self.original = original_error

    def __str__(self):
        return f"Прокси ошибка: {str(self.original)}"