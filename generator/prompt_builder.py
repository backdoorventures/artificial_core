import openai
import streamlit as st

def generate_blog_post(topic: str, tone: str = "professional", word_count: int = 1200) -> str:
    prompt = (
        f"Write a {tone}, SEO-optimized blog post of about {word_count} words "
        f"on the topic: '{topic}'. Use subheadings, bullet points, and make it "
        f"engaging and helpful. Format it for easy reading and avoid fluff."
    )

    openai.api_key = st.secrets["OPENAI_API_KEY"]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

