# Meridian Billing × Graphify MCP

> **Every APAC customer pays slightly less than they should, and nobody knows why.**
> This repo is a small billing codebase with a hidden bug. You turn it into a knowledge graph
> with [Graphify](https://pypi.org/project/graphifyy/), serve that graph over **MCP**, and let
> Claude Code (or any MCP client) find the bug through graph tools.

```text
$ python run_demo.py
Region   Invoiced   Expected   Gap
NA         973.25     973.25    0.00
Europe     973.25     973.25    0.00
APAC       971.00     973.25    2.25   <-- why?
LATAM      973.25     973.25    0.00
```

The answer is 4 hops away, and the graph finds it in a single tool call:

```text
bill_customer() -> send_invoice_email() -> create_invoice() -> regional_price() -> legacy_apac_rounding()
```

```python
def legacy_apac_rounding(amount):
    """Round DOWN to a whole number.

    # WHY: Added in 2019 for one APAC reseller contract that billed in whole units.
    # NOTE: Nobody removed it. It now runs for every APAC account.
    """
```

---

## What you will learn

- Build a code graph with `graphify extract` (no LLM, no tokens used)
- Connect the graph to Claude Code as a **stdio MCP server**
- Ask questions with 10 graph tools: `graph_stats`, `shortest_path`, `get_neighbors`, `god_nodes` and more
- Query the same server from a **plain Python MCP client** (no AI model)
- Keep the graph fresh with `graphify update`. The server picks up changes with no restart
- Share one graph with your team over **HTTP with an API key**, and test it with **MCP Inspector**

## Repo layout

```text
.
├── meridian-billing/        # the project to graph (start Claude Code here)
│   ├── run_demo.py          # shows the APAC billing gap
│   └── meridian/            # accounts, billing, reports, support, notifications, utils
└── extras/                  # keep OUTSIDE the project, or it ends up in the graph
    ├── ask_graph.py         # tiny stdio MCP client: lists tools, calls graph_stats + shortest_path
    ├── ask_team.py          # HTTP MCP client with an API key, standard library only
    └── credits.py           # a new file to add in Step 5 (shows live graph updates)
```

## Requirements

| Tool | Version |
| --- | --- |
| Python | 3.10+ |
| [uv](https://docs.astral.sh/uv/) | any recent |
| [Claude Code](https://claude.com/claude-code) | tested with 2.1.329 |
| Node.js | 22.19+ (only for MCP Inspector in Step 6) |

Tested with `graphifyy` 0.9.108 on November 21, 2026.

> You do **not** need `graphify install` for this demo. That command installs the Claude Code
> *skill*. The MCP server does not use it.

---

## Quickstart

```bash
git clone https://github.com/sudarshan-koirala/meridian-billing-mcp.git
cd meridian-billing-mcp/meridian-billing
python run_demo.py          # see the APAC gap
```

### Step 1: Install Graphify and build the graph

```bash
uv tool install "graphifyy[mcp]"      # keep the quotes, zsh needs them
graphify extract . --code-only
graphify cluster-only . --no-label
```

Expected: **22 code files, 89 nodes, 215 edges, 12 communities**.
Open `graphify-out/graph.html` in a browser to see the graph.

### Step 2: Connect Claude Code

```bash
claude mcp add --transport stdio graphify -- graphify-mcp "$(pwd)/graphify-out/graph.json"
claude mcp list
# graphify: graphify-mcp .../graphify-out/graph.json - Connected
```

Start Claude Code **after** this step, in the `meridian-billing` folder.

### Step 3: Ask through the tools

Run `/mcp`. You see `graphify` with 10 tools:
`query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats`,
`shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.

Then try these prompts:

```text
Use the graphify MCP tools. Call graph_stats and show me the numbers.
```
→ Nodes: 89, Edges: 215, Communities: 12, EXTRACTED: 100%

```text
Use the graphify MCP tools. What is the shortest path from bill_customer to legacy_apac_rounding?
```
→ 4 hops: `bill_customer() -> send_invoice_email() -> create_invoice() -> regional_price() -> legacy_apac_rounding()`

```text
Use the graphify MCP tools. Show the neighbors of legacy_apac_rounding. Why does this function exist? Do not edit any files.
```
→ `regional_price()` [calls], `pricing.py` [imports], `currency.py` [contains], and the rationale node
*"WHY: Added in 2019 for one APAC reseller..."*

> **Tip:** Start each prompt with *"Use the graphify MCP tools"*. If the Graphify skill is also
> installed, Claude Code may use the skill and not the MCP server.

### Step 4: A second agent, with no AI

Any MCP client can use the same server. This script lists the tools and asks the same question:

```bash
uv run --with mcp ../extras/ask_graph.py
```

You get the same 10 tools, the same stats and the same 4-hop path.

### Step 5: Keep the graph fresh

Add a new file and update the graph:

```bash
cp ../extras/credits.py meridian/billing/
graphify update .
```

Ask Claude Code to `Call graph_stats again`. You see **Nodes: 92**, with no server restart.

```text
Use the graphify MCP tools. What is the shortest path from apply_credit to legacy_apac_rounding?
```
→ 2 hops: `apply_credit() -> regional_price() -> legacy_apac_rounding()`. The new code also inherits the bug.

### Step 6: Share the graph with your team

**Tab 1 (the server):**

```bash
graphify-mcp graphify-out/graph.json --transport http --host 0.0.0.0 --port 8099 --api-key demo-key-123
```

**Tab 2 (a teammate, in an empty folder with no code):**

```bash
mkdir -p ~/demos/teammate && cd ~/demos/teammate
claude mcp add --transport http graphify-team http://<YOUR_IP>:8099/mcp --header "Authorization: Bearer demo-key-123"
claude mcp add --transport http graphify-nokey http://<YOUR_IP>:8099/mcp
claude mcp list
# graphify-team:  http://<YOUR_IP>:8099/mcp (HTTP) - Connected
# graphify-nokey: http://<YOUR_IP>:8099/mcp (HTTP) - Failed to connect ... (HTTP 401): unauthorized
```

Find your IP with `ipconfig getifaddr en0` (Mac) or `ipconfig` (Windows).
Start `claude` in the teammate folder and ask the shortest-path question with
*"Use only the graphify-team MCP tools"*. That folder has no code, so the answer must come from the server.

**Test with MCP Inspector:**

```bash
npx @modelcontextprotocol/inspector http://<YOUR_IP>:8099/mcp --transport http --header "Authorization: Bearer demo-key-123"
```

- With the key: status **Connected**, **Tools (10)**, and `shortest_path` returns the 4 hops.
- Without the `--header`: status **Failed**, `Dynamic Client Registration rejected (HTTP 401)`, and no Tools tab.

**Or test with plain Python (no packages needed):**

```bash
GRAPHIFY_API_KEY=demo-key-123 python3 ../extras/ask_team.py   # ANSWER FROM THE SHARED GRAPH + 4 hops
GRAPHIFY_API_KEY=             python3 ../extras/ask_team.py   # ACCESS DENIED (401)
```

Set `GRAPHIFY_URL=http://<SERVER_IP>:8099/mcp` to point the script at another machine.

> **Security:** `--host 0.0.0.0` lets every machine on your network reach the server. Use it only on
> a trusted network, never on public Wi-Fi. The default `127.0.0.1` is local-only.
> `demo-key-123` is a demo key. Use a long random key for real use, and note that
> `claude mcp get` prints the key in plain text.

**Clean up:**

```bash
claude mcp remove graphify-team && claude mcp remove graphify-nokey   # in the teammate folder
# Ctrl+C in Tab 1 stops the server
```

---

## More prompts to try

| Prompt | Expected |
| --- | --- |
| `Use the graphify MCP tools. Call god_nodes with top_n 5.` | Database 20, get_account() 18, round_money() 15, regional_price() 13, create_invoice() 12 |
| `Use the graphify MCP tools. Call get_node for legacy_apac_rounding.` | Source `meridian/utils/currency.py` L9, degree 4 |
| `Use the graphify MCP tools. Use query_graph with depth 1: which code changes the price for APAC accounts?` | Finds the code that changes APAC prices |

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `graphify-mcp: command not found` | `uv tool install --reinstall "graphifyy[mcp]"` |
| `zsh: no matches found: graphifyy[mcp]` | Put the package name in double quotes |
| `claude mcp list` shows *Failed to connect* | Path is wrong or `graph.json` is missing. Build (Step 1), then remove and add the server again |
| `/mcp` does not show graphify | Claude Code started before Step 2 or in another folder. Restart it in `meridian-billing` |
| Claude answers without calling a tool | Name the tool: *"Use the graphify MCP tools. Call shortest_path..."* |
| Graph has 99 nodes, not 89 | `ask_graph.py` is inside the project. Keep `extras/` outside and rebuild |
| Graph has 92 nodes before Step 5 | `credits.py` is already in `meridian/billing/`. Remove it and rebuild |
| `address already in use` on port 8099 | Use `--port 8100` and set `GRAPHIFY_URL=http://127.0.0.1:8100/mcp` |
| Inspector: `PORT IS IN USE` on 6274 | An old Inspector is running. Stop it with Ctrl+C |
| Inspector fails even with the key | Server in Tab 1 is not running, or the keys do not match |
| `graphify-team` fails to connect | Missing `--host 0.0.0.0`, wrong IP, or firewall blocks 8099 (on a Mac, click *Allow*) |
| `list_prs`, `get_pr_impact`, `triage_prs` error | These need a GitHub repo with pull requests. Not used in this demo |

## About the sample project

Meridian Labs is a fictional SaaS company. The `meridian` package is a small, dependency-free
billing system (accounts, pricing, invoices, tax, refunds, reports, support SLAs, email). It exists
only to give the graph something real to explore. The bug is intentional, so please don't fix it
before you try the demo 🙂
