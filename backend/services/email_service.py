from services.ai_service import generate_ai_email
from services.personalization_service import analyze_customer


def _enrich_with_insights(data):
    insights = analyze_customer(data)
    enriched = dict(data)
    enriched.update(insights)
    return enriched


def _normalize_purchase_summary(purchase_history):
    items = [item.strip() for item in str(purchase_history or "").split("\n") if item.strip()]
    if not items:
        return "your recent purchase"
    return items[0] if len(items) == 1 else ", ".join(items[:2])


def _normalize_tone(tone):
    normalized = str(tone).strip() if tone else "Friendly"
    return normalized if normalized else "Friendly"


def _get_tone_variants(tone):
    mapping = {
        "Friendly": {
            "greeting": "Hi",
            "opening": "We wanted to share a special offer just for you.",
        },
        "Warm": {
            "greeting": "Hello",
            "opening": "We have a heartfelt offer tailored to your tastes.",
        },
        "Casual": {
            "greeting": "Hey",
            "opening": "We've got a great pick we think you'll love.",
        },
        "Conversational": {
            "greeting": "Hi",
            "opening": "Let's make your next shopping experience easy and fun.",
        },
        "Professional": {
            "greeting": "Hello",
            "opening": "We have a professional recommendation selected for you.",
        },
        "Formal": {
            "greeting": "Hello",
            "opening": "Please enjoy an exclusive offer crafted for you.",
        },
        "Luxury": {
            "greeting": "Hello",
            "opening": "Treat yourself to a premium choice today.",
        },
        "Urgent": {
            "greeting": "Hi",
            "opening": "Act quickly to claim this time-sensitive offer.",
        },
    }
    return mapping.get(tone, mapping["Friendly"])


def _render_rule_based_email(data):
    customer = data["customer_name"].strip()
    category = data.get("favorite_category", "Products")
    location = data.get("location", "")
    purchase_summary = _normalize_purchase_summary(data.get("purchase_history"))
    product = data.get("recommended_product", category)
    discount = data.get("discount_percentage", 5)
    cta = data.get("cta", "Shop today and enjoy your exclusive offer.")
    tone = _normalize_tone(data.get("tone"))
    variants = _get_tone_variants(tone)

    subject = f"{discount}% off {product} for {customer}"
    if category and category not in subject:
        subject = f"{discount}% off {product} in {category}"

    if location:
        location_phrase = f" in {location}"
    else:
        location_phrase = ""

    email_lines = [
        f"{variants['greeting']} {customer},",
        variants["opening"],
        f"Since you previously purchased {purchase_summary}, we think you’ll love {product} from our {category} collection{location_phrase}.",
        f"As a {data.get('loyalty_status', 'valued customer')}, you can enjoy {discount}% off on your next purchase.",
        cta,
        "Best regards,",
        "ShopEasy Team",
    ]

    email_body = "\n\n".join([line for line in email_lines if line])
    return {"success": True, "subject": subject, "email": email_body, "used_fallback": True}


def generate_email(data):
    enriched_data = _enrich_with_insights(data)
    ai_result = generate_ai_email(enriched_data)
    if ai_result.get("success"):
        return ai_result

    fallback_result = _render_rule_based_email(enriched_data)
    fallback_result["fallback_reason"] = ai_result.get("message", "AI generation failed.")
    return fallback_result

