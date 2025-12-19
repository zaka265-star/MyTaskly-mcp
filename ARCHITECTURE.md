# MyTaskly MCP - Architecture Documentation

## Overview

This MCP (Model Context Protocol) server provides external access to MyTaskly's functionality through HTTP requests to the FastAPI backend, instead of direct database queries.

## Project Structure

```
MyTaskly-mcp/
├── src/
│   ├── core/                      # Core MCP server
│   │   ├── __init__.py
│   │   └── server.py             # FastMCP instance & tool registration
│   │
│   ├── client/                    # HTTP client layer
│   │   ├── __init__.py
│   │   ├── base.py               # Base HTTP client with auth
│   │   ├── categories.py         # Category API endpoints
│   │   ├── tasks.py              # Task API endpoints
│   │   ├── notes.py              # Note API endpoints
│   │   └── health.py             # Health check endpoint
│   │
│   ├── tools/                     # MCP tools (business logic)
│   │   ├── __init__.py
│   │   ├── categories.py         # Category tools (4 methods)
│   │   ├── tasks.py              # Task tools (8 methods)
│   │   ├── notes.py              # Note tools (4 methods)
│   │   ├── meta.py               # Meta tools (3 methods)
│   │   └── health.py             # Health check tool (1 method)
│   │
│   ├── formatters/                # Response formatters
│   │   ├── __init__.py
│   │   └── tasks.py              # Task formatting for React Native UI
│   │
│   ├── auth.py                    # JWT authentication
│   ├── config.py                  # Configuration settings
│   └── http_server.py            # Optional HTTP server wrapper
│
├── tests/                         # Test suite
├── run_server.py                  # Main entry point
├── pyproject.toml                 # Project configuration
└── requirements.txt               # Python dependencies
```

## Layer Responsibilities

### 1. Client Layer (`src/client/`)

**Purpose:** Handle HTTP communication with FastAPI server

**Responsibilities:**
- JWT token generation for user authentication
- HTTP request execution (GET, POST, PUT, DELETE)
- Error handling for network issues
- Response parsing

**Example:**
```python
# src/client/tasks.py
class TaskClient(BaseClient):
    async def get_tasks(self, user_id, filters...):
        token = await self._get_user_token(user_id)
        return await self._get("/tasks/", token, params=filters)
```

### 2. Tools Layer (`src/tools/`)

**Purpose:** MCP tool definitions with business logic

**Responsibilities:**
- JWT authentication verification (from MCP client)
- Input validation
- Calling appropriate client methods
- Response formatting
- Error handling and user-friendly messages

**Example:**
```python
# src/tools/tasks.py
async def get_tasks(authorization: str, filters...) -> Dict[str, Any]:
    """Get tasks with authentication and formatting."""
    user_id = verify_jwt_token(authorization)  # Auth
    tasks = await task_client.get_tasks(user_id, filters)  # HTTP call
    return format_tasks_for_ui(tasks)  # Formatting
```

### 3. Formatters Layer (`src/formatters/`)

**Purpose:** Transform API responses for specific UI frameworks

**Responsibilities:**
- Format dates for Italian locale
- Add color codes for priorities/categories
- Calculate summary statistics
- Generate voice-friendly summaries for TTS
- Create UI hints for mobile rendering

**Example:**
```python
# src/formatters/tasks.py
def format_tasks_for_ui(tasks):
    return {
        "type": "task_list",
        "tasks": [format_task(t) for t in tasks],
        "summary": calculate_stats(tasks),
        "voice_summary": generate_voice_summary(tasks),
        "ui_hints": {...}
    }
```

### 4. Core Layer (`src/core/`)

**Purpose:** MCP server instance and tool registration

**Responsibilities:**
- Create FastMCP server instance
- Register all tools from tools/ modules
- Server configuration

## Available Tools (20 Total)

### Category Tools (4)
1. **get_my_categories** - Get all user categories
2. **create_category** - Create new category
3. **update_category** - Update category by ID
4. **search_categories** - Search categories with fuzzy matching

