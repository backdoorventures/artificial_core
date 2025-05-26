def build_prompt(topic: str, tone: str = "professional", word_count: int = 1200) -> str:
    """
    Builds a high-conversion, SEO-optimized blog post prompt for GPT.
    """
    return (
        f"Write a {tone} blog post that is SEO-optimized and approximately {word_count} words long. "
        f"The topic is: '{topic}'.\n\n"
        f"Structure the content using H1 for the main title and H2 for key sections. "
        f"Use bullet points or numbered lists where helpful. Write with a natural, helpful tone as if speaking directly to the reader.\n\n"
        f"Include:\n"
        f"- A compelling introduction that hooks the reader\n"
        f"- Key benefits, use cases, and comparisons (if relevant)\n"
        f"- Clear sectioning with headers\n"
        f"- A FAQ section with 3–5 concise, valuable questions and answers\n"
        f"- A strong conclusion summarizing the key points\n\n"
        f"Include natural keyword placement, but avoid keyword stuffing. Write like a real person who has experience with this topic.\n\n"
        f"Do not mention that you are an AI or refer to the prompt. Just deliver the article."
    )
