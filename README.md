**Your Notion workspace, fully accessible through AI.**

A Model Context Protocol (MCP) server that exposes Notion's API for managing pages, databases, blocks, and users across your workspace.


## Overview

The Notion MCP Server provides a complete interface to your Notion workspace:

- Search, read, and write pages with full block-level content control
- Create and query databases with filters, sorts, and pagination
- Manage workspace users and bot identity

Perfect for:

- AI assistants that need to read or update Notion pages and databases
- Automating content creation, knowledge base updates, and task management
- Building tools that integrate Notion with other services


## Tools

### Read Operations

<details>
<summary><code>search_notion</code> — Search pages and databases</summary>

Searches all pages and databases by title, or lists all workspace content when no query is provided.

**Inputs:**
```
- `query` (string, optional) — Search query string; leave empty to list all pages (default: "")
- `filter_type` (string, optional) — Filter results by type: page or data_source
- `page_size` (int, optional) — Number of results to return (max: 100, default: 20)
- `start_cursor` (string, optional) — Pagination cursor from a previous response
```

**Output:**

```json
{
  "results": [{ "id": "page-id", "object": "page", "properties": {...} }, ...],
  "next_cursor": "cursor-string",
  "has_more": true
}
```

</details>


<details>
<summary><code>get_page</code> — Get a page by ID</summary>

Retrieves a Notion page with its properties and metadata.

**Inputs:**
```
- `page_id` (string, required) — The Notion page ID
```

**Output:**

```json
{
  "id": "page-id",
  "object": "page",
  "properties": { "title": { "title": [{ "plain_text": "Page Title" }] } },
  "parent": { "type": "workspace" },
  ...
}
```

</details>


<details>
<summary><code>fetch_page_content</code> — Get a page with full block content</summary>

Retrieves a Notion page along with all its child blocks. Supports recursive fetching up to a configurable depth.

**Inputs:**
```
- `page_id` (string, required) — The Notion page ID
- `include_children` (bool, optional) — Fetch child blocks (default: true)
- `recursive` (bool, optional) — Recursively fetch nested blocks (default: false)
- `max_depth` (int, optional) — Maximum nesting depth for recursive fetch (default: 3)
- `page_size` (int, optional) — Number of blocks per page (default: 100)
- `start_cursor` (string, optional) — Pagination cursor for blocks
```

**Output:**

```json
{
  "id": "page-id",
  "properties": {...},
  "children": [
    { "type": "paragraph", "paragraph": { "rich_text": [{ "plain_text": "Hello" }] } }
  ]
}
```

</details>


### Write Operations

<details>
<summary><code>create_page_under_page</code> — Create a page under a parent page</summary>

Creates a new child page under an existing parent page.

**Inputs:**
```
- `parent_page_id` (string, required) — ID of the parent page
- `title` (string, optional) — Title of the new page (default: "Untitled New page Created")
- `position` (object, optional) — Insert position: {"type": "page_end"} or {"type": "page_start"}
```

**Output:**

```json
{
  "id": "new-page-id",
  "object": "page",
  "url": "https://www.notion.so/new-page-id",
  ...
}
```

</details>


<details>
<summary><code>create_workspace_page</code> — Create a top-level workspace page</summary>

Creates a new page at the workspace level, not under any parent page.

**Inputs:**
```
- `title` (string, optional) — Title of the new page (default: "Untitled New page Created")
```

**Output:**

```json
{
  "id": "new-page-id",
  "object": "page",
  "url": "https://www.notion.so/new-page-id",
  ...
}
```

</details>


<details>
<summary><code>update_page</code> — Update a page's properties and metadata</summary>

Updates properties, icon, cover, archive status, or lock state of an existing page.

**Inputs:**
```
- `page_id` (string, required) — The Notion page ID
- `properties` (object, optional) — Page properties to update (schema depends on page type)
- `icon` (object, optional) — Page icon (emoji or external URL)
- `cover` (object, optional) — Page cover image (external URL)
- `archived` (bool, optional) — Archive or unarchive the page
- `in_trash` (bool, optional) — Move to trash or restore from trash
- `is_locked` (bool, optional) — Lock or unlock the page
- `template` (object, optional) — Template settings
- `erase_content` (bool, optional) — Erase all page content
```

**Output:**

```json
{
  "id": "page-id",
  "archived": false,
  "properties": {...},
  ...
}
```

</details>


<details>
<summary><code>append_text_block</code> — Append a text block to a page</summary>

Adds a text block (paragraph, heading, list item, etc.) to an existing page or block.

**Inputs:**
```
- `block_id` (string, required) — Page ID or parent block ID to append to
- `type` (string, required) — Block type: paragraph, heading_1, heading_2, heading_3, bulleted_list_item, numbered_list_item, to_do, toggle, quote, or callout
- `content` (string, required) — Text content for the block
- `checked` (bool, optional) — For to_do blocks only — whether the item is checked
- `color` (string, optional) — Text or background color (e.g., red, blue_background)
- `position` (string, optional) — Insertion position: start or end
```

**Output:**

```json
{
  "results": [{ "type": "paragraph", "id": "block-id", ... }]
}
```

</details>


### Database Operations

<details>
<summary><code>get_database</code> — Get a database by ID</summary>

