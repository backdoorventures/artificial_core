from datetime import datetime
import yaml
import re

def slugify(text: str) -> str:
    """
    Converts a title into a clean URL slug.
    Example: 'Best Hosting in 2025!' → 'best-hosting-in-2025'
    """
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)          # remove special characters
    text = re.sub(r"[\s_]+", "-", text)           # replace spaces/underscores with dash
    return text.strip("-")

def format_markdown(title: str, body: str, tags: list) -> str:
    """
    Adds Hugo-compatible frontmatter to the blog post body.
    """
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
    slug = slugify(title)
    filename = f"{slug}.md"
    return filename, markdown_str

