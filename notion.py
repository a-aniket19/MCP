import os
from mcp.server.fastmcp import FastMCP
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Notion")

notion = Client(auth=os.getenv("NOTION_API_KEY"))

@mcp.tool()
def search_notion(query: str) -> str:
    """Search across all pages and databases in the Notion workspace for a given query."""
    results = notion.search(query=query).get("results", [])
    
    if not results:
        return "No results found."
    
    output = []
    for r in results:
        title = "Untitled"
        if r["object"] == "page":
            props = r.get("properties", {})
            for prop in props.values():
                if prop["type"] == "title":
                    title_parts = prop["title"]
                    if title_parts:
                        title = title_parts[0]["plain_text"]
                    break
        output.append(f"- {title} (ID: {r['id']})")
    
    return "\n".join(output)

@mcp.tool()
def get_page(page_id: str) -> str:
    """Read the content of a Notion page by its ID."""
    blocks = notion.blocks.children.list(block_id=page_id).get("results", [])
    
    if not blocks:
        return "Page is empty."
    
    output = []
    for block in blocks:
        block_type = block["type"]
        content = block.get(block_type, {})
        rich_text = content.get("rich_text", [])
        text = "".join([t["plain_text"] for t in rich_text])
        if text:
            output.append(text)
    
    return "\n".join(output)

@mcp.tool()
def create_page(title: str, content: str, parent_page_id: str) -> str:
    """Create a new Notion page with a title and content under a specified parent page ID."""
    notion.pages.create(
        parent={"page_id": parent_page_id},
        properties={
            "title": {
                "title": [{"text": {"content": title}}]
            }
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": content}}]
                }
            }
        ]
    )
    return f"Page '{title}' created successfully."

if __name__ == "__main__":
    mcp.run()