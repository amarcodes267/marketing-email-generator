CATEGORY_PRODUCTS = {
    "Fashion": "Jacket",
    "Electronics": "Wireless Earbuds",
    "Sports": "Performance Running Shoes",
    "Books": "Bestselling Novel",
    "Beauty": "Skincare Kit",
    "Home Decor": "Smart Lamp",
}

PREMIUM_PRODUCTS = {
    "Fashion": "Premium Jacket",
    "Electronics": "Premium Wireless Earbuds",
    "Sports": "Premium Performance Running Shoes",
    "Books": "Exclusive Bestselling Novel",
    "Beauty": "Luxury Skincare Kit",
    "Home Decor": "Designer Smart Lamp",
}

PREMIUM_SEGMENTS = {"VIP Customer"}


def _normalize_category(category):
    if category is None or not str(category).strip():
        raise ValueError("Favorite Category is required.")
    return str(category).strip()


def _require_known_category(category):
    if category not in CATEGORY_PRODUCTS:
        available = ", ".join(CATEGORY_PRODUCTS)
        raise ValueError(f"Unknown category: {category}. Choose from: {available}.")
    return category


def recommend_product(category, customer_segment="New Customer"):
    normalized = _normalize_category(category)
    _require_known_category(normalized)
    if customer_segment in PREMIUM_SEGMENTS:
        return PREMIUM_PRODUCTS[normalized]
    return CATEGORY_PRODUCTS[normalized]

