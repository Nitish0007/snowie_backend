def render_lines(title: str, items: list[str]) -> str:
    body = "\n".join(f"- {item}" for item in items)
    return f"[{title}]\n{body}"

def render_examples_user_assistant(examples: list[dict]) -> str:
  lines = []
  for ex in examples:
    if "user" in ex and "assistant" in ex:
      lines.append(f'User: "{ex["user"]}"')
      lines.append(f'AI: "{ex["assistant"]}"')
    elif ex.get("role") == "user":
      lines.append(f'User: "{ex["content"]}"')
    elif ex.get("role") == "assistant":
      lines.append(f'AI: "{ex["content"]}"')
  return "\n".join(lines)

def render_bad_good_examples(examples: list[dict]) -> str:
  lines = []
  for ex in examples:
    lines.append(f'BAD: {ex["bad"]}')
    lines.append(f'GOOD: {ex["good"]}')
  return "\n".join(lines)