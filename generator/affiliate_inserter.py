def insert_affiliate_ctas(text: str, product: str = "Hostinger") -> str:
    if product.lower() == "hostinger":
        cta_block = """
---

## 🌐 Ready to Launch Your Website?

If you're a student looking for reliable, affordable hosting, I recommend [Hostinger](https://your-affiliate-link.com/hosting). It's what I use, and it’s perfect for beginners.

👉 [Click here to get started with Hostinger](https://your-affiliate-link.com/hosting)

---
"""
        return f"{text.strip()}\n\n{cta_block.strip()}"
    else:
        return text


