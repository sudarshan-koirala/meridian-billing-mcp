"""A tiny MCP client. It asks the Graphify MCP server two questions. No AI model is used.

Run from the meridian-billing folder: uv run --with mcp ../extras/ask_graph.py
"""
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="graphify-mcp", args=["graphify-out/graph.json"])


async def ask(session, tool, arguments):
    result = await session.call_tool(tool, arguments)
    print(f"\n--- {tool} ---")
    print("\n".join(part.text for part in result.content if hasattr(part, "text")))


async def main():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Tools:", ", ".join(tool.name for tool in tools.tools))
            await ask(session, "graph_stats", {})
            await ask(session, "shortest_path", {"source": "bill_customer", "target": "legacy_apac_rounding"})


asyncio.run(main())
