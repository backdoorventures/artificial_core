from datetime import datetime
import yaml
from .utils import slugify  # if you have this, otherwise I’ll give you a fallback

def format_markdown(title: str, body: str, tags: list) -> str:
    frontmatter = {
        "title": title,
        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tags": tags
    }

    yaml_header = yaml.dump(frontmatter, default_flow_style=False).strip()
    return f"---\n{yaml_header}\n---\n\n{body.strip()}"

def export_markdown(title: str, body: str, tags: str) -> tuple:
    """
    Converts input into Hugo-ready markdown with frontmatter and returns:
    (filename, markdown_string)
    """
    tag_list = [tag.strip() for tag in tags.split(",")]
    markdown_str = format_markdown(title, body, tag_list)

    # Create slug-based filename
    slug = title.lower().replace(" ", "-").replace("?", "").replace(":", "")
    filename = f"{slug}.md"

    return filename, markdown_str
