def build_launchlayer_prompt(keyword: str, brand: str, affiliate_link: str, video_id: str, word_count: int = 1200) -> str:
    """
    Builds a full SEO-optimized blog post prompt for LaunchLayer long-form content.
    """

    return f"""
You are a senior SEO copywriter working for LaunchLayer — a futuristic review site that publishes high-conversion blog posts built around affiliate products.

Write a detailed, helpful blog post about the keyword: **"{keyword}"**. The brand being promoted is **{brand}**.

## Formatting Rules:
- Write in a natural, high-authority tone (not robotic, not hype)
- Must be approx. {word_count} words
- Use **H1 for the title**, and **H2s for major sections**
- Include **bullet points or numbered lists** where useful
- NEVER use inline hyperlinks — CTA is handled by our button system
- Mention the product/brand name often and naturally
- Write like a trusted expert helping readers make a smart decision

## Required Structure:
1. **Cinematic intro paragraph** — hard-hitting, no fluff
2. **Feature breakdown** — detailed list of what the product offers
3. **Pricing + Free Plan clarity** — highlight limits, usage caps, etc.
4. **Comparison to typical alternatives** — can be text or table format
5. **Use cases** — bullet list of who this is best for
6. **Final thoughts** — summary that reinforces value and encourages action
7. **DO NOT include affiliate links or buttons — we insert them**

## Additional:
- Assume a YouTube video will be embedded via `{{< youtube {video_id} >}}`
- CTA buttons will be inserted via this config:
    - Text: Try {brand}
    - URL: {affiliate_link}
    - Position: both

Write the blog post body only. No frontmatter. No formatting instructions. Just clean markdown-ready content.
"""
