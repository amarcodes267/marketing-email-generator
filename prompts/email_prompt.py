def _format_purchase_history(purchase_history):
    items = [
        item.strip()
        for item in str(purchase_history or "").split("\n")
        if item.strip()
    ]
    return ", ".join(items) if items else "our products"


def build_email_prompt(data):
    customer = data["customer_name"]
    age = data["age"]
    gender = data["gender"]
    location = data["location"]
    purchase_summary = _format_purchase_history(data.get("purchase_history"))
    category = data.get("favorite_category", "Products")
    spending = f"{data['total_spending']:,.2f}"
    tone = data.get("tone", "Friendly")

    customer_segment = data.get("customer_segment", "New Customer")
    spending_level = data.get("spending_level", "Standard")
    loyalty_status = data.get("loyalty_status", "New")
    recommended_product = data.get("recommended_product", "a premium product")
    discount_percentage = data.get("discount_percentage", 5)
    marketing_style = data.get(
        "marketing_style",
        "Use a friendly, warm and casual conversational tone.",
    )
    cta = data.get("cta", "Shop today and enjoy your exclusive offer.")

    user_content = (
        f"Customer Profile\n"
        f"Name: {customer}\n"
        f"Age: {age}\n"
        f"Gender: {gender}\n"
        f"Location: {location}\n"
        f"Purchase History: {purchase_summary}\n"
        f"Favorite Category: {category}\n"
        f"Total Spending: Rs. {spending}\n\n"
        f"Marketing Insights\n"
        f"Customer Segment: {customer_segment}\n"
        f"Spending Level: {spending_level}\n"
        f"Loyalty Status: {loyalty_status}\n"
        f"Recommended Product: {recommended_product}\n"
        f"Personalized Discount: {discount_percentage}%\n"
        f"Marketing Style: {marketing_style}\n"
        f"Call To Action: {cta}\n\n"
        f"Write a {tone.lower()} marketing email to {customer} about {category} products.\n"
        f"The email must include an engaging subject line.\n"
        f"Mention the previous purchase of {purchase_summary}.\n"
        f"Recommend the related product {recommended_product}.\n"
        f"Offer a personalized {discount_percentage}% discount.\n"
        f"Match the tone and marketing style described above.\n"
        f"End the email with the call to action: {cta}\n"
        f"Write the email body in 100 to 120 words.\n"
        f"Do not use placeholders like [Name] or [Company].\n"
        f"Write the subject line first, then the email body.\n\n"
        f"Subject:"
    )

    return [
        {
            "role": "system",
            "content": "You are a marketing copywriter who writes concise personalized emails based on customer analytics.",
        },
        {"role": "user", "content": user_content},
    ]

