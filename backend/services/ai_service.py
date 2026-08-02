import re

from models.llm import ModelLoadError, generate_text, load_model
from prompts.email_prompt import build_email_prompt
from services.recommendation_service import recommend_product

SUBJECT_PATTERNS = [
    re.compile(r"\[\s*Subject(?:\s+Line)?\s*:\s*(.+?)\s*\]", re.IGNORECASE | re.DOTALL),
    re.compile(r"(?:Subject|Subject Line)\s*:\s*([^\n]+)", re.IGNORECASE),
]
GREETING_PATTERN = re.compile(
    r"^(?:Dear|Hey|Hi|Hello|Greetings|To)[^\n]*\n",
    re.IGNORECASE | re.MULTILINE,
)
NOISE_PATTERN = re.compile(
    r"\n\s*(?:(?:P\.S\.|P\.S:|Best Wishes|Warm regards|Regards|Yours faithfully|Sincerely|Thanks for being|Thank you for being|Image of|About Us|Contact Details|Your Company|Copyright|Unsubscribe|Follow us|Connect with us|Social media)[^\n]*)"
    r"|(?:\n\s*Best regards[^\n]*\n(?:[^\n]*\n){0,6})"
    r"|(?:\n\s*Cheers[^\n]*\n(?:[^\n]*\n){0,6})"
    r"|(?:\n\s*With love[^\n]*\n(?:[^\n]*\n){0,6})",
    re.IGNORECASE,
)
SIGNOFF_TAIL_PATTERN = re.compile(
    r"\s*(?:Sincerely|Regards|Best regards|Best Regards|Thanks|Cheers|With love)[^\n]*(\n.*)?$",
    re.IGNORECASE | re.DOTALL,
)
EMAIL_LINE_PATTERN = re.compile(
    r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$",
    re.IGNORECASE,
)
PHONE_LINE_PATTERN = re.compile(r"^\+?[\d\s()-]{8,}$")
PHONE_PATTERN = re.compile(r"\+?\d[\d\s().-]{7,}\d")
DOUBLE_ARTICLE_PATTERN = re.compile(
    r"\b(the|a|an)\s+(?:the|a|an)\s+", re.IGNORECASE
)
CONCATENATED_WORD_PATTERN = re.compile(r"([.!?])([A-Z])")
MIN_EMAIL_WORDS = 20
MAX_EMAIL_WORDS = 600
PLACEHOLDER_PATTERN = re.compile(r"\[.*?\]")
HASHTAG_PATTERN = re.compile(r"#\S+", re.IGNORECASE)
GAP_PATTERN = re.compile(
    r"(?:such as|like|including|at|visit|on|of|with|for the|a brand new|our new)\s+[,.;:]"
)
EXTRA_SPACE_PATTERN = re.compile(r"[ \t]{2,}")
EXTRA_COMMA_PATTERN = re.compile(r",\s*,")
INLINE_WHITESPACE_PATTERN = re.compile(r"[ \t]*\n[ \t]*")
EMPTY_GAP_PATTERN = re.compile(
    r"\b(?:such as|like|including|at|visit|on|of|with|for|the|a|an)\s*(?=[,.;:])",
    re.IGNORECASE,
)
PREPOSITION_BEFORE_END_PATTERN = re.compile(
    r"\b(?:such as|like|including|at|visit|on|of|with|for|the|a|an)\s+$",
    re.IGNORECASE,
)

