from services.ai_service import generate_ai_email
from services.personalization_service import analyze_customer


def _enrich_with_insights(data):
    insights = analyze_customer(data)
    enriched = dict(data)
    enriched.update(insights)
    return enriched


def generate_email(data):
    enriched_data = _enrich_with_insights(data)
    return generate_ai_email(enriched_data)

