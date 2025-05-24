import re

# Map your keywords to affiliate links
AFFILIATE_LINKS = {
    "hosting": "https://your-affiliate-link.com/hosting",
    "VPN": "https://your-affiliate-link.com/vpn",
    "password manager": "https://your-affiliate-link.com/password-manager",
    "email marketing": "https://your-affiliate-link.com/email-marketing",
    "AI writing tool": "https://your-affiliate-link.com/ai-writer"
}

def insert_affiliate_links(text: str) -> str:
    for keyword, url in AFFILIATE_LINKS.items():
        # Only replace plain text, not already-linked keywords
        pattern = rf"(?<!\]\()(?<!href=\")\b({re.escape(keyword)})\b"
        replacement = rf"[\1]({url})"
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

