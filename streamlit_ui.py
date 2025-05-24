import streamlit as st
from generator.prompt_builder import generate_blog_post
from generator.markdown_exporter import format_markdown
from generator.affiliate_inserter import insert_affiliate_links

st.set_page_config(page_title="Backdoor Blog Builder", layout="centered")

st.title("🛠️ Backdoor Blog Builder")
st.markdown("Generate SEO-optimized blog posts with affiliate injection.")

topic = st.text_input("Enter a blog topic:", max_chars=100)
tone = st.selectbox("Select tone:", ["professional", "conversational", "casual"])
tags_input = st.text_input("Tags (comma separated):", value="seo, automation, affiliate")
use_affiliate = st.checkbox("Insert affiliate links automatically")

if st.button("Generate Blog Post") and topic.strip():
    with st.spinner("Generating post..."):
        content = generate_blog_post(topic, tone=tone)
        if use_affiliate:
            content = insert_affiliate_links(content)
        markdown = format_markdown(topic.title(), content, [tag.strip() for tag in tags_input.split(",")])
    
    st.success("✅ Blog post generated!")
    st.code(markdown, language="markdown")
else:
    st.markdown("⚠️ Enter a topic to get started.")
