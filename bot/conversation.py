MAX_TURNS = 10

def get_history(context) -> list[dict]:
  return context.chat_data.setdefault('messages', [])

def append_turn(context, user_text: str, assistant_text: str) -> None:
  history = get_history(context)
  history.append({"role": "user", "content": user_text})
  history.append({"role": "assistant", "content": assistant_text})
  max_messages = MAX_TURNS * 2
  while len(history) > max_messages:
    context.chat_data["messages"] = history[-max_messages:]

def clear_history(context) -> None:
  context.chat_data["messages"] = []