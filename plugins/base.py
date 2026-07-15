from dataclasses import dataclass
from typing import Any, Awaitable, Callable

ToolHandler = Callable[..., Awaitable[str]]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]   # JSON Schema
    handler: ToolHandler


class BasePlugin:
    name: str = ""
    description: str = ""

    def tools(self) -> list[Tool]:
        raise NotImplementedError

    def openai_tools(self) -> list[dict]:
        """What the model actually sees."""
        return [
            {
                "type": "function",
                "function": {
                    # namespaced: notion.search_page
                    "name": f"{self.name}.{tool.name}",
                    "description": f"{self.description}. {tool.description}",
                    "parameters": tool.parameters,
                },
            }
            for tool in self.tools()
        ]

    def get_handler(self, tool_name: str) -> ToolHandler | None:
        for tool in self.tools():
            if tool.name == tool_name:
                return tool.handler
        return None