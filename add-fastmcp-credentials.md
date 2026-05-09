# Adding `fastmcp-credentials` to an MCP Server

This guide walks through every change needed to migrate an existing FastMCP server from passing credentials as tool parameters to injecting them server-side via `fastmcp-credentials`.

After this migration the LLM never sees tokens, API keys, or secrets — they are resolved from HTTP headers and injected transparently into every tool call.

---

## What changes

| Before | After |
|--------|-------|
| Every tool accepts `oauth_token`, `api_key`, etc. as parameters | No auth params on any tool |
| The HTTP client receives the token from the tool call | The HTTP client calls `get_credentials()` to read the injected credential |
| The server is a plain `FastMCP(...)` instance | The server wraps a `CredentialMiddleware` around a `HeaderCredentialBackend` |

---

## Step 1 — Add the dependency

In `requirements.txt`, add:

```
fastmcp-credentials>=0.1.0
```

---

## Step 2 — Wire the middleware into the server

In your main server file (e.g. `my_mcp_server.py`), replace the bare `FastMCP` instantiation with one that includes the credential middleware.

**Before:**
```python
from fastmcp import FastMCP

mcp = FastMCP("My Service MCP Server")
```

**After:**
```python
from fastmcp import FastMCP
from fastmcp_credentials import CredentialMiddleware, HeaderCredentialBackend

backend = HeaderCredentialBackend()
mcp = FastMCP("My Service MCP Server", middleware=[CredentialMiddleware(backend)])
```

That's all the server-level change needed. The middleware intercepts every tool call, reads credentials from the incoming request headers, and stores them in a request-scoped context variable.

---

## Step 3 — Update the HTTP client utility

Find the shared function (usually in `utils/`) that builds request headers and makes API calls. Remove the token parameter and replace it with a call to `get_credentials()`.

**Before (typical pattern):**
```python
import requests

def get_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

def make_api_request(method: str, endpoint: str, token: str, body=None, params=None):
    headers = get_headers(token)
    response = requests.request(method=method, url=BASE_URL + endpoint,
                                headers=headers, json=body, params=params)
    return response.json()
```

**After:**
```python
import requests
from fastmcp_credentials import get_credentials

def get_headers() -> dict:
    cred = get_credentials()
    # Use cred.access_token for OAuth, cred.api_key for static key auth
    token = cred.access_token or cred.api_key
    if not token:
        raise ValueError("No credential available")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

def make_api_request(method: str, endpoint: str, body=None, params=None):
    headers = get_headers()
    response = requests.request(method=method, url=BASE_URL + endpoint,
                                headers=headers, json=body, params=params)
    return response.json()
```

Key points:
- `get_credentials()` is synchronous — no `await`, no `ctx` argument needed.
- It returns a `ResolvedCredential` dataclass. Use `cred.access_token` for OAuth flows and `cred.api_key` for static API key flows.
- If neither field is populated, raise an explicit error early so the failure message is clear.

---

## Step 4 — Remove auth parameters from every tool

Go through every `@mcp.tool()` function and its underlying service function. Remove every parameter that carries a credential (`oauth_token`, `access_token`, `api_key`, `bearer_token`, etc.) from both the tool wrapper and the service function signatures.

**Before:**
```python
@mcp.tool(name="list_items", description="List all items")
def list_items(oauth_token: str, folder_id: str, page_size: int = 20):
    return list_items_service(oauth_token, folder_id, page_size)


def list_items_service(oauth_token: str, folder_id: str, page_size: int) -> dict:
    result = make_api_request("GET", f"/items/{folder_id}", token=oauth_token,
                              params={"page_size": page_size})
    return result
```

**After:**
```python
@mcp.tool(name="list_items", description="List all items")
def list_items(folder_id: str, page_size: int = 20):
    return list_items_service(folder_id, page_size)


def list_items_service(folder_id: str, page_size: int) -> dict:
    result = make_api_request("GET", f"/items/{folder_id}",
                              params={"page_size": page_size})
    return result
```

Repeat for every tool in the server. A quick way to find all occurrences:

```bash
grep -rn "oauth_token\|api_key\|access_token\|bearer_token" tools/ notion_mcp_server.py
```

---

## Step 5 — Update the README

Remove all mentions of auth parameters from the **Inputs** section of every tool. The auth section of the README should only describe how a user obtains credentials from the service and connects them through the Curious Layer platform — no mention of headers, env vars, or middleware mechanics.

See [README-instructions.md](README-instructions.md) for the current template.

---

## The `ResolvedCredential` reference

`get_credentials()` always returns this dataclass regardless of backend:

```python
@dataclass
class ResolvedCredential:
    type: Literal["static", "oauth"]

    # Static auth
    api_key: str | None

    # OAuth
    access_token: str | None
    refresh_token: str | None
    client_id: str | None
    client_secret: str | None
    token_uri: str | None
    scopes: list[str] | None
    expires_at: datetime | None

    # Provider-specific extras
    extra: dict          # populated from X-MCP-Cred-Extra header

    def is_expired(self) -> bool: ...
```

Use `cred.extra["key"]` for any provider-specific fields the gateway injects beyond the standard set (e.g. tenant IDs, signing secrets).

---

## Headers the gateway injects

For reference, these are the headers `HeaderCredentialBackend` reads. You never need to handle them manually — the middleware does it.

| Header | Description |
|--------|-------------|
| `X-MCP-Cred-Access-Token` | OAuth access token |
| `X-MCP-Cred-Api-Key` | Static API key / PAT |
| `X-MCP-Cred-Scopes` | Comma-separated OAuth scopes |
| `X-MCP-Cred-Extra` | JSON object with provider-specific extras |
| `X-MCP-Cred-Expires-At` | Token expiry as ISO 8601 UTC |

At least one of `X-MCP-Cred-Access-Token` or `X-MCP-Cred-Api-Key` must be present, or the middleware raises `MissingCredentialHeaderError`.

---

## Quick checklist

- [ ] `fastmcp-credentials>=0.1.0` added to `requirements.txt`
- [ ] `HeaderCredentialBackend` + `CredentialMiddleware` wired into `FastMCP(...)`
- [ ] `get_credentials()` used in the HTTP utility instead of a token parameter
- [ ] All auth parameters removed from tool function signatures
- [ ] All auth parameters removed from service function signatures
- [ ] README Tools section updated — no auth params in any **Inputs** list
- [ ] README auth section updated to describe credential setup only (no implementation details)
