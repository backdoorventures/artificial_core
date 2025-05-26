import streamlit as st
from generator.prompt_builder import build_prompt
from generator.affiliate_inserter import insert_affiliate_ctas
from generator.markdown_exporter import export_markdown
import openai
import os

# Load secrets from Streamlit (or use env)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit Config
st.set_page_config(page_title="Backdoor Blog Builder", layout="centered")
st.title("🚀 Backdoor Blog Builder")
st.markdown("Generate SEO-optimized affiliate blog posts with one click.")

# Inputs
keyword = st.text_input("🎯 Keyword (e.g. best web hosting for students 2025):")
tone = st.selectbox("🗣️ Tone", ["professional", "conversational", "casual"])
tags = st.text_input("🏷️ Tags (comma separated)", value="seo, affiliate, blogging")
include_cta = st.checkbox("✅ Insert Hostinger CTA", value=True)

# Generate
if st.button("Generate Post") and keyword.strip():
    with st.spinner("Generating post..."):

        # Step 1: Build prompt
        prompt = build_prompt(keyword, tone)

        # Step 2: Call GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response['choices'][0]['message']['content']

        # Step 3: Insert CTA if checked
        if include_cta:
            content = insert_affiliate_ctas(content, product="Hostinger")

        # Step 4: Export .md
        filename, markdown_output = export_markdown(
            title=keyword.title(),
            body=content,
            tags=tags
        )

        # Step 5: Display
        st.success("✅ Blog post generated!")
        st.download_button("📥 Download Markdown", markdown_output, file_name=filename)
        st.code(markdown_output, language="markdown")

else:
    st.markdown("⚠️ Enter a keyword to generate content.")
