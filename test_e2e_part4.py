import sys
import os

PROJECT_DIR = r"c:/Users/HELLO/Desktop/genai-marketing-copy"
sys.path.insert(0, PROJECT_DIR)
os.chdir(PROJECT_DIR)

from services.email_service import generate_email

profiles = [
    {
        "customer_name": "John",
        "age": 28,
        "gender": "Male",
        "location": "Mumbai",
        "purchase_history": "Nike Shoes\nGym Gloves",
        "favorite_category": "Sports",
        "total_spending": 35000,
        "tone": "Friendly",
    },
    {
        "customer_name": "Sarah",
        "age": 24,
        "gender": "Female",
        "location": "Delhi",
        "purchase_history": "Laptop\nHeadphones",
        "favorite_category": "Electronics",
        "total_spending": 4000,
        "tone": "Professional",
    },
    {
        "customer_name": "Priya",
        "age": 32,
        "gender": "Female",
        "location": "Bangalore",
        "purchase_history": "Designer Dress\nHeels",
        "favorite_category": "Fashion",
        "total_spending": 70000,
        "tone": "Luxury",
    },
]

for profile in profiles:
    print("=" * 60)
    print("PROFILE:", profile["customer_name"], "/", profile["favorite_category"], "/", profile["tone"], "/", profile["total_spending"])
    result = generate_email(profile)
    if result.get("success"):
        print("SUBJECT:", result["subject"])
        print("EMAIL:")
        print(result["email"])
    else:
        print("ERROR:", result.get("message"))
    print()

print("ALL TESTS COMPLETE")

