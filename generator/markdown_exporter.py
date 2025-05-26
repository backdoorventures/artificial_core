from datetime import datetime
import yaml
import re

def slugify(text: str) -> str:
    """
    Converts a title into a clean URL slug.
    Example: 'Best Hosting in 2025!' → 'best-hosting-in-2025'
    """
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)  # remove punctuation
    text = re.sub(r"[\s_]+", "-", text)   # replace spaces/underscores with dashes
    return text.strip("-")

def format_markdown(title: str, body: str, tags: list, summary: str = None) -> str:
    """
    Formats the post with Hugo-compatible YAML frontmatter.
    """
    frontmatter = {
        "title": str(title).strip('"'),
        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tags": tags
    }

    if summary:
        frontmatter["summary"] = summary.strip()

    yaml_header = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).strip()
    markdown_body = body.strip()

    return f"---\n{yaml_header}\n---\n\n{markdown_body}"

def export_markdown(title: str, body: str, tags: str, summary: str = None) -> tuple:
    """
    Converts the input into a slugged Hugo .md file and returns:
    (filename, markdown_string)
    """
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    markdown_str = format_markdown(title, body, tag_list, summary)
    filename = f"{slugify(title)}.md"
    return filename, markdown_str


