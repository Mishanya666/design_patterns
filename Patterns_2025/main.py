import connexion
import json
from Src.Services.osv_service import osv_filter
from Src.Filters.nomenclature_filter import nomenclature_prototype
from Src.Services.osv_service import osv_prototype, calculate_osv


from flask import request, jsonify
from Src.Dtos.filter_dto import filter_dto
from Src.Core.data_prototype import DataPrototype

app = connexion.FlaskApp(__name__)

# Загружаем настройки
with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

nom_map = {n["id"]: n for n in settings["default_refenences"]["nomenclatures"]}
range_map = {r["id"]: r for r in settings["default_refenences"]["ranges"]}

@app.route("/api/filter/<model_type>", methods=['POST'])
def filter_data(model_type: str):
    dto = filter_dto(**request.json)

    if model_type == "nomenclature":
        prototype = nomenclature_prototype.clone()
        data = settings["default_refenences"]["nomenclatures"]
        result = prototype.execute(data, dto)
        return jsonify(result)

    return jsonify({"error": "Unknown model"}), 400


@app.route("/api/osv", methods=['POST'])
def get_osv():
    dto = filter_dto(**request.json)

    # Клонируем прототип и настраиваем под ОСВ
    prototype = osv_prototype.clone()
    transactions = settings.get("default_transactions", [])

    # Фильтруем транзакции
    filtered_txs = [
        t for t in transactions
        if osv_filter(t, dto, nom_map)
    ]

    # Считаем ОСВ
    result = calculate_osv(filtered_txs, nom_map, range_map)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8080)
