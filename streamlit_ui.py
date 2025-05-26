import streamlit as st
from openai import OpenAI
from generator.prompt_builder import build_prompt
from generator.affiliate_inserter import insert_affiliate_ctas
from generator.markdown_exporter import export_markdown
from generator.push_to_git import push_post_to_github

# === Initialize OpenAI Client (SDK v1.23.2) ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Optional: Uncomment this if you ever need to specify a different base_url (e.g., proxy or local server)
# client = client.with_options(base_url="https://api.openai.com/v1")

# === Streamlit UI Config ===
st.set_page_config(page_title="Backdoor Blog Builder", layout="centered")
st.title("🚀 Backdoor Blog Builder")
st.markdown("Generate SEO-optimized affiliate blog posts with one click.")

# === Inputs ===
keyword = st.text_input("🎯 Keyword (e.g. best web hosting for students 2025):")
tone = st.selectbox("🗣️ Tone", ["professional", "conversational", "casual"])
tags = st.text_input("🏷️ Tags (comma separated)", value="seo, affiliate, blogging")
include_cta = st.checkbox("✅ Insert Hostinger CTA", value=True)

# === Generate Button ===
if st.button("Generate Post") and keyword.strip():
    with st.spinner("🧠 Generating your blog post..."):
        prompt = build_prompt(keyword, tone)

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            content = response.choices[0].message.content.strip()

        except Exception as e:
            st.error("💥 OpenAI generation failed.")
            st.exception(e)
            st.stop()

        if include_cta:
            content = insert_affiliate_ctas(content, product="Hostinger")

        filename, markdown_output = export_markdown(
            title=keyword.title(),
            body=content,
            tags=tags
        )

        st.success("✅ Blog post generated!")
        st.download_button("📥 Download Markdown", markdown_output, file_name=filename)
        st.code(markdown_output, language="markdown")

        success, msg = push_post_to_github(filename, markdown_output)
        st.info(msg)

else:
    st.markdown("⚠️ Enter a keyword and click 'Generate Post' to begin.")









