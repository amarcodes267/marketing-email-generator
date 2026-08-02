ALLOWED_GENDERS = ["Male", "Female", "Other"]
MAX_NAME_LENGTH = 80
MAX_LOCATION_LENGTH = 120
MAX_PURCHASE_HISTORY_LENGTH = 2000
ALLOWED_TONES = [
    "Friendly",
    "Warm",
    "Casual",
    "Conversational",
    "Professional",
    "Formal",
    "Business",
    "Trustworthy",
    "Luxury",
    "Elegant",
    "Premium",
    "Exclusive",
    "Exciting",
    "Energetic",
    "Urgent",
    "Promotional",
]
ALLOWED_CATEGORIES = [
    "Fashion",
    "Electronics",
    "Books",
    "Sports",
    "Home Decor",
    "Beauty",
]


def validate_email_request(data):
    errors = []

    if data is None:
        return {"valid": False, "errors": [{"field": "body", "message": "Request body is required."}]}

    customer_name = data.get("customer_name")
    if not customer_name or not str(customer_name).strip():
        errors.append({"field": "customer_name", "message": "Customer Name is required."})
    elif len(str(customer_name).strip()) > MAX_NAME_LENGTH:
        errors.append({"field": "customer_name", "message": f"Customer Name must be at most {MAX_NAME_LENGTH} characters."})

    age = data.get("age")
    if age is None:
        errors.append({"field": "age", "message": "Age is required."})
    elif not isinstance(age, int):
        errors.append({"field": "age", "message": "Age must be an integer."})
    elif age < 18 or age > 100:
        errors.append({"field": "age", "message": "Age must be between 18 and 100."})

    gender = data.get("gender")
    if not gender:
        errors.append({"field": "gender", "message": "Gender is required."})
    elif gender not in ALLOWED_GENDERS:
        errors.append({"field": "gender", "message": "Gender must be one of: Male, Female, Other."})

    location = data.get("location")
    if not location or not str(location).strip():
        errors.append({"field": "location", "message": "Location is required."})
    elif len(str(location).strip()) > MAX_LOCATION_LENGTH:
        errors.append({"field": "location", "message": f"Location must be at most {MAX_LOCATION_LENGTH} characters."})

    purchase_history = data.get("purchase_history")
    if not purchase_history or not str(purchase_history).strip():
        errors.append({"field": "purchase_history", "message": "Purchase History is required."})
    elif len(str(purchase_history).strip()) > MAX_PURCHASE_HISTORY_LENGTH:
        errors.append({"field": "purchase_history", "message": f"Purchase History must be at most {MAX_PURCHASE_HISTORY_LENGTH} characters."})

    favorite_category = data.get("favorite_category")
    if not favorite_category or not str(favorite_category).strip():
        errors.append({"field": "favorite_category", "message": "Favorite Category is required."})
    elif favorite_category not in ALLOWED_CATEGORIES:
        available = ", ".join(ALLOWED_CATEGORIES)
        errors.append({"field": "favorite_category", "message": f"Unknown category. Choose from: {available}."})

    total_spending = data.get("total_spending")
    if total_spending is None:
        errors.append({"field": "total_spending", "message": "Total Spending is required."})
    elif isinstance(total_spending, bool) or not isinstance(total_spending, (int, float)):
        errors.append({"field": "total_spending", "message": "Total Spending must be a number."})
    elif total_spending <= 0:
        errors.append({"field": "total_spending", "message": "Total Spending must be greater than 0."})

    tone = data.get("tone")
    if not tone:
        errors.append({"field": "tone", "message": "Tone is required."})
    elif tone not in ALLOWED_TONES:
        available = ", ".join(ALLOWED_TONES)
        errors.append({"field": "tone", "message": f"Unknown tone. Choose from: {available}."})

    if errors:
        return {"valid": False, "errors": errors}

    return {"valid": True, "errors": []}