Retrieves a Notion database object with its title, parent, and data sources.

**Inputs:**
```
- `database_id` (string, required) — The Notion database ID
```

**Output:**

```json
{
  "id": "database-id",
  "title": [{ "plain_text": "My Database" }],
  "properties": {...},
  ...
}
```

</details>


<details>
<summary><code>get_data_source</code> — Get a data source schema</summary>

Retrieves the schema and properties of a database (data source) by ID.

**Inputs:**
```
- `data_source_id` (string, required) — The data source (database) ID
```

**Output:**

```json
{
  "id": "database-id",
  "properties": {
    "Name": { "type": "title" },
    "Status": { "type": "select", "select": { "options": [...] } }
  }
}
```

</details>


<details>
<summary><code>query_data_source</code> — Query a database with filters and sorts</summary>

Queries a database to retrieve pages matching optional filters and sort criteria.

**Inputs:**
```
- `data_source_id` (string, required) — The data source (database) ID to query
- `filter` (object, optional) — Notion filter object to narrow results
- `sorts` (list, optional) — List of sort objects to order results
- `page_size` (int, optional) — Number of results per page (max: 100, default: 100)
- `start_cursor` (string, optional) — Pagination cursor from a previous response
```

**Output:**

```json
{
  "results": [{ "id": "page-id", "properties": {...} }, ...],
  "next_cursor": "cursor-string",
  "has_more": false
}
```

</details>


<details>
<summary><code>create_database</code> — Create a new database</summary>

Creates a new database as a child of an existing page, with optional properties, icon, and cover.

**Inputs:**
```
- `parent_id` (string, required) — ID of the parent page to create the database under
- `title` (string, optional) — Database title (default: "Untitled Database")
- `description` (string, optional) — Database description
- `properties` (object, optional) — Database property schema definition
- `is_inline` (bool, optional) — Create as inline database (default: false)
- `icon` (object, optional) — Database icon (emoji or external URL)
- `cover` (object, optional) — Database cover image
```

**Output:**

```json
{
  "id": "database-id",
  "title": [{ "plain_text": "My Database" }],
  "url": "https://www.notion.so/database-id",
  ...
}
```

</details>


### User Operations

<details>
<summary><code>list_users</code> — List workspace users</summary>

Lists all users in the workspace. Guest users are excluded.

**Inputs:**
```
- `page_size` (int, optional) — Number of users per page (max: 100, default: 100)
- `start_cursor` (string, optional) — Pagination cursor from a previous response
```

**Output:**

```json
{
  "results": [{ "id": "user-id", "name": "Jane Doe", "type": "person", ... }],
  "has_more": false
}
```

</details>


<details>
<summary><code>get_user</code> — Get a specific user</summary>

Returns information about a specific workspace user by their ID.

**Inputs:**
```
- `user_id` (string, required) — The Notion user ID
```

**Output:**

```json
{
  "id": "user-id",
  "name": "Jane Doe",
  "type": "person",
  "person": { "email": "jane@example.com" }
}
```

</details>


<details>
<summary><code>get_self</code> — Get bot user info</summary>

Returns information about the bot associated with the current API token, including owner and workspace details.

**Inputs:**
```
None
```

**Output:**

```json
{
  "id": "bot-user-id",
  "name": "My Integration",
  "type": "bot",
  "bot": { "owner": { "type": "workspace" }, "workspace_name": "My Workspace" }
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Pagination</strong></summary>

List and query tools support cursor-based pagination:

- `page_size` — Number of results per request (max: 100)
- `start_cursor` — Cursor value from a previous response's `next_cursor` field; omit for the first page

</details>

<details>
<summary><strong>Block Types for append_text_block</strong></summary>

Available `type` values:

- `paragraph` — Standard text block
- `heading_1`, `heading_2`, `heading_3` — Headings of different sizes
- `bulleted_list_item` — Bullet point
- `numbered_list_item` — Numbered list item
- `to_do` — Checkbox item (use `checked` param)
- `toggle` — Collapsible toggle block
- `quote` — Block quote
- `callout` — Highlighted callout box

</details>

<details>
<summary><strong>Color Options for append_text_block</strong></summary>

Text colors: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`

Background colors: append `_background` (e.g., `red_background`, `blue_background`)

</details>

<details>
<summary><strong>Notion ID Format</strong></summary>

Notion IDs are UUIDs and can be found in the page URL:

```
https://www.notion.so/workspace/My-Page-<page-id>
Example page_id: 8f9b3c2d-1a2b-3c4d-5e6f-7a8b9c0d1e2f
```

Dashes are optional — both formats work with the API.

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** OAuth token not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_TOKEN` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check your Notion OAuth credential is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Notion credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Notion account via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check that filter/sort objects match Notion's expected schema format

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Notion API Error</strong></summary>

- **Cause:** Upstream Notion API returned an error
- **Solution:**
  1. Check Notion service status at [Notion Status](https://status.notion.so)
  2. Verify your integration has access to the target page or database (share it with the integration in Notion)
  3. Review the error message returned in the response for specific details

</details>

---

### Resources

- **[Notion API Documentation](https://developers.notion.com)** — Official API reference
- **[Notion API Reference](https://developers.notion.com/reference)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling
