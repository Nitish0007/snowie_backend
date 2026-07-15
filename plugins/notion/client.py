import httpx

NOTION_VERSION = "2022-06-28"

class NotionClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    async def search_pages(self, query: str) -> list[dict]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.api_base_url + f"/search",
                headers=self.headers,
                json={"query": query, "filter": {"value": "page", "property": "object"}},
            )
            resp.raise_for_status()
            return resp.json().get("results", [])

    async def get_page_blocks(self, page_id: str) -> list[dict]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                self.api_base_url + f"/blocks/{page_id}/children",
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json().get("results", [])