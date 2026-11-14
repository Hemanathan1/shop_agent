import copy
from datetime import date

import pytest

import shop_data
import tools


@pytest.fixture(autouse=True)
def fresh_state(monkeypatch):
    
    monkeypatch.setattr(shop_data, "ORDERS", copy.deepcopy(shop_data.ORDERS))
    monkeypatch.setattr(tools, "_today", lambda: date(2026, 11, 14))


def test_search_finds_by_category():
    names = [p["name"] for p in tools.search_products("shoes")]
    assert names == ["Running Shoes", "Trail Shoes"]


def test_search_respects_max_price():
    names = [p["name"] for p in tools.search_products("shoes", max_price=3000)]
    assert names == ["Running Shoes"]


def test_search_no_match_returns_empty_list():
    assert tools.search_products("laptop") == []


def test_inventory_known_product():
    result = tools.check_inventory("P102")
    assert result["units_in_stock"] == 8


def test_inventory_unknown_product_returns_error():
    assert "error" in tools.check_inventory("P999")


def test_order_status_shipped():
    result = tools.get_order_status("O1001")
    assert result["status"] == "shipped"
    assert result["expected_arrival"] == "2026-11-16"
    assert result["items"] == ["Wireless Mouse"]


def test_order_status_unknown_order():
    assert "error" in tools.get_order_status("O9999")


def test_return_allowed_inside_window():
    result = tools.start_return("O1002", "Wrong size")
    assert result["return_started"] is True
    assert shop_data.ORDERS["O1002"]["return_requested"] is True


def test_return_rejected_after_window():
    result = tools.start_return("O1003", "Changed my mind")
    assert "error" in result
    assert "window" in result["error"]


def test_return_rejected_if_not_delivered():
    assert "error" in tools.start_return("O1001", "Too slow")


def test_return_cannot_be_requested_twice():
    tools.start_return("O1002", "Wrong size")
    assert "error" in tools.start_return("O1002", "Wrong size")