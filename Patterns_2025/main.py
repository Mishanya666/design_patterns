import connexion
from flask import request, jsonify

from Src.Dtos.filter_dto import filter_dto
from Src.Core.filter_manager import filter_manager
from Src.Services.osv_service import OSVService
from Src.Models.settings_model import settings_model
import json

app = connexion.FlaskApp(__name__)

"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    return "SUCCESS"


# Загружаем настройки
settings = json.load(open("settings.json"))

# Регистрация фильтров
from Src.Filters.nomenclature_filter import NomenclatureFilter
filter_manager.register("nomenclature", NomenclatureFilter(settings["default_refenences"]))

# ОСВ сервис
osv_service = OSVService(settings)

@app.route("/api/filter/<model_type>", methods=['POST'])
def filter_data(model_type: str):
    dto = filter_dto(**request.json)
    data_key = {
        "nomenclature": "nomenclatures",
        "range": "ranges",
        "category": "categories",
        "storage": "storages"
    }.get(model_type)

    if not data_key:
        return jsonify({"error": "Unsupported model"}), 400

    items = settings["default_refenences"][data_key]
    # Здесь нужно маппинг в объекты, упростим — возвращаем как есть
    filtered = filter_manager.apply(model_type, items, dto)
    return jsonify(filtered)

@app.route("/api/osv", methods=['POST'])
def get_osv():
    dto = filter_dto(**request.json)
    transactions = settings.get("default_transactions", [])
    result = osv_service.calculate(transactions, dto)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8080)
