TONE_STYLES = {
    "Professional": {
        "greeting": "Dear",
        "signoff": "Best regards",
        "body_prefix": "We are pleased to inform you about our latest offerings tailored to your preferences."
    },
    "Friendly": {
        "greeting": "Hey",
        "signoff": "Cheers",
        "body_prefix": "We hope you are doing great! We have something special just for you."
    },
    "Luxury": {
        "greeting": "Dear",
        "signoff": "Yours sincerely",
        "body_prefix": "It is our privilege to present you with an exclusive selection curated to your exquisite taste."
    },
    "Exciting": {
        "greeting": "Hello",
        "signoff": "See you soon",
        "body_prefix": "Get ready! We have some amazing news that will make your day."
    }
}

CATEGORY_ADJECTIVES = {
    "Fashion": "stylish",
    "Electronics": "cutting-edge",
    "Books": "bestselling",
    "Sports": "high-performance",
    "Home Decor": "elegant",
    "Beauty": "premium"
}


def generate_subject(customer_name):
    return f"Exclusive Offer for {customer_name}"


def generate_email_body(data):
    tone = TONE_STYLES.get(data["tone"], TONE_STYLES["Professional"])
    adjective = CATEGORY_ADJECTIVES.get(data["favorite_category"], "amazing")
    purchase_items = data["purchase_history"].strip().split("\n")
    purchase_items = [item.strip() for item in purchase_items if item.strip()]
    purchase_str = purchase_items[0] if purchase_items else "our products"
    spending_formatted = f"₹{data['total_spending']:,.2f}"

    body = f"{tone['greeting']} {data['customer_name']},\n\n"
    body += f"{tone['body_prefix']}\n\n"
    body += f"Thank you for purchasing {purchase_str}.\n\n"
    body += f"We appreciate your interest in {data['favorite_category']} products.\n\n"
    body += f"Because you are one of our valued customers from {data['location']}, we have prepared exciting offers especially for you.\n\n"
    body += f"As a valued customer with a total spending of {spending_formatted}, we want to make sure you get the best experience with our {adjective} {data['favorite_category'].lower()} collection.\n\n"
    body += "We hope to see you again soon.\n\n"
    body += f"{tone['signoff']},\n"
    body += "Marketing Team"

    return body


def generate_email(data):
    subject = generate_subject(data["customer_name"])
    body = generate_email_body(data)
    return {
        "success": True,
        "subject": subject,
        "email": body
    }

