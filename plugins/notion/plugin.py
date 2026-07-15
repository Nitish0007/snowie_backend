import json
from plugins.base import BasePlugin, Tool
from plugins.notion.client import NotionClient


class NotionPlugin(BasePlugin):
    name = "notion"
    description = "Read and analyze pages from Notion workspace"

    def __init__(self, client: NotionClient):
        self.client = client

    async def _search_page(self, query: str) -> str:
        pages = await self.client.search_pages(query)
        if not pages:
            return json.dumps({"found": False, "pages": []})

        simplified = [
            {
                "id": p["id"],
                "title": self._extract_title(p),
                "url": p.get("url"),
            }
            for p in pages[:5]
        ]
        return json.dumps({"found": True, "pages": simplified})

    async def _analyze_page(self, page_id: str, focus: str = "general") -> str:
        blocks = await self.client.get_page_blocks(page_id)
        text_chunks = []

        for block in blocks:
            block_type = block.get("type")
            rich = block.get(block_type, {}).get("rich_text", [])
            line = "".join(part.get("plain_text", "") for part in rich)
            if line:
                text_chunks.append(line)

        content = "\n".join(text_chunks)
        return json.dumps({
            "page_id": page_id,
            "focus": focus,
            "content": content,
        })

    def _extract_title(self, page: dict) -> str:
        props = page.get("properties", {})
        for prop in props.values():
            if prop.get("type") == "title":
                title_parts = prop.get("title", [])
                return "".join(t.get("plain_text", "") for t in title_parts)
        return "Untitled"

    def tools(self) -> list[Tool]:
        return [
            Tool(
                name="search_page",
                description="Search Notion for a page by title or keywords, e.g. 'daily schedule'.",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search text such as 'daily schedule'",
                        }
                    },
                    "required": ["query"],
                },
                handler=self._search_page,
            ),
            Tool(
                name="analyze_page",
                description="Read a Notion page and return its text content for analysis.",
                parameters={
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "focus": {
                            "type": "string",
                            "description": "What to focus on, e.g. 'daily schedule tasks'",
                        },
                    },
                    "required": ["page_id"],
                },
                handler=self._analyze_page,
            ),
            Tool(
                name="search_in_blocks",
                description="Search for text in Notion blocks, e.g. 'find all tasks for tomorrow'.",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search text such as 'find all tasks for tomorrow'",
                        }
                    },
                    "required": ["query"],
                },
                handler=self._search_in_blocks,
            )
        ]