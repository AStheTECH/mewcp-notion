
**Seamless Notion Integration for MCP**

A Model Context Protocol (MCP) server that exposes Notion's API for comprehensive page, database, and user operations.

---

## Overview

The Notion MCP Server provides a stateless, multi-user interface to interact with Notion:

- **Page Operations**: Create, update, and fetch pages with full content and property support.
- **Database Management**: Query data sources, create new databases, and retrieve metadata.
- **Workspace Navigation**: Search across the entire workspace and access user information.

Perfect for:

- **Content Automation**: Appending blocks and updating status automatically.
- **Data Synchronization**: Fetching database records for external analysis.
- **AI-Powered Workflows**: Allowing models to browse and modify your Notion workspace.

---

## Tools

<details>
<summary><code>search_notion</code> — Search all pages and databases by title or list all pages</summary>

Search all pages and databases by title, with optional filtering by type. Use an empty query to list all reachable objects.

**Inputs:**
```
- `query` (string, optional) — Search query string, keep it empty to list all pages
- `filter_type` (string, optional) — Filter by 'page' or 'data_source'
- `page_size` (integer, optional) — Number of pages to return (max 100)
- `start_cursor` (string, optional) — Pagination cursor
```

**Output:**

```json
{
  "result": "List of pages and databases matching the search criteria"
}
```

</details>

---

<details>
<summary><code>get_page</code> — Retrieve a Notion page by ID with properties and metadata</summary>

Retrieve a specific Notion page by its ID, including all properties and metadata.

**Inputs:**
```
- `page_id` (string, required) — The ID of the page to retrieve
```

**Output:**

```json
{
  "result": "Page object with properties and metadata"
}
```

</details>

---

<details>
<summary><code>fetch_page_content</code> — Retrieve a Notion page with its full content</summary>

Retrieve a Notion page with its full content including all child blocks and properties, with optional recursion.

**Inputs:**
```
- `page_id` (string, required) — The ID of the page to fetch
- `include_children` (boolean, optional) — Whether to include child blocks
- `recursive` (boolean, optional) — Whether to fetch children recursively
- `max_depth` (integer, optional) — Maximum depth for recursion
- `page_size` (integer, optional) — Number of child blocks to return
- `start_cursor` (string, optional) — Pagination cursor
```

**Output:**

```json
{
  "result": "Page content including all blocks and properties"
}
```

</details>

---

<details>
<summary><code>create_page_under_page</code> — Create a new page under a parent page</summary>

Create a new page as a child of an existing parent page.

**Inputs:**
```
- `parent_page_id` (string, required) — The ID of the parent page
- `title` (string, optional) — Title of the new page
- `position` (object, optional) — Insert position: `{"type": "page_end"}` or `{"type": "page_start"}`
```

**Output:**

```json
{
  "result": "Metadata of the newly created page"
}
```

</details>

---

<details>
<summary><code>create_workspace_page</code> — Create a new page at workspace level</summary>

Create a new page at the workspace root level without a parent page.

**Inputs:**
```
- `title` (string, optional) — Title of the new page
```

**Output:**

```json
{
  "result": "Metadata of the newly created workspace page"
}
```

</details>

---

<details>
<summary><code>update_page</code> — Update an existing Notion page's properties and metadata</summary>

Update properties, metadata, and content settings of an existing Notion page.

**Inputs:**
```
- `page_id` (string, required) — The ID of the page to update
- `properties` (object, optional) — Page properties to update
- `icon` (object, optional) — Page icon settings
- `cover` (object, optional) — Page cover image settings
- `archived` (boolean, optional) — Whether to archive the page
- `in_trash` (boolean, optional) — Whether to move the page to trash
- `is_locked` (boolean, optional) — Whether to lock the page
- `template` (object, optional) — Template settings
- `erase_content` (boolean, optional) — Whether to erase all page content
```

**Output:**

```json
{
  "result": "Updated page object"
}
```

</details>

---

<details>
<summary><code>append_text_block</code> — Append a text block to a page or block</summary>

Append a new text block of various types (paragraph, heading, to-do, etc.) to a page or parent block.

**Inputs:**
```
- `block_id` (string, required) — The ID of the page or parent block
- `type` (string, required) — Type of block: `paragraph`, `heading_1`, `heading_2`, `heading_3`, `bulleted_list_item`, `numbered_list_item`, `to_do`, `toggle`, `quote`, `callout`
- `content` (string, required) — The text content for the block
- `checked` (boolean, optional) — Whether the item is checked (for to-dos)
- `color` (string, optional) — Text or background color (e.g., `red`, `blue_background`)
- `position` (string, optional) — Insert position: `end` or `start`
```

