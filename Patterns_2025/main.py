import connexion
import json
from Src.Services.osv_service import osv_filter
from Src.Filters.nomenclature_filter import nomenclature_prototype
from Src.Services.osv_service import osv_prototype, calculate_osv
from Src.Dtos.filter_dto import filter_dto
from flask import request, jsonify
from datetime import datetime
from Src.Services.balance_service import BalanceService
from Src.settings_manager import settings_manager

app = connexion.FlaskApp(__name__)
balance_service = BalanceService(settings_manager().settings)

@app.route("/api/settings/block-period", methods=["POST"])
def set_block_period():
    data = request.json
    if not data or "date" not in data:
        return jsonify({"error": "Укажите date в формате YYYY-MM-DD"}), 400
    try:
        new_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        settings_manager().settings.block_period = data["date"]
        balance_service.recalculate_blocked_turnover()  # Пересчитываем кэш
        return jsonify({"block_period": data["date"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/settings/block-period", methods=["GET"])
def get_block_period():
    return jsonify({"block_period": settings_manager().settings.block_period.isoformat()})

@app.route("/api/balance", methods=["GET"])
def get_balance():
    date_str = request.args.get("date")
    if not date_str:
        return jsonify({"error": "Укажите параметр date"}), 400
    try:
        as_of_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        result = balance_service.get_balance(as_of_date)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
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
