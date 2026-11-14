"""Mock store data. In a real system this would be a database or API."""

PRODUCTS = {
    "P100": {"name": "Wireless Mouse", "price": 799.0, "category": "accessories", "stock": 25},
    "P101": {"name": "Mechanical Keyboard", "price": 3499.0, "category": "accessories", "stock": 0},
    "P102": {"name": "USB-C Hub", "price": 1499.0, "category": "accessories", "stock": 8},
    "P200": {"name": "Running Shoes", "price": 2999.0, "category": "footwear", "stock": 12},
    "P201": {"name": "Trail Shoes", "price": 4599.0, "category": "footwear", "stock": 3},
}

ORDERS = {
    "O1001": {"status": "shipped", "items": ["P100"], "delivered_on": None,
              "eta": "2026-11-16", "return_requested": False},
    "O1002": {"status": "delivered", "items": ["P200"], "delivered_on": "2026-11-10",
              "eta": None, "return_requested": False},
    "O1003": {"status": "delivered", "items": ["P102"], "delivered_on": "2026-10-20",
              "eta": None, "return_requested": False},
}

RETURN_WINDOW_DAYS = 7