def _get_placeholder_defaults(data):
    customer = data["customer_name"]
    category = data.get("favorite_category", "Products")
    segment = data.get("customer_segment", "New Customer")
    product = recommend_product(category, segment)
    discount_percentage = data.get("discount_percentage", 5)
    discount_label = f"{discount_percentage}%"
    discount_phrase = f"{discount_percentage}% off"
    defaults = {
        "name": customer,
        "customer name": customer,
        "customer's name": customer,
        "customer": customer,
        "john": customer,
        "sarah": customer,
        "priya": customer,
        "brand name": "ShopEasy",
        "your brand name": "ShopEasy",
        "your company name": "ShopEasy",
        "company name": "ShopEasy",
        "company": "ShopEasy",
        "brand": "ShopEasy",
        "product name": product,
        "product": product,
        "category": category,
        "sports product": product,
        "electronics product": product,
        "fashion product": product,
        "beauty product": product,
        "home decor product": product,
        "books product": product,
        "relevant product": product,
        "percent": discount_label,
        "percentage": discount_label,
        "discount": discount_label,
        "personalized discount": discount_phrase,
        "discount code": customer.upper()[:6],
        "coupon code": customer.upper()[:6],
        "code": customer.upper()[:6],
        "offer code": customer.upper()[:6],
        "insert coupon code": customer.upper()[:6],
        "insert coupon code here": customer.upper()[:6],
        "insert link to purchase page": "https://shopeasy.com",
        "insert email address": "support@shopeasy.com",
        "insert phone number": "+91-1800-123-4567",
        "insert social media handles": "@ShopEasy",
        "insert price in words": "five thousand",
        "insert discount amount in words": "one thousand",
        "insert date": "this week",
        "deadline": "this week",
        "valid until": "this weekend",
        "offer valid until": "this weekend",
        "expiry date": "this weekend",
        "last date": "this weekend",
        "your brand description and mission statement": "ShopEasy delivers premium products with exceptional service.",
        "your email": "support@shopeasy.com",
        "your phone number": "+91-1800-123-4567",
        "your name": "ShopEasy Team",
        "your email address": "support@shopeasy.com",
        "your company logo": "",
        "placeholder text": "",
        "close the email": "",
        "insert image or logo of nike shoes or sports product": "",
        "image of the dress and your logo": "",
        "image of john holding a pair of nike shoes": "",
        "image": "",
        "logo": "",
        "customer support": "support@shopeasy.com",
        "website": "https://shopeasy.com",
        "web address": "https://shopeasy.com",
        "link": "https://shopeasy.com",
        "social media": "@ShopEasy",
        "brands": "top brands",
        "product details": "detailed specifications",
        "features": "premium features",
        "pictures of the product": "",
        "image of the product": "",
        "product image": "",
        "your logo here": "",
        "logo here": "",
        "company logo here": "",
        "insert logo": "",
        "insert image": "",
        "insert product image": "",
        "store location": "shopeasy.com",
        "location": "shopeasy.com",
        "address": "shopeasy.com",
        "your physical address": "shopeasy.com",
        "customer service": "support@shopeasy.com",
        "customer care": "support@shopeasy.com",
        "telephone": "+91-1800-123-4567",
        "contact number": "+91-1800-123-4567",
        "email id": "support@shopeasy.com",
        "email address": "support@shopeasy.com",
    }
    return defaults


