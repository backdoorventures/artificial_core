import streamlit as st
from openai import OpenAI
from generator.prompt_builder import build_prompt
from generator.affiliate_inserter import insert_affiliate_ctas
from generator.markdown_exporter import export_markdown
from generator.push_to_git import push_post_to_github

# ===== ✅ Load OpenAI API Key Safely =====
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OpenAI API key is missing in Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# ===== ✅ Streamlit UI Config =====
st.set_page_config(page_title="Backdoor Blog Builder", layout="centered")
st.title("🚀 Backdoor Blog Builder")
st.markdown("Generate SEO-optimized affiliate blog posts with one click.")

# ===== ✅ User Inputs =====
keyword = st.text_input("🎯 Keyword (e.g. best web hosting for students 2025):")
tone = st.selectbox("🗣️ Tone", ["professional", "conversational", "casual"])
tags = st.text_input("🏷️ Tags (comma separated)", value="seo, affiliate, blogging")
include_cta = st.checkbox("✅ Insert Hostinger CTA", value=True)

# ===== ✅ Generate Blog Post =====
if st.button("Generate Post") and keyword.strip():
    with st.spinner("🧠 Generating your blog post..."):

        # Step 1: Build prompt
        prompt = build_prompt(keyword, tone)

        # Step 2: Call GPT via OpenAI V1
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            content = response.choices[0].message.content
        except Exception as e:
            st.error(f"❌ OpenAI API call failed: {e}")
            st.stop()

        # Step 3: Inject affiliate CTA
        if include_cta:
            content = insert_affiliate_ctas(content, product="Hostinger")

        # Step 4: Format markdown
        filename, markdown_output = export_markdown(
            title=keyword.title(),
            body=content,
            tags=tags
        )

        # Step 5: Show results
        st.success("✅ Blog post generated!")
        st.download_button("📥 Download Markdown", markdown_output, file_name=filename)
        st.code(markdown_output, language="markdown")

        # Step 6: Push to GitHub
        success, msg = push_post_to_github(filename, markdown_output)
        st.info(msg)

else:
    st.markdown("⚠️ Enter a keyword and click 'Generate Post' to begin.")



