import sys

from prompts.email_prompt import build_email_prompt
from services.personalization_service import analyze_customer

PROFILES = [
    {
        "name": "John",
        "data": {
            "customer_name": "John",
            "age": 28,
            "gender": "Male",
            "location": "Mumbai",
            "purchase_history": "Nike Shoes\nGym Gloves",
            "favorite_category": "Sports",
            "total_spending": 35000,
            "tone": "Friendly",
        },
        "expected_segment": "Premium Customer",
        "expected_discount": 15,
        "expected_product": "Performance Running Shoes",
        "expected_level": "Premium",
        "expected_loyalty": "Gold",
    },
    {
        "name": "Sarah",
        "data": {
            "customer_name": "Sarah",
            "age": 24,
            "gender": "Female",
            "location": "Delhi",
            "purchase_history": "Laptop\nHeadphones",
            "favorite_category": "Electronics",
            "total_spending": 4000,
            "tone": "Professional",
        },
        "expected_segment": "New Customer",
        "expected_discount": 5,
        "expected_product": "Wireless Earbuds",
        "expected_level": "Budget",
        "expected_loyalty": "New",
    },
    {
        "name": "Priya",
        "data": {
            "customer_name": "Priya",
            "age": 32,
            "gender": "Female",
            "location": "Bangalore",
            "purchase_history": "Designer Dress\nHeels",
            "favorite_category": "Fashion",
            "total_spending": 70000,
            "tone": "Luxury",
        },
        "expected_segment": "VIP Customer",
        "expected_discount": 20,
        "expected_product": "Premium Jacket",
        "expected_level": "Premium",
        "expected_loyalty": "Platinum",
    },
]


def run_assertions():
    failures = []
    for profile in PROFILES:
        insights = analyze_customer(profile["data"])
        checks = [
            ("customer_segment", profile["expected_segment"]),
            ("discount_percentage", profile["expected_discount"]),
            ("recommended_product", profile["expected_product"]),
            ("spending_level", profile["expected_level"]),
            ("loyalty_status", profile["expected_loyalty"]),
        ]
        for field, expected in checks:
            actual = insights[field]
            if actual != expected:
                failures.append(
                    f"{profile['name']}: {field} expected '{expected}', got '{actual}'"
                )
        if not insights["discount_message"] or str(insights["discount_percentage"]) not in insights["discount_message"]:
            failures.append(f"{profile['name']}: discount_message missing percentage")
        if not insights["marketing_style"]:
            failures.append(f"{profile['name']}: marketing_style empty")
        if not insights["cta"]:
            failures.append(f"{profile['name']}: cta empty")

        enriched = dict(profile["data"])
        enriched.update(insights)
        messages = build_email_prompt(enriched)
        joined_prompt = messages[0]["content"] + "\n" + messages[1]["content"]
        required_parts = [
            profile["expected_product"],
            f"{profile['expected_discount']}%",
            profile["expected_segment"],
            insights["cta"],
        ]
        for part in required_parts:
            if part not in joined_prompt:
                failures.append(f"{profile['name']}: prompt missing '{part}'")

    if failures:
        print("PERSONALIZATION TESTS FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("PERSONALIZATION TESTS PASSED")
    for profile in PROFILES:
        insights = analyze_customer(profile["data"])
        print(f"  {profile['name']}: {insights['customer_segment']} | {insights['spending_level']} | {insights['loyalty_status']} | {insights['recommended_product']} | {insights['discount_percentage']}% | cta={insights['cta']}")
    return 0


if __name__ == "__main__":
    sys.exit(run_assertions())

