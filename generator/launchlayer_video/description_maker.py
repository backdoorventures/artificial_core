from openai import OpenAI
import os

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_description(keyword, script_text):
    prompt = (
        f"You are a world-class SEO content strategist working for a futuristic tech brand called LaunchLayer.\n\n"
        f"Your task is to generate a high-converting, SEO-optimized YouTube video description based on the keyword: \"{keyword}\".\n\n"
        "The voiceover script is:\n"
        f"'''\n{script_text}\n'''\n\n"
        "Your description must:\n"
        "- Start with a keyword-rich hook (1–2 sentences)\n"
        "- Include 2 full paragraphs packed with related semantic phrases\n"
        "- Naturally use the keyword at least 3–4 times\n"
        "- Include long-tail variations and industry buzzwords\n"
        "- Position LaunchLayer as a trusted voice in emerging tech reviews\n"
        "- End with a strong CTA and clean list of links\n\n"
        "Format:\n"
        "1. Cinematic intro paragraph\n"
        "2. Body paragraph with rich keyword context and future-facing tone\n"
        "3. CTA paragraph with these 3 links formatted clearly:\n"
        "- Website: https://launchlayer.tech\n"
        "- Blog: https://launchlayer.tech/blog\n"
        "- Medium: https://medium.com/@launchlayer\n\n"
        "Do NOT use hashtags or emojis. Use spacing for clarity. Keep it tight, clean, and optimized for ranking."
    )

    res = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=450
    )
    return res.choices[0].message.content.strip()
