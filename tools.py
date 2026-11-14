"""Tools the shopping agent can call.

Each function has type hints and a docstring, because the model reads them
to decide when and how to use the tool.
"""

from datetime import date, datetime

import shop_data


def _today() -> date:
    """Separate function so tests can control 'today'."""
    return date.today()


def search_products(query: str, max_price: float = 0) -> list:
    """Search the catalogue by product name or category.

    Args:
        query: Words to look for, such as "shoes" or "usb hub".
        max_price: Only return products at or below this price in rupees.
            Use 0 for no price limit.

    Returns:
        A list of matching products with id, name, price and in_stock.
    """
    words = query.lower().split()
    results = []
    for pid, p in shop_data.PRODUCTS.items():
        text = f"{p['name']} {p['category']}".lower()
        if words and not all(w in text for w in words):
            continue
        if max_price and p["price"] > max_price:
            continue
        results.append({"id": pid, "name": p["name"], "price": p["price"],
                        "in_stock": p["stock"] > 0})
    return results


def check_inventory(product_id: str) -> dict:
    """Check how many units of a product are in stock.

    Args:
        product_id: The product id, such as "P100".

    Returns:
        The product name and units in stock, or an error if the id is unknown.
    """
    p = shop_data.PRODUCTS.get(product_id)
    if p is None:
        return {"error": f"Unknown product id {product_id}"}
    return {"id": product_id, "name": p["name"], "units_in_stock": p["stock"]}


def get_order_status(order_id: str) -> dict:
    """Look up the status of an order.

    Args:
        order_id: The order id, such as "O1001".

    Returns:
        Status, item names, and the delivery date or expected arrival date.
    """
    o = shop_data.ORDERS.get(order_id)
    if o is None:
        return {"error": f"Unknown order id {order_id}"}
    return {
        "order_id": order_id,
        "status": o["status"],
        "items": [shop_data.PRODUCTS[i]["name"] for i in o["items"]],
        "delivered_on": o["delivered_on"],
        "expected_arrival": o["eta"],
        "return_requested": o["return_requested"],
    }


def start_return(order_id: str, reason: str) -> dict:
    """Start a return for a delivered order, if it is inside the return window.

    Args:
        order_id: The order id, such as "O1002".
        reason: Why the customer wants to return the order.

    Returns:
        A confirmation, or an error explaining why the return is not allowed.
    """
    o = shop_data.ORDERS.get(order_id)
    if o is None:
        return {"error": f"Unknown order id {order_id}"}
    if o["status"] != "delivered":
        return {"error": "Only delivered orders can be returned."}
    if o["return_requested"]:
        return {"error": "A return has already been requested for this order."}
    delivered = datetime.strptime(o["delivered_on"], "%Y-%m-%d").date()
    days = (_today() - delivered).days
    if days > shop_data.RETURN_WINDOW_DAYS:
        return {"error": f"Return window of {shop_data.RETURN_WINDOW_DAYS} days has passed "
                         f"(delivered {days} days ago)."}
    o["return_requested"] = True
    return {"order_id": order_id, "return_started": True, "reason": reason}