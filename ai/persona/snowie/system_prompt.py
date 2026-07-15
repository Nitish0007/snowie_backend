from ai.persona.snowie.role import ROLE, render_role
from ai.persona.snowie.output_hygiene import OUTPUT_HYGIENE, render_output_hygiene
# from ai.persona.snowie.emotions import get_emotions, RENDERERS, DEFAULT_EMOTIONS

# Always-on modules (add rules.py, security.py here later)
ALWAYS_ACTIVE_RENDERERS = [
    render_role,
    render_output_hygiene,
]

ALWAYS_ACTIVE_DATA = [
    ROLE,
    OUTPUT_HYGIENE,
]


def build(
    # active_emotions: list[str] | None = None,
    user_name: str | None = None,
    include_tool_rules: bool = True,
):
    role = {**ROLE, "user": {**ROLE["user"]}}
    if user_name:
        role["user"]["name"] = user_name

    parts: list[str] = []

    # 1. Always-active modules
    parts.append(render_role(role))
    parts.append(render_output_hygiene(OUTPUT_HYGIENE))

    # 2. Active emotions
    # emotion_ids = active_emotions if active_emotions is not None else DEFAULT_EMOTIONS
    # for emotion in get_emotions(emotion_ids):
    #     renderer = RENDERERS.get(emotion["id"])
    #     if renderer:
    #         parts.append(renderer(emotion))

    # 3. Tool rules (temporary — move to rules.py later)
    if include_tool_rules:
        parts.append(_tool_rules_block())

    return "\n\n".join(parts)


def _tool_rules_block() -> str:
    return """[CHAT vs TOOLS]
You have two modes:
CHAT (no tools):
- Greetings, small talk, identity ("who are you"), feelings, advice, general questions
- Answer directly as Snowie from your persona
- Do NOT call any tool
TOOLS (use plugins):
- Only when the user wants something from an external service
- Examples: check Notion schedule, find a page, read workspace data, etc.
Rules:
1. Default to CHAT unless the user clearly needs external data or an action.
2. "Who are you", "hi", "how are you" → always CHAT, never use tools.
3. Only say you can't help when the user asked for a specific action that no tool supports.
4. Never mention tools, plugins, or "no tool available" in your reply.
5. Keep responses natural and concise.
6. Don't use the Mode in which you are (CHAT or TOOLS) in your response at all."""