**Output:**

```json
{
  "result": "Details of the appended block"
}
```

</details>

---

<details>
<summary><code>get_database</code> — Retrieve a database object by ID</summary>

Retrieve a database (data source) by ID with title, parent information, and associated data sources.

**Inputs:**
```
- `database_id` (string, required) — The ID of the database to retrieve
```

**Output:**

```json
{
  "result": "Database object with metadata"
}
```

</details>

---

<details>
<summary><code>get_data_source</code> — Retrieve a data source with schema information</summary>

Retrieve a data source (database schema/properties) by ID.

**Inputs:**
```
- `data_source_id` (string, required) — The ID of the data source to retrieve
```

**Output:**

```json
{
  "result": "Data source object with properties and schema"
}
```

</details>

---

<details>
<summary><code>query_data_source</code> — Query a data source (database) with filters and sorting</summary>

Query a database to retrieve pages with optional filtering and sorting.

**Inputs:**
```
- `data_source_id` (string, required) — The ID of the data source (database)
- `filter` (object, optional) — Notion filter object
- `sorts` (array, optional) — Notion sorts array
- `page_size` (integer, optional) — Number of records to return
- `start_cursor` (string, optional) — Pagination cursor
```

**Output:**

```json
{
  "result": "List of database entries matching the query"
}
```

</details>

---

<details>
<summary><code>create_database</code> — Create a new database as a child of a page</summary>

Create a new database (inline or full) under an existing page.

**Inputs:**
```
- `parent_id` (string, required) — The ID of the parent page
- `title` (string, optional) — Title of the database
- `description` (string, optional) — Description of the database
- `properties` (object, optional) — Database properties/schema
- `is_inline` (boolean, optional) — Whether the database is inline
- `icon` (object, optional) — Database icon settings
- `cover` (object, optional) — Database cover image settings
```

**Output:**

```json
{
  "result": "Metadata of the newly created database"
}
```

</details>

---

<details>
<summary><code>list_users</code> — List all users in the workspace</summary>

List all users in the workspace (excluding guests).

**Inputs:**
```
- `page_size` (integer, optional) — Number of users to return per page
- `start_cursor` (string, optional) — Pagination cursor
```

**Output:**

```json
{
  "result": "List of workspace users"
}
```

</details>

---

<details>
<summary><code>get_user</code> — Retrieve a specific user by ID</summary>

Retrieve information about a specific user in the workspace.

**Inputs:**
```
- `user_id` (string, required) — The ID of the user to retrieve
```

**Output:**

```json
{
  "result": "User object with profile information"
}
```

</details>

---

<details>
<summary><code>get_self</code> — Retrieve the bot user associated with your API token</summary>

Retrieve the bot user associated with your API token, including owner and workspace information.

**Inputs:**
```
None
```

**Output:**

```json
{
  "result": "Bot user object with workspace and owner details"
}
```

</details>

---

<details>
<summary><strong>API Parameters Reference</strong></summary>

### Common Parameters

- `page_size` — Maximum number of items to return in a single request (default: 20 or 100 depending on tool).
- `start_cursor` — Token used for pagination to retrieve the next set of results.
- `filter` — A structured object used to narrow down results based on specific criteria.

### Resource Formats

**Notion ID:**

```
32-character hexadecimal string, often formatted with hyphens.
Example: 834c6e94-0d70-4f52-87a4-82a1789c6d48
```

**Block Type:**

```
String indicating the structure of the block.
Example: paragraph, heading_1, to_do
```

</details>

---

<details>
<summary><strong>Troubleshooting</strong></summary>

### **Missing or Invalid Curious Layer API Key**

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` header is present
  2. Check API key is active in your Curious Layer account
  3. Regenerate API key if expired

### **Insufficient Credits**

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

### **Credential Not Connected**

- **Cause:** No Notion credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCp dashboard
  2. Connect your Notion account (OAuth)
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

### **Malformed Request Payload**

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

### **Server Not Found**

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `notion-mcp-server/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

### **Notion API Error**

- **Cause:** Upstream Notion API returned an error
- **Solution:**
  1. Check Notion service status at [Notion Status Page](https://status.notion.so/)
  2. Verify your credential has the required permissions (scopes)
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Notion API Documentation](https://developers.notion.com/docs)** — Official API reference
- **[Notion API Reference](https://developers.notion.com/reference/intro)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
