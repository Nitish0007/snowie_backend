import json
from ai.agent import ai_client
from ai.persona.snowie.system_prompt import build as build_snowie_system_prompt
from config.settings import MODEL_NAME, MAX_TOKENS

SNOWIE_SYSTEM_PROMPT = build_snowie_system_prompt()
MAX_ROUNDS = 5

class AIRouter:
    def __init__(self, plugins: list):
        self.plugins = {p.name: p for p in plugins}
        self.tool_index: dict[str, tuple] = {}  # "notion.search_page" -> (plugin, tool_name)

        for plugin in plugins:
            for tool in plugin.tools():
                full_name = f"{plugin.name}.{tool.name}"
                self.tool_index[full_name] = (plugin, tool.name)

    def _all_openai_tools(self) -> list[dict]:
        tools = []
        for plugin in self.plugins.values():
            tools.extend(plugin.openai_tools())
        return tools

    async def _execute_tool(self, full_name: str, arguments: dict) -> str:
        if full_name not in self.tool_index:
            return json.dumps({"error": f"Unknown tool: {full_name}"})

        plugin, tool_name = self.tool_index[full_name]
        handler = plugin.get_handler(tool_name)
        return await handler(**arguments)

    def _assistant_tool_message(self, message) -> dict:
        return {
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments or "{}",
                    },
                }
                for tool_call in (message.tool_calls or [])
            ],
        }

    async def _run_tool_calls(self, messages: list[dict], tool_calls) -> None:
        """Append assistant turn + tool result turns onto messages."""
        messages.append(self._assistant_tool_message(
            type("M", (), {"content": "", "tool_calls": tool_calls})()
        ))

        for call in tool_calls:
            try:
                args = json.loads(call.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
                print(f"Error parsing arguments for tool {call.function.name}: {call.function.arguments}")
            
            result = await self._execute_tool(call.function.name, args)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result,
            })

    async def route(self, user_text: str, history: list[dict] | None = None) -> str:
        """
        Run chat + tool loop until the model returns a final text reply.
        Flow:
          user → model → (tool_calls?) → execute tools → model → ... → final text
        """

        # build message with history and user input
        history = history or []
        tools = self._all_openai_tools()
        messages = [
            {"role": "system", "content": SNOWIE_SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": user_text},
        ]

        for _ in range(MAX_ROUNDS):
            kwargs = {
                "model": MODEL_NAME,
                "messages": messages,
                "max_tokens": MAX_TOKENS,
            }

            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"

            response = ai_client.chat.completions.create(**kwargs)
            message = response.choices[0].message

            if not message.tool_calls:
                return message.content or "I am not sure how to help you with that."

            messages.append(self._assistant_tool_message(message))

            for call in message.tool_calls:
                try:
                    args = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                    print(f"Error parsing arguments for tool {call.function.name}: {call.function.arguments}")
                
                result = await self._execute_tool(call.function.name, args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                })

        return "Too many rounds, please try again later."

        

            