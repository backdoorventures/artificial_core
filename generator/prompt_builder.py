def build_prompt(topic: str, tone: str = "professional", word_count: int = 1200) -> str:
    """
    Returns a GPT-ready prompt string to generate a blog post.
    """
    return (
        f"Write a {tone}, SEO-optimized blog post of around {word_count} words "
        f"on the topic: '{topic}'. Use clear H1 and H2 subheadings, bullet points, and natural keyword placement. "
        f"Make it helpful, engaging, and easy to read. Avoid fluff, and include a strong intro and conclusion."
    )


