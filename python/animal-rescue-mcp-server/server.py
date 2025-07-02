from fastmcp import FastMCP

# Create a server instance
mcp = FastMCP(name="MyAssistantServer")

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="127.0.0.1",
        path="/sse",
        port=8432
    )