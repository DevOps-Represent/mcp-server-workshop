# python animal rescue mcp server

minimal example because the modelcontextprotocol docs are weird because they use an old fastmcp version and obfuscate everything with UV

```bash
python3 -m venv venv
./venv/bin/pip install fastmcp
./venv/bin/python server.py
# run the mcp inspector in the background and point it to SSE on http://127.0.0.1:8432/sse
```

now add tools using docs here https://github.com/jlowin/fastmcp