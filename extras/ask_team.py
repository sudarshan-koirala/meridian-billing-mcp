"""A teammate asks the shared Graphify MCP server over HTTP.

No AI model is used. No extra packages are necessary.
Run from any folder:
  With the key:     GRAPHIFY_API_KEY=demo-key-123 python ask_team.py
  Without the key:  GRAPHIFY_API_KEY= python ask_team.py
For a real team, set GRAPHIFY_URL to the address of the shared machine,
for example http://192.168.1.20:8099/mcp
"""
import json
import os
import urllib.error
import urllib.request

SERVER_URL = os.environ.get("GRAPHIFY_URL", "http://127.0.0.1:8099/mcp")
API_KEY = os.environ.get("GRAPHIFY_API_KEY", "")
NO_PROXY = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def send(message, session_id=None):
    """Send one MCP message to the server and return (reply, session id)."""
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    request = urllib.request.Request(SERVER_URL, data=json.dumps(message).encode(), headers=headers)
    with NO_PROXY.open(request, timeout=30) as response:
        body = response.read().decode()
        session_id = response.headers.get("Mcp-Session-Id", session_id)
    reply = None
    for line in body.splitlines():  # the server answers as an event stream
        if line.startswith("data:"):
            reply = json.loads(line[5:])
    if reply is None and body.strip().startswith("{"):
        reply = json.loads(body)
    return reply, session_id


def main():
    print(f"Server:  {SERVER_URL}")
    print(f"API key: {'yes' if API_KEY else 'NO KEY'}")
    hello = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-03-26", "capabilities": {},
        "clientInfo": {"name": "ask_team", "version": "1.0"}}}
    try:
        _, session_id = send(hello)
    except urllib.error.HTTPError as error:
        if error.code == 401:
            print("\nACCESS DENIED (401). The server sent no graph data.")
            print("Ask the owner of the server for the API key.")
            return
        raise
    except urllib.error.URLError:
        print("\nNO ANSWER. The server is not running at this address.")
        return

    send({"jsonrpc": "2.0", "method": "notifications/initialized"}, session_id)
    question = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
        "name": "shortest_path",
        "arguments": {"source": "bill_customer", "target": "legacy_apac_rounding"}}}
    reply, _ = send(question, session_id)
    print("\nANSWER FROM THE SHARED GRAPH:")
    for part in reply["result"]["content"]:
        print(part.get("text", ""))


main()
