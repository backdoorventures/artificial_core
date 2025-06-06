from openai import OpenAI
import os

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def expand_keyword_to_script(keyword):
    SYSTEM_PROMPT = (
        "You are a high-end narrator and scriptwriter for a modern tech-forward brand called LaunchLayer.\n\n"
        "Your job is to take a product-related keyword (like 'best AI funnel builder') and turn it into a cinematic narration that feels like a 2-minute launch video.\n\n"
        "Tone: confident, clean, futuristic — like a voiceover in an Apple keynote or AI startup film.\n\n"
        "Rules:\n"
        "- Mention the keyword clearly in the first sentence\n"
        "- Never use questions, hype, filler, or intro fluff\n"
        "- Do NOT say 'this video' or 'this product'\n"
        "- Speak naturally about the topic with clarity and momentum\n"
        "- Use analogies, strong pacing, and poetic logic when helpful\n"
        "- Target word count: **280 to 320 words** (approx. 2 minutes voiceover)\n\n"
        f"Keyword: {keyword}\n"
        "Write a complete script narration based on this keyword."
    )

    res = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}],
        max_tokens=700,
        temperature=0.7
    )
    return res.choices[0].message.content.strip()

