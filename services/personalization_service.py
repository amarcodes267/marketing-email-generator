from services.recommendation_service import recommend_product

SEGMENT_BOUNDARIES = [
    ("New Customer", 0, 5000),
    ("Regular Customer", 5001, 20000),
    ("Premium Customer", 20001, 50000),
    ("VIP Customer", 50001, float("inf")),
]

LOYALTY_BY_SEGMENT = {
    "New Customer": "New",
    "Regular Customer": "Silver",
    "Premium Customer": "Gold",
    "VIP Customer": "Platinum",
}

DISCOUNT_BY_SEGMENT = {
    "New Customer": 5,
    "Regular Customer": 10,
    "Premium Customer": 15,
    "VIP Customer": 20,
}

MARKETING_STYLES = {
    "Friendly": "Use a friendly, warm and casual conversational tone. Be approachable and personable.",
    "Warm": "Use a warm, heartfelt tone that makes the customer feel valued and appreciated.",
    "Casual": "Use a casual, relaxed tone with simple language as if writing to a friend.",
    "Conversational": "Use a conversational, natural tone that invites dialogue and engagement.",
    "Professional": "Use a professional, polished tone with clear and precise language.",
    "Formal": "Use a formal, courteous tone with structured and dignified language.",
    "Business": "Use a business-focused tone that is direct, confident and results-oriented.",
    "Trustworthy": "Use a trustworthy, reassuring tone that builds confidence and credibility.",
    "Luxury": "Use a luxury, elegant tone with refined and sophisticated language.",
    "Elegant": "Use an elegant, graceful tone with polished and refined phrasing.",
    "Premium": "Use a premium, high-end tone that emphasizes exclusivity and quality.",
    "Exclusive": "Use an exclusive, elite tone that makes the customer feel special and privileged.",
    "Exciting": "Use an exciting, energetic tone that creates enthusiasm and anticipation.",
    "Energetic": "Use an energetic, vibrant tone with dynamic and upbeat language.",
    "Urgent": "Use an urgent, time-sensitive tone that encourages immediate action.",
    "Promotional": "Use a promotional, compelling tone that highlights offers and value.",
}

CTA_BY_TONE = {
    "Friendly": "Shop today and enjoy your exclusive offer.",
    "Warm": "Come by and let us make your day special.",
    "Casual": "Check it out today and treat yourself.",
    "Conversational": "Let's get you set up with something you'll love.",
    "Professional": "Explore our latest collection today.",
    "Formal": "We invite you to explore our latest offerings at your convenience.",
    "Business": "Discover the value waiting for you today.",
    "Trustworthy": "Explore with confidence today.",
    "Luxury": "Experience premium quality today.",
    "Elegant": "Indulge in elegance today.",
    "Premium": "Elevate your everyday with premium quality today.",
    "Exclusive": "Claim your exclusive offer today.",
    "Exciting": "Hurry! Offer ends soon.",
    "Energetic": "Jump in now and grab this exciting offer.",
    "Urgent": "Act now before this offer expires.",
    "Promotional": "Don't miss out on this amazing deal today.",
}


def _coerce_spending(total_spending):
    if total_spending is None:
        raise ValueError("Total Spending is required.")
    if isinstance(total_spending, bool):
        raise ValueError("Total Spending must be a number.")
    if isinstance(total_spending, (int, float)):
        value = total_spending
    else:
        try:
            value = float(total_spending)
        except (TypeError, ValueError):
            raise ValueError("Total Spending must be a number.")
    if value <= 0:
        raise ValueError("Total Spending must be greater than 0.")
    return value


def _determine_segment(total_spending):
    for segment, lower, upper in SEGMENT_BOUNDARIES:
        if lower <= total_spending <= upper:
            return segment
    return "VIP Customer"


def _determine_spending_level(total_spending):
    if total_spending <= 5000:
        return "Budget"
    if total_spending <= 20000:
        return "Standard"
    return "Premium"


def _normalize_tone(tone):
    normalized = str(tone).strip() if tone else "Friendly"
    if normalized not in MARKETING_STYLES:
        raise ValueError(f"Unknown tone: {normalized}. Choose from: {', '.join(MARKETING_STYLES)}.")
    return normalized


def analyze_customer(data):
    category = data.get("favorite_category")
    total_spending = data.get("total_spending")
    tone = data.get("tone")

    spending = _coerce_spending(total_spending)
    customer_segment = _determine_segment(spending)
    spending_level = _determine_spending_level(spending)
    loyalty_status = LOYALTY_BY_SEGMENT[customer_segment]
    discount_percentage = DISCOUNT_BY_SEGMENT[customer_segment]
    recommended_product = recommend_product(category, customer_segment)
    normalized_tone = _normalize_tone(tone)

    return {
        "customer_segment": customer_segment,
        "spending_level": spending_level,
        "loyalty_status": loyalty_status,
        "recommended_product": recommended_product,
        "discount_percentage": discount_percentage,
        "discount_message": f"Enjoy a special {discount_percentage}% discount on your next purchase.",
        "marketing_style": MARKETING_STYLES[normalized_tone],
        "cta": CTA_BY_TONE[normalized_tone],
    }

