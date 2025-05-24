from datetime import datetime
import yaml

def format_markdown(title: str, body: str, tags: list) -> str:
    frontmatter = {
        "title": title,
        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tags": tags
    }

    yaml_header = yaml.dump(frontmatter, default_flow_style=False).strip()
    return f"---\n{yaml_header}\n---\n\n{body.strip()}"
