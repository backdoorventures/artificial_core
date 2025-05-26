def format_markdown(title: str, body: str, tags: list, summary: str = None) -> str:
    """
    Formats the post with Hugo-compatible YAML frontmatter.
    Automatically removes duplicate H1 (# title) from body.
    """
    frontmatter = {
        "title": str(title).strip('"'),
        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tags": tags
    }

    if summary:
        frontmatter["summary"] = summary.strip()

    yaml_header = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).strip()

    # 🧼 Strip duplicate H1 title from top of body if present
    body = body.strip()
    pattern = rf"^#\s*{re.escape(title.strip())}\s*\n*"
    body = re.sub(pattern, "", body, flags=re.IGNORECASE)

    markdown_body = body.strip()

    return f"---\n{yaml_header}\n---\n\n{markdown_body}"



