# Migration Guide - From Old to New Structure

## What Changed?

### Old Structure (v1.0)
```
src/
├── server.py         # All MCP tools in one file (240 lines)
├── client.py         # All HTTP logic in one file (170 lines)
├── formatters.py     # Response formatting
├── auth.py
└── config.py
```

### New Structure (v2.0)
```
src/
├── core/
│   └── server.py            # Server registration only
├── client/
│   ├── base.py              # Shared HTTP logic
│   ├── categories.py        # Category endpoints
│   ├── tasks.py             # Task endpoints
│   ├── notes.py             # Note endpoints
│   └── health.py            # Health endpoint
├── tools/
│   ├── categories.py        # Category tools
│   ├── tasks.py             # Task tools
│   ├── notes.py             # Note tools
│   ├── meta.py              # Meta tools
│   └── health.py            # Health tool
├── formatters/
│   └── tasks.py             # Task formatters
├── auth.py                  # Unchanged
└── config.py                # Unchanged
```

## Breaking Changes

### Import Changes

**Old:**
```python
from src.server import mcp
from src.client import fastapi_client
from src.formatters import format_tasks_for_ui
```

**New:**
```python
from src.core.server import mcp
from src.client import task_client, category_client, note_client
from src.formatters import format_tasks_for_ui
```

### Client Usage Changes

**Old:**
```python
tasks = await fastapi_client.get_tasks(user_id)
```

**New:**
```python
tasks = await task_client.get_tasks(user_id)
```

## Migration Steps

### 1. Backup Old Files (Optional)

```bash
cd E:/MyTaskly/MyTaskly-mcp
mkdir backup
cp src/server.py backup/
cp src/client.py backup/
```

### 2. Install/Update Dependencies

```bash
pip install -r requirements.txt
```

### 3. Update Configuration

No changes needed - `.env` file remains the same.

### 4. Test the New Structure

```bash
# Test server startup
python run_server.py

# You should see a banner with all 20 tools listed
```

### 5. Update MCP Client Configuration

If you're using the MCP client from a different codebase:

**Before:**
```json
{
  "mcp_server_path": "E:/MyTaskly/MyTaskly-mcp/src/server.py"
}
```

**After:**
```json
{
  "mcp_server_path": "E:/MyTaskly/MyTaskly-mcp/run_server.py"
}
```

### 6. Verify All Tools Work

Run the test suite to verify everything works:

```bash
pytest tests/ -v
```

## Tool Mapping

All tools remain the same, just organized differently:

| Tool Name | Old Location | New Location |
|-----------|-------------|--------------|
| get_tasks | src/server.py | src/tools/tasks.py |
| get_categories | src/server.py | src/tools/categories.py |
| create_note | src/server.py | src/tools/notes.py |
| health_check | src/server.py | src/tools/health.py |
| ... | ... | ... |

## Rollback Plan

If you need to rollback to the old structure:

```bash
# Restore backup files
cp backup/server.py src/
cp backup/client.py src/

# Update run_server.py to use old server
# Edit run_server.py to import from src.server instead of src.core.server
```

## Benefits of New Structure

1. **Easier to Find Code**: Want to add a task feature? Go to `src/tools/tasks.py`
2. **Easier to Test**: Each module can be tested independently
3. **Easier to Maintain**: Changes to one domain don't affect others
4. **Better Performance**: Only import what you need
5. **Clearer Responsibilities**: Each file has a single, clear purpose

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'src.core'"

**Solution:**
```bash
# Make sure you're in the project root
cd E:/MyTaskly/MyTaskly-mcp

# Make sure __init__.py files exist
ls src/core/__init__.py
ls src/client/__init__.py
ls src/tools/__init__.py
```

### Issue: "Tool not found"

**Solution:** Check that the tool is registered in `src/core/server.py`:

```python
from src.tools.tasks import get_tasks
mcp.tool()(get_tasks)
```

### Issue: "Authentication failed"

**Solution:** This is unchanged - make sure your `.env` has:
```env
JWT_SECRET_KEY=your_secret_here
FASTAPI_API_KEY=your_api_key_here
```

## Testing Checklist

After migration, verify:

- [ ] Server starts without errors: `python run_server.py`
- [ ] All 20 tools are listed in banner
- [ ] Health check works (no auth): Call `health_check()`
- [ ] Authentication works: Call any tool with valid JWT
- [ ] Category tools work: Test `get_my_categories`
- [ ] Task tools work: Test `get_tasks`
- [ ] Note tools work: Test `get_notes`
- [ ] Meta tools work: Test `add_multiple_tasks`

## Support

If you encounter issues during migration:

1. Check `ARCHITECTURE.md` for structural details
2. Review the test files in `tests/` for usage examples
3. Compare with backup files to see what changed
4. Check the FastMCP documentation for any breaking changes

## What Stays the Same

- Authentication flow (MCP JWT → FastAPI JWT)
- All tool signatures and parameters
- Response formats
- Configuration in `.env`
- External API endpoints
- Database schema (this is external MCP, no DB access)
