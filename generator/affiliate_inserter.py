def insert_affiliate_ctas(text: str, product: str = "Hostinger") -> str:
    if product.lower() == "hostinger":
        cta_block = """
---

## 🚀 Ready to Launch Your Website?

If you're a student or beginner looking to start a blog, portfolio, or business in 2025, **Hostinger is the easiest and most affordable way to go live today.**

Thousands of beginners trust Hostinger for its fast setup, free domain, and simple dashboard — without needing tech skills.

👉 **[Click here to launch your site with Hostinger now](https://your-affiliate-link.com/hosting)**  
💡 You can be online in less than 10 minutes.

Still unsure? [Read why I recommend Hostinger](https://your-affiliate-link.com/hosting) — it’s the same platform I use to run this blog.

---
"""
        return f"{text.strip()}\n\n{cta_block.strip()}"
    else:
        return text
