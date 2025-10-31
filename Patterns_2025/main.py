import connexion
from flask import Response, app
from flask import request

from Src.Core.validator import operation_exception
from Src.settings_manager import settings_manager
from Src.start_service import start_service
from Src.Logics.factory_entities import factory_entities
from Src.reposity import reposity
from Src.Logics.convert_factory import convert_factory
import json
from Src.Models.settings_model import ResponseFormat
from datetime import datetime, date
from Src.Logics.turnover_report import turnover_report

@app.route("/api/data", methods=['GET'])
def get_data():
    entity_type = request.args.get('type', reposity.nomenclature_key())
    format_str = request.args.get('format', 'Json').upper()
    try:
        response_format = ResponseFormat[format_str]
    except KeyError:
        return "Invalid format", 400

    factory_entities_inst = factory_entities()
    data = factory_entities_inst.repo.data.get(entity_type, [])

    if response_format == ResponseFormat.JSON:
        convert_fact = convert_factory()
        converted_data = convert_fact.convert(data)
        json_data = json.dumps(converted_data, ensure_ascii=False, indent=4)
        return json_data, 200, {'Content-Type': 'application/json'}
    else:
        factory.settings.response_format = response_format
        data_str = factory.create_default(entity_type)
        return data_str, 200, {'Content-Type': 'text/plain'}

app = connexion.FlaskApp(__name__)
start = start_service()
start.start()
factory = factory_entities()
repo = start.data


@app.route("/api/accessibility", methods=['GET'])
def accessibility():
    return "SUCCESS"

@app.route("/api/nomenclatures/<format>", methods=['GET'])
def get_nomenclatures(format):
    try:
        logic = factory.create(format)
        data = repo[reposity.nomenclature_key()]
        result = logic.build(format, data)
        content_type = {
            "CSV": "text/csv",
            "Markdown": "text/markdown",
            "Json": "application/json",
            "XML": "application/xml"
        }.get(format, "text/plain")
        return Response(result, content_type=content_type)
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/ranges/<format>", methods=['GET'])
def get_ranges(format):
    try:
        logic = factory.create(format)
        data = repo[reposity.range_key()]
        result = logic.build(format, data)
        content_type = {
            "CSV": "text/csv",
            "Markdown": "text/markdown",
            "Json": "application/json",
            "XML": "application/xml"
        }.get(format, "text/plain")
        return Response(result, content_type=content_type)
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/groups/<format>", methods=['GET'])
def get_groups(format):
    try:
        logic = factory.create(format)
        data = repo[reposity.group_key()]
        result = logic.build(format, data)
        content_type = {
            "CSV": "text/csv",
            "Markdown": "text/markdown",
            "Json": "application/json",
            "XML": "application/xml"
        }.get(format, "text/plain")
        return Response(result, content_type=content_type)
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/api/receipt/<code>", methods=['GET'])
def get_receipt(code: str):
    repo = reposity()
    receipts = repo.data.get(reposity.receipt_key(), [])
    for receipt in receipts:
        if receipt.unique_code == code:
            convert_fact = convert_factory()
            converted = convert_fact.convert(receipt)
            json_data = json.dumps(converted, ensure_ascii=False, indent=4)
            return json_data, 200, {'Content-Type': 'application/json'}
    return "Receipt not found", 404

@app.route("/api/receipts/<format>", methods=['GET'])
def get_receipts(format):
    try:
        logic = factory.create(format)
        data = repo[reposity.receipt_key()]
        result = logic.build(format, data)
        content_type = {
            "CSV": "text/csv",
            "Markdown": "text/markdown",
            "Json": "application/json",
            "XML": "application/xml"
        }.get(format, "text/plain")
        return Response(result, content_type=content_type)
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/receipts", methods=['GET'])
def get_receipts():
    repo = reposity()
    receipts = repo.data.get(reposity.receipt_key(), [])
    convert_fact = convert_factory()
    converted = convert_fact.convert(receipts)
    json_data = json.dumps(converted, ensure_ascii=False, indent=4)
    return json_data, 200, {'Content-Type': 'application/json'}


@app.route("/api/turnover_report", methods=['GET'])
def get_turnover_report():
    """
    Возвращает оборотно-сальдовую ведомость (ОСВ).
    :param start_date: Дата начала (YYYY-MM-DD).
    :param end_date: Дата окончания (YYYY-MM-DD).
    :param storage: Уникальный код склада.
    :return: JSON с таблицей ОСВ.
    """
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')
    storage_code = request.args.get('storage')

    if not all([start_str, end_str, storage_code]):
        return "Missing parameters", 400

    try:
        start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
        report = turnover_report.generate(start_date, end_date, storage_code)
        return json.dumps(report, indent=4, ensure_ascii=False), 200, {'Content-Type': 'application/json'}
    except ValueError as e:
        return str(e), 400
    except operation_exception as e:
        return str(e), 400


@app.route("/api/save", methods=['POST'])
def save_data():
    """
    Сохраняет все данные из репозитория в файл data.json.
    """
    repo = reposity()
    # Сериализация данных (простая, с __dict__)
    data_to_save = {}
    for key, items in repo.data.items():
        data_to_save[key] = [item.__dict__ for item in items]
        # Обработка дат и объектов
        for item_dict in data_to_save[key]:
            for k, v in item_dict.items():
                if isinstance(v, date):
                    item_dict[k] = v.isoformat()
                elif hasattr(v, 'name'):  # Для связанных моделей
                    item_dict[k] = v.name

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=4, ensure_ascii=False)

    return "Data saved to data.json", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

    settings_mgr = settings_manager()
    settings_mgr.file_name = "settings.json"
    settings_mgr.load()

    service = start_service()
    service.file_name = "settings.json"

    if settings_mgr.settings.first_start:
        service.start()
        # После первого старта установить False и сохранить
        settings_mgr.settings.first_start = False
        # Сохранить settings.json (добавить метод save в settings_manager)