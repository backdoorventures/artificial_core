def insert_affiliate_ctas(text: str, product: str = "Hostinger") -> str:
    if product.lower() == "hostinger":
        cta_block = """
---

## 🚀 Launch Your First Website Today

If you're a student or beginner looking to start a blog, portfolio, or side hustle, **Hostinger is one of the top-rated platforms** for getting started fast — and affordably.

It’s beginner-friendly, includes a free domain, and takes less than 10 minutes to go live.

👉 **[Click here to launch your website with Hostinger](https://your-affiliate-link.com/hosting)**  
🎯 No tech skills required. Perfect for your first online project.

---
"""
        return f"{text.strip()}\n\n{cta_block.strip()}"
    else:
        return text
