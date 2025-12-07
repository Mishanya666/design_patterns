

"""
Типы событий
"""
class event_type:

    """
    Событие - смена даты блокировки
    """
    @staticmethod
    def change_block_period() -> str:
        return "change_block_period"

    """
    Событие - сформирован Json
    """
    @staticmethod
    def convert_to_json() -> str:
        return "convert_to_json"

    """
    Получить список всех событий
    """
    @staticmethod
    def events() -> list:
        result = []
        methods = [method for method in dir(event_type) if
                    callable(getattr(event_type, method)) and not method.startswith('__') and method != "events"]
        for method in methods:
            key = getattr(event_type, method)()
            result.append(key)

        return result

    @staticmethod
    def nomenclature_updated() -> str:
        return "nomenclature_updated"

    @staticmethod
    def nomenclature_deleted() -> str:
        return "nomenclature_deleted"

    """
       Событие - обновлены настройки
       """

    @staticmethod
    def settings_updated() -> str:
        return "settings_updated"

    """
    Событие - складская операция
    """

    @staticmethod
    def storage_operation() -> str:
        return "storage_operation"

    """
    Событие - складская операция создана
    """

    @staticmethod
    def storage_operation_created() -> str:
        return "storage_operation_created"

    """
    Событие - складская операция обновлена
    """

    @staticmethod
    def storage_operation_updated() -> str:
        return "storage_operation_updated"

    """
    Событие - складская операция удалена
    """

    @staticmethod
    def storage_operation_deleted() -> str:
        return "storage_operation_deleted"

    """
    Событие - расчет остатков (OST)
    """

    @staticmethod
    def ost_calculation() -> str:
        return "ost_calculation"

    """
    Событие - расчет остатков завершен
    """

    @staticmethod
    def ost_calculation_completed() -> str:
        return "ost_calculation_completed"

    """
    Событие - ошибка расчета остатков
    """

    @staticmethod
    def ost_calculation_error() -> str:
        return "ost_calculation_error"

    """
    Событие - запуск приложения
    """

    @staticmethod
    def application_started() -> str:
        return "application_started"

    """
    Событие - остановка приложения
    """

    @staticmethod
    def application_stopped() -> str:
        return "application_stopped"

    """
    Событие - ошибка приложения
    """

    @staticmethod
    def application_error() -> str:
        return "application_error"

    """
    Событие - API запрос
    """

    @staticmethod
    def api_request() -> str:
        return "api_request"

    """
    Событие - API запрос успешен
    """

    @staticmethod
    def api_request_success() -> str:
        return "api_request_success"

    """
    Событие - API запрос с ошибкой
    """

    @staticmethod
    def api_request_error() -> str:
        return "api_request_error"

    """
    Событие - аутентификация пользователя
    """

    @staticmethod
    def user_authenticated() -> str:
        return "user_authenticated"

    """
    Событие - ошибка аутентификации
    """

    @staticmethod
    def authentication_error() -> str:
        return "authentication_error"

    """
    Событие - выход пользователя
    """

    @staticmethod
    def user_logged_out() -> str:
        return "user_logged_out"

    """
    Событие - экспорт данных
    """

    @staticmethod
    def data_export() -> str:
        return "data_export"

    """
    Событие - импорт данных
    """

    @staticmethod
    def data_import() -> str:
        return "data_import"

    """
    Событие - отчет сгенерирован
    """

    @staticmethod
    def report_generated() -> str:
        return "report_generated"

    """
    Событие - запуск фоновой задачи
    """

    @staticmethod
    def background_task_started() -> str:
        return "background_task_started"

    """
    Событие - завершение фоновой задачи
    """

    @staticmethod
    def background_task_completed() -> str:
        return "background_task_completed"

    """
    Событие - ошибка фоновой задачи
    """

    @staticmethod
    def background_task_error() -> str:
        return "background_task_error"

    """
    Событие - кэш обновлен
    """

    @staticmethod
    def cache_updated() -> str:
        return "cache_updated"

    """
    Событие - кэш очищен
    """

    @staticmethod
    def cache_cleared() -> str:
        return "cache_cleared"

    """
    Событие - уведомление пользователя
    """

    @staticmethod
    def user_notification() -> str:
        return "user_notification"

    """
    Событие - системное предупреждение
    """

    @staticmethod
    def system_warning() -> str:
        return "system_warning"

    """
    Событие - критическая ошибка
    """

    @staticmethod
    def critical_error() -> str:
        return "critical_error"

    """
    Событие - проверка целостности данных
    """

    @staticmethod
    def data_integrity_check() -> str:
        return "data_integrity_check"

    """
    Событие - резервное копирование данных
    """

    @staticmethod
    def data_backup() -> str:
        return "data_backup"

    """
    Событие - восстановление данных
    """

    @staticmethod
    def data_restore() -> str:
        return "data_restore"

    """
    Событие - аудит безопасности
    """

    @staticmethod
    def security_audit() -> str:
        return "security_audit"

