import pytest
from datetime import date
from Src.Services.balance_service import BalanceService
import json

@pytest.fixture
def settings():
    with open("settings.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    from Src.Models.settings_model import settings_model
    s = settings_model()
    s.default_transactions = data["default_transactions"]
    s.default_refenences = data["default_refenences"]
    return s

def test_balance_independent_of_block_period(settings):
    service = BalanceService(settings)

    settings.block_period = "2025-01-01"
    service.recalculate_blocked_turnover()
    result1 = service.get_balance(date(2025-12-31))

    settings.block_period = "2024-06-01"
    service.recalculate_blocked_turnover()
    result2 = service.get_balance(date(2025-12-31))

    settings.block_period = "2023-01-01"
    service.recalculate_blocked_turnover()
    result3 = service.get_balance(date(2025-12-31))

    assert result1 == result2 == result3
