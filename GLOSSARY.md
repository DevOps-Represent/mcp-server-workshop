# Glossary

## Core

Play the game: https://public.canva.site/mcp-workshop-terms

| Term | Definition |
|------|------------|
| **Model Context Protocol (MCP)** | A protocol that defines how AI models, tools, and resources interact using structured context and standardised messaging. |
| **Context** | The organised set of information—including user input, history, and resources—provided to an AI model for a specific request. |
| **Resource** | Any external data, file, or service referenced in the context to support or enhance model outputs. |
| **Prompt** | The main input or instruction, often with context and resources, sent to an AI model to generate a response. |
| **Tool** | An external function or API that the model can invoke during processing to perform actions or fetch information. |
| **Transport** | The underlying communication mechanism used to exchange MCP messages between clients and servers, such as stdio (standard input/output), HTTP, WebSockets, or gRPC. |
| **Session** | A persistent interaction between a client and an MCP server, maintaining context and state across multiple exchanges. |
| **Context Tree** | The hierarchical structure that organizes all context nodes, resources, and prompts for a session. |
| **MCP Server** | The backend service that implements MCP, managing context, resources, and model interactions. |
| **MCP Client** | Any application or interface that communicates with an MCP server to send prompts and receive responses. |
| **Server-Sent Events (SSE)** | A transport mechanism for streaming events from the server to the client over HTTP, commonly used for real-time MCP communication. |
| **MCP Inspector** | A web-based client tool for connecting to and testing MCP servers, allowing you to invoke tools and inspect responses interactively. |
| **Remote MCP Server** | An MCP server that is accessible over the network (e.g., via HTTP, SSE, or WebSockets), as opposed to running locally or via stdio. |
| **Agent** | An autonomous or semi-autonomous entity that interacts with users, models, and tools via the MCP protocol to accomplish tasks. |
| **Workflow** | A defined sequence of steps or actions, often involving multiple tools or agents, orchestrated via MCP to achieve a specific goal. |
| **Human in the Loop** | A pattern where human input or approval is integrated into the workflow, allowing humans to intervene or guide agent actions. |

## Extra Definitions

| Term | Definition |
|------|------------|
| **Sampling** | The method of generating model outputs by probabilistically selecting from possible continuations, guided by parameters like temperature or top-k. |
| **Root** | The top-level context node from which all other context elements and resources branch in an MCP session. |
| **Context Node** | An individual element within the context tree, representing a specific piece of information or resource. |
| **Proxy** | A service or tool that relays requests between MCP clients and remote MCP servers, often used to bridge local and remote environments. |
| **Context Management** | The operations and strategies for creating, updating, and maintaining context throughout an MCP session. |
| **Invocation** | The act of calling a tool or resource from within a model's context during processing. |
| **Capability** | A specific function or feature that an MCP server or tool exposes to clients or models. |
| **Message** | A structured data packet exchanged between MCP clients and servers, containing prompts, responses, or context updates. |
| **OAuth** | An open standard protocol used for secure authentication and authorization, often integrated into MCP servers for user login and permissions. |
| **Schema** | The formal definition of the structure and types of data used in MCP messages and contexts. |
| **Authorisation** | The process of controlling access to resources, tools, or actions within the MCP environment. |
| **Authentication** | The process of verifying the identity of a user or client before granting access to MCP server features. |
| **Integration** | The process of connecting external tools, resources, or services to an MCP server to extend its functionality. |