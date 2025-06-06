def build_launchlayer_prompt(
    keyword: str,
    video_id: str,
    row: dict,
    word_count: int = 1200
) -> str:
    """
    Builds an SEO-optimized blog post prompt using data from the affiliate row.
    """

    product_name = row["product_name"]
    affiliate_link = row["affiliate_link"]
    product_brain = row["brain"]

    return f"""
You are a world-class SEO content writer working for LaunchLayer — a clean, modern tech review site.

Write a full-length blog post based on the keyword: **"{keyword}"**  
The product being reviewed is: **{product_name}**

You have internal documentation for reference:
'''
{product_brain}
'''

Use this “brain” as your only source of truth. Mention specific features, strengths, limits, use cases, etc. Write as if you’ve personally used the tool.

## Style & Structure:
- Tone: clean, confident, professional (not hype, not robotic)
- Length: ~{word_count} words
- Use H1 for the title, H2s for major sections
- Use bullet points or numbered lists when appropriate
- **Never** include markdown links or `[text](url)` — CTA buttons will be handled by the system
- Mention the product name naturally throughout
- Use the keyword early and 3–4 more times in a natural way

## Required Content Sections:
1. SEO-optimized intro paragraph using the keyword
2. Full feature breakdown based on the product brain
3. Clear explanation of pricing or free limits
4. Comparison to common competitors
5. Bullet list of ideal use cases
6. Final thoughts with subtle push toward action

## Embedded:
- A YouTube video will be embedded like this: `{{< youtube {video_id} >}}`
- A CTA button will be auto-inserted with:
    - Text: Try {product_name} or Check out {product_name}
    - URL: {affiliate_link}
    - Position: both

Return **only** the markdown body content. No frontmatter. No instructions. No disclaimers.
"""