def _replace_placeholders(text, data):
    if text is None:
        return ""
    defaults = _get_placeholder_defaults(data)
    text = PLACEHOLDER_PATTERN.sub(
        lambda match: defaults.get(match.group(0)[1:-1].strip().lower(), ""),
        text,
    )
    customer = data["customer_name"]
    text = re.sub(
        r"\b" + re.escape(customer) + r"(?:'s|['\u2019]s) Name\b",
        customer,
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\b[A-Z][a-z]+['\u2019]s Name\b",
        customer,
        text,
    )
    text = re.sub(r"\b(?:Dear|Hey|Hi|Hello|Greetings)\s*,\s*$", "", text, flags=re.IGNORECASE | re.MULTILINE)
    return text


def _is_leftover_line(stripped):
    lowered = stripped.lower()
    if not stripped:
        return True
    if lowered in {"this week", "this weekend", "shopeasy", "shopeasy team", "sarah", "john", "priya", "marketing copywriter", "copywriter"}:
        return True
    if lowered.startswith("shopeasy"):
        return True
    if "@" in stripped or EMAIL_LINE_PATTERN.search(stripped):
        return True
    if PHONE_LINE_PATTERN.search(stripped) or stripped.startswith("+91"):
        return True
    if len(stripped.split()) == 1:
        return True
    return False


def _remove_leftover_lines(text):
    lines = text.split("\n")
    kept = []
    for line in lines:
        if line.strip() and not _is_leftover_line(line.strip()):
            kept.append(line)
        elif line.strip() and kept:
            previous_line = kept[-1].strip()
            if previous_line.endswith((".", "!", "?")):
                kept.append(line)
        elif not line.strip():
            kept.append("")
    return "\n".join(kept)


def _close_placeholder_gaps(text):
    text = GAP_PATTERN.sub(" ", text)
    text = EXTRA_COMMA_PATTERN.sub(",", text)
    text = EXTRA_SPACE_PATTERN.sub(" ", text)
    text = INLINE_WHITESPACE_PATTERN.sub("\n", text)
    text = EMPTY_GAP_PATTERN.sub(" ", text)
    text = re.sub(r"\.{2,}", ".", text)
    text = re.sub(r"\s+([.,;:])", r"\1", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = PREPOSITION_BEFORE_END_PATTERN.sub("", text)
    text = EXTRA_SPACE_PATTERN.sub(" ", text)
    return text


def _trim_edges(text):
    text = text.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _clean_text(text):
    text = HASHTAG_PATTERN.sub("", text)
    text = NOISE_PATTERN.sub("", text)
    text = SIGNOFF_TAIL_PATTERN.sub("", text)
    text = re.sub(r"^\s*Subject(?:\s+Line)?\s*:\s*", "", text, flags=re.IGNORECASE | re.MULTILINE)
    text = PLACEHOLDER_PATTERN.sub("", text)
    text = PHONE_PATTERN.sub("", text)
    text = DOUBLE_ARTICLE_PATTERN.sub(r"\1 ", text)
    text = CONCATENATED_WORD_PATTERN.sub(r"\1 \2", text)
    text = _close_placeholder_gaps(text)
    text = _remove_leftover_lines(text)
    text = _trim_edges(text)
    return text


def _truncate_body(text, max_words):
    words = text.split()
    if len(words) <= max_words:
        return text
    truncated = words[:max_words]
    joined = " ".join(truncated)
    last_sentence = max(
        joined.rfind(". "), joined.rfind("! "), joined.rfind("? ")
    )
    if last_sentence > len(joined) * 0.5:
        joined = joined[: last_sentence + 1]
    return joined.strip()


def _parse_generated_text(generated_text, data):
    text = generated_text.strip()

    for pattern in SUBJECT_PATTERNS:
        match = pattern.search(text)
        if match:
            subject = match.group(1).strip().split("\n")[0].strip()
            if subject:
                before = text[: match.start()].strip()
                after = text[match.end():].strip()
                remaining = before + "\n" + after if before else after
                remaining = remaining.strip()
                if remaining:
                    return subject, remaining

    greeting_match = GREETING_PATTERN.search(text)
    if greeting_match:
        customer = data["customer_name"]
        category = data["favorite_category"]
        fallback_subject = f"Exclusive Offer for {customer} on {category} Products"
        return fallback_subject, text

    if len(text.splitlines()) >= 2:
        first_line = text.split("\n", 1)[0].strip()
        rest = text.split("\n", 1)[1].strip()
        if first_line and rest:
            return first_line, rest

    return None, None


def generate_ai_email(data):
    try:
        prompt_messages = build_email_prompt(data)
    except Exception as error:
        return {"success": False, "message": f"Prompt generation failed: {error}"}

    try:
        load_model()
    except ModelLoadError as error:
        return {"success": False, "message": str(error)}
    except Exception as error:
        return {"success": False, "message": f"AI model initialization failed: {error}"}

    try:
        generated_text = generate_text(prompt_messages)
    except TimeoutError as error:
        return {"success": False, "message": str(error)}
    except Exception as error:
        return {"success": False, "message": f"AI generation failed: {error}"}

    parsed = _parse_generated_text(generated_text, data)
    if not parsed or parsed[0] is None or parsed[1] is None:
        return {
            "success": False,
            "message": "AI output could not be parsed into a valid subject and email. Please try again.",
        }

    subject, email_body = parsed
    subject = _replace_placeholders(subject, data)
    email_body = _replace_placeholders(email_body, data)
    email_body = _clean_text(email_body)

    if not subject or not email_body:
        return {
            "success": False,
            "message": "AI output could not be parsed into a valid subject and email. Please try again.",
        }

    word_count = len(email_body.split())
    if word_count < MIN_EMAIL_WORDS:
        return {
            "success": False,
            "message": "AI generated email was too short. Please try again.",
        }
    if word_count > MAX_EMAIL_WORDS:
        email_body = _truncate_body(email_body, MAX_EMAIL_WORDS)

    return {"success": True, "subject": subject, "email": email_body}

