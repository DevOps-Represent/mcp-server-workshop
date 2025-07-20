# 🧠 Build an AI Backend: Tools, Memory & Prompts for Real-World LLMs

Welcome to the workshop! In this hands-on session, you'll learn how to build and deploy an **MCP (Model Context Protocol) server** — the backend brain behind AI clients like assistants, copilots, and autonomous agents.

Using the open-source **TypeScript or Python MCP SDK** and **Claude**, you’ll create a system that gives an LLM memory, tool access, and structured prompts — and deploy it live using **Cloudflare**.

No prior AI experience needed — just Python, JavaScript/TypeScript, and curiosity!

---

<details>
<summary><strong>🎯 Workshop Goals</strong></summary>

By the end of this workshop, you will:

- Understand what an **MCP Server** is and how it powers AI systems
- Use the MCP SDK to:
  - Register and expose tools (functions) to an AI model
  - Manage context and memory for stateful conversations
  - Orchestrate prompts and responses between clients and Claude
- Run and test your MCP server locally
- **Deploy your MCP server to Cloudflare** using Workers or Pages Functions so others can use it too

</details>

---

<details>
<summary><strong>👩‍💻 Who This Is For</strong></summary>

This workshop is designed for:

- Engineers curious about AI infrastructure
- Folks building AI-powered assistants, bots, or internal tools
- DevOps/Platform engineers interested in tool orchestration
- Anyone who wants to get hands-on with real LLM systems (beyond chatbots)

</details>

---

<details>
<summary><strong>🧰 Tools & Tech Requirements</strong></summary>

All tools are free, open source, or have free tiers. We'll support you with setup.

| Tool                            | Purpose                          |
|---------------------------------|----------------------------------|
| TypeScript or Python MCP SDK    | Core server logic                |
| Node.js v18+ or Python 3.10+    | Runtime                          |
| MCP client of choice            | AI model backend                 |
| Cloudflare Workers /            | Live deployment platform         |

You’ll need:
- A personal GitHub account
- A working Node.js v18+ or Python 3.10+ environment (or Gitpod access)
- An account with [Claude](https://claude.ai/) or mcp client of choice
- A [Cloudflare account](https://dash.cloudflare.com/sign-up) (free tier is fine)

### 👉🏾[Full set-up instructions are here](workshop_setup_instructions.md) 
</details>

---

<details>
<summary><strong>🛠 What You'll Build</strong></summary>

- A fully working **AI backend** with:
  - Custom tools (functions) that your AI can call
  - Memory for storing state or chat history
  - Prompt logic that guides Claude’s behavior
- A live, working **Cloudflare-hosted MCP server** accessible from the web

</details>

---

<details>
<summary><strong>📦 You’ll Walk Away With</strong></summary>

- A GitHub repo of your custom, live-deployed MCP server
- Experience building modern AI infrastructure with open source tools
- A clearer understanding of AI backend architecture and edge deployments
- Confidence to keep building LLM-powered assistants, agents, or copilots
- Real experience with **Cloudflare’s developer platform** (Workers, Pages, etc.)

</details>