### Task Tools (8)
5. **get_tasks** - Get tasks with filters (formatted for React Native)
6. **update_task** - Update task fields
7. **complete_task** - Quick shortcut to mark as completed
8. **get_task_stats** - Get statistics (total, completed, by priority, etc.)
9. **get_next_due_task** - Get N upcoming tasks
10. **get_overdue_tasks** - Get all overdue tasks
11. **get_upcoming_tasks** - Get tasks due in next N days
12. **add_task** - Create new task with smart category handling

### Note Tools (4)
13. **get_notes** - Get all user notes
14. **create_note** - Create new note (post-it style)
15. **update_note** - Update note text/position/color
16. **delete_note** - Delete a note

### Meta Tools (3)
17. **get_or_create_category** - Smart category finder/creator with fuzzy matching
18. **move_all_tasks_between_categories** - Bulk move tasks
19. **add_multiple_tasks** - Bulk create tasks

### System Tools (1)
20. **health_check** - Check server health (no auth required)

## Authentication Flow

```
1. User authenticates with frontend → receives MCP JWT token
2. Frontend calls MCP tool with: authorization="Bearer <mcp_jwt_token>"
3. MCP tool verifies MCP token → extracts user_id
4. MCP client generates FastAPI JWT token for user_id
5. MCP client calls FastAPI endpoint with FastAPI token
6. FastAPI validates token → executes operation → returns data
7. MCP tool formats response → returns to frontend
```

**Two JWT Tokens:**
- **MCP Token:** Authenticates MCP client (issued by frontend)
- **FastAPI Token:** Authenticates with backend (generated by MCP client)

## Adding New Tools

### 1. Add HTTP Client Method

```python
# src/client/tasks.py
async def new_operation(self, user_id: int, params...) -> Dict[str, Any]:
    """Call new FastAPI endpoint."""
    token = await self._get_user_token(user_id)
    return await self._post("/new-endpoint", token, json={...})
```

### 2. Add MCP Tool

```python
# src/tools/tasks.py
async def new_tool(authorization: str, params...) -> Dict[str, Any]:
    """Tool documentation here."""
    user_id = verify_jwt_token(authorization)
    result = await task_client.new_operation(user_id, params)
    return format_response(result)
```

### 3. Register Tool

```python
# src/core/server.py
from src.tools.tasks import new_tool
mcp.tool()(new_tool)
```

### 4. Update run_server.py Banner

Add the new tool to the list in `print_banner()`.

## Configuration

**Environment Variables** (`.env`):
```env
FASTAPI_BASE_URL=http://localhost:8080
FASTAPI_API_KEY=your_api_key_here
JWT_SECRET_KEY=your_mcp_jwt_secret
MCP_AUDIENCE=mytaskly-mcp
MCP_SERVER_NAME=MyTaskly-MCP
MCP_SERVER_VERSION=2.0.0
LOG_LEVEL=INFO
```

## Running the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run MCP server (stdio mode)
python run_server.py

# Test with MCP client
# Configure your MCP client to connect to this server
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Benefits of This Architecture

### Scalability
- Each module is small (~200-300 lines max)
- Easy to add new features without touching existing code
- Clear separation of concerns

### Maintainability
- Changes to HTTP client don't affect tool logic
- Changes to formatting don't affect HTTP calls
- Each layer can be tested independently

### Testability
- Mock HTTP responses to test tools
- Mock client to test formatters
- Unit test each component in isolation

### Readability
- Clear file organization by domain (categories, tasks, notes)
- Each file has a single responsibility
- Easy to find and understand code

## Migration from Old Structure

**Old:** All logic in `src/server.py` (240 lines) and `src/client.py` (170 lines)

**New:**
- `src/client/` - 5 files (base + 4 domains)
- `src/tools/` - 5 files (4 domains + health)
- `src/formatters/` - 1 file
- `src/core/` - 1 file (server registration)

**Total:** Much more organized, maintainable, and scalable!
