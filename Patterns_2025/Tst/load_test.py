import time
import random
from datetime import datetime, timedelta, date
import json

# Генерируем 5000 транзакций
def generate_transactions(count=5000):
    noms = ["0c101a7e-5934-4155-83a6-d2c388fcc11a", "39d9349d-28fa-4c7b-ad92-5c5fc7cf93da"]
    start = datetime(2020, 1, 1)
    txs = []
    for i in range(count):
        dt = start + timedelta(days=random.randint(0, 2000))
        txs.append({
            "id": str(i),
            "nomenclature_id": random.choice(noms),
            "storage_id": "7dc27e96-e6ad-4e5e-8c56-84e00667e3d7",
            "value": random.uniform(-100, 100),
            "period": dt.strftime("%Y-%m-%d")
        })
    return txs

# Замеры
from Src.Services.balance_service import BalanceService

settings = type('obj', (), {
    "default_transactions": generate_transactions(10000),
    "default_refenences": json.load(open("settings.json"))["default_refenences"],
    "block_period": None
})()

service = BalanceService(settings)

dates = ["2023-01-01", "2024-01-01", "2025-01-01", "2025-06-01"]

results = []
for block_date in dates:
    settings.block_period = block_date
    service.recalculate_blocked_turnover()

    start = time.time()
    balance = service.get_balance(date(2025, 12, 31))
    elapsed = time.time() - start
    results.append({"block_date": block_date, "time_ms": round(elapsed * 1000, 2)})

print(results)