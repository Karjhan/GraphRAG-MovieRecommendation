def filter_to_context(answer: str, context: str):
    allowed_titles = []

    for line in context.split("\n"):
        if line.startswith("Movie:"):
            allowed_titles.append(line.replace("Movie:", "").strip())

    filtered_lines = []

    for line in answer.split("\n"):
        if any(title in line for title in allowed_titles):
            filtered_lines.append(line)

    return "\n".join(filtered_lines) if filtered_lines else answer