from openai import OpenAI
import os

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_title(script_text, keyword):
    prompt = (
        f"You are writing a short, cinematic YouTube title for a video targeting the keyword: \"{keyword}\".\n\n"
        f"The full video script is:\n'''\n{script_text}\n'''\n\n"
        "Rules:\n"
        "- Must be under 80 characters\n"
        "- Must include or relate to the keyword naturally\n"
        "- No emojis, no hashtags, no hype\n"
        "- Write in title case\n"
        "- Make it sound like a premium launch video or futuristic product drop\n\n"
        "Return only the title."
    )

    res = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60
    )
    return res.choices[0].message.content.strip()

