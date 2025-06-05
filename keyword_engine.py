import requests
import csv
import os
from datetime import datetime

# File paths
AFFILIATE_CSV = "data/affiliate_products.csv"
USED_KEYWORDS_CSV = "data/used_keywords.csv"

# Google Autocomplete endpoint
GOOGLE_SUGGEST_URL = "https://suggestqueries.google.com/complete/search"

# Headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def load_affiliate_products():
    with open(AFFILIATE_CSV, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def save_used_keyword(keyword, brand):
    exists = os.path.isfile(USED_KEYWORDS_CSV)
    with open(USED_KEYWORDS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["keyword", "brand_name", "date_used"])
        writer.writerow([keyword, brand, datetime.now().strftime("%Y-%m-%d")])

def load_used_keywords():
    if not os.path.exists(USED_KEYWORDS_CSV):
        return set()
    with open(USED_KEYWORDS_CSV, newline='', encoding='utf-8') as f:
        return set(row["keyword"].strip().lower() for row in csv.DictReader(f))

def get_google_autocomplete_keywords(query):
    params = {
        "client": "firefox",
        "q": query
    }
    response = requests.get(GOOGLE_SUGGEST_URL, params=params, headers=HEADERS)
    response.raise_for_status()
    return response.json()[1]

def get_new_keyword():
    affiliates = load_affiliate_products()
    used_keywords = load_used_keywords()

    # Filter to the top-most unused product
    unused = [a for a in affiliates if a["used"].lower() == "false"]
    if not unused:
        raise Exception("No unused affiliate products available.")

    selected = unused[0]
    topic = selected["general_topic"]
    brand = selected["product_name"]

    suggestions = get_google_autocomplete_keywords(topic)

    for kw in suggestions:
        if kw.lower().strip() not in used_keywords:
            save_used_keyword(kw, brand)
            return kw, brand, topic

    raise Exception("No new keywords found. All suggestions already used.")

# Run once for testing
if __name__ == "__main__":
    keyword, brand, topic = get_new_keyword()
    print(f"✅ New Keyword: {keyword}\nBrand: {brand}\nTopic: {topic}")

