# MyTaskly MCP Server

**Model Context Protocol (MCP) server** for [MyTaskly](https://github.com/Gabry848/MyTaskly-app) with **OAuth 2.1 JWT authentication** and seamless integration with the [FastAPI backend](https://github.com/Gabry848/MyTaskly-server).

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-2025-00D8FF?style=flat-square)](https://modelcontextprotocol.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Integration-00D8FF?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 📋 Key Features

### 🔐 Enterprise-Grade Authentication
- **OAuth 2.1 JWT** - Secure token-based authentication following MCP 2025 standards (RFC 8707)
- **Multi-User Support** - Single deployment serves all users via JWT token validation
- **Audience Claim Validation** - Prevents token reuse across services

### 🚀 High-Performance Integration
- **HTTP API Gateway** - Communicates with FastAPI backend, no direct database access
- **Stateless Architecture** - No session management, fully scalable
- **Connection Pooling** - Optimized HTTP client for high throughput

### 📱 Mobile-First Design
- **React Native Optimized** - Returns data formatted for native mobile components
- **Voice-Friendly Responses** - Includes voice summaries for TTS in chat applications
- **Pre-formatted UI Data** - Emojis, colors, and formatted dates ready for display

---

## 🛠️ Available MCP Tools (20 Total)

The MCP server provides **20 tools** organized into 5 categories for comprehensive task management.

### 📋 Task Tools (8)

| Tool | Description | Auth Required |
|------|-------------|---------------|
| `get_tasks` | Get tasks with filters (formatted for React Native) | ✅ Yes |
| `add_task` | Create new task with smart category handling | ✅ Yes |
| `update_task` | Update task fields | ✅ Yes |
| `complete_task` | Quick shortcut to mark task as completed | ✅ Yes |
| `get_task_stats` | Get statistics (total, completed, by priority) | ✅ Yes |
| `get_next_due_task` | Get N upcoming tasks | ✅ Yes |
| `get_overdue_tasks` | Get all overdue tasks | ✅ Yes |
| `get_upcoming_tasks` | Get tasks due in next N days | ✅ Yes |

**Example Response - `get_tasks`:**
```json
{
  "type": "task_list",
  "tasks": [
    {
      "id": 123,
      "title": "Pizza",
      "endTimeFormatted": "Venerdì 15 dicembre, 18:00",
      "category": "Cibo",
      "categoryColor": "#EF4444",
      "priority": "Alta",
      "priorityEmoji": "⚡",
      "status": "Pending",
      "actions": {
        "canEdit": true,
        "canDelete": true,
        "canComplete": true
      }
    }
  ],
  "summary": {
    "total": 10,
    "pending": 5,
    "completed": 3,
    "high_priority": 2
  },
  "voice_summary": "Hai 10 task, di cui 2 ad alta priorità. 5 sono in sospeso e 3 completati."
}
```

---

### 📂 Category Tools (4)

| Tool | Description | Auth Required |
|------|-------------|---------------|
| `get_my_categories` | Get all user categories | ✅ Yes |
| `create_category` | Create new category | ✅ Yes |
| `update_category` | Update category by ID | ✅ Yes |
| `search_categories` | Search categories with fuzzy matching | ✅ Yes |

**Example Response - `get_my_categories`:**
```json
{
  "categories": [
    {
      "category_id": 1,
      "name": "Lavoro",
      "description": "Task di lavoro",
      "is_shared": true,
      "owner_id": 1,
      "permission_level": "READ_WRITE"
    }
  ],
  "total": 5,
  "owned": 3,
  "shared_with_me": 2
}
```

---

### 📝 Note Tools (4)

| Tool | Description | Auth Required |
|------|-------------|---------------|
| `get_notes` | Get all user notes | ✅ Yes |
| `create_note` | Create new note (post-it style) | ✅ Yes |
| `update_note` | Update note text/position/color | ✅ Yes |
| `delete_note` | Delete a note | ✅ Yes |

**Example Response - `create_note`:**
```json
{
  "note_id": 456,
  "title": "Comprare il latte",
  "color": "#FFEB3B",
  "position_x": 100.5,
  "position_y": 250.0,
  "created_at": "2025-01-15T10:30:00Z",
  "message": "✅ Nota creata con successo"
}
```

---

### 🔧 Meta Tools (3)

| Tool | Description | Auth Required |
|------|-------------|---------------|
| `get_or_create_category` | Smart category finder/creator with fuzzy matching | ✅ Yes |
| `move_all_tasks_between_categories` | Bulk move tasks between categories | ✅ Yes |
| `add_multiple_tasks` | Bulk create multiple tasks at once | ✅ Yes |

---

### ⚕️ System Tools (1)

| Tool | Description | Auth Required |
|------|-------------|---------------|
| `health_check` | Check server health and connectivity | ❌ No |

**Example Response - `health_check`:**
```json
{
  "mcp_server": "healthy",
  "fastapi_server": "healthy",
  "fastapi_url": "http://localhost:8080",
  "timestamp": "2025-01-15T10:30:00Z",
  "version": "2.0.0"
}
```

---

## 🚀 Getting Started

### Usage Options

You have **two ways** to use the MyTaskly MCP Server:

#### Option 1: Use Official Public Server (Recommended)

Use the **official MyTaskly MCP server** (coming soon) - no setup required!

```bash
# Configure your MCP client to connect to:
# https://mcp.mytasklyapp.com (URL will be published soon)
```

**Benefits:**
- ✅ No installation or configuration needed
- ✅ Always up-to-date with latest features
- ✅ Managed and monitored by MyTaskly team
- ✅ Works out-of-the-box with MyTaskly mobile app

---

#### Option 2: Self-Host (Advanced Users)

Run your own local MCP server instance.

**Prerequisites:**
- **Python 3.11+** (virtual environment recommended)
- **MyTaskly FastAPI Server** running locally (see [MyTaskly-server](https://github.com/Gabry848/MyTaskly-server))
- **JWT Secret Key** matching your FastAPI server configuration
- **Modified MyTaskly App** configured to use your custom server

**Quick Start (5 minutes):**

```bash
git clone https://github.com/Gabry848/MyTaskly-mcp.git
cd MyTaskly-mcp
python -m venv venv && pip install -r requirements.txt
cp .env.example .env && python main.py
```

⚠️ **Important:** When self-hosting, you must also:
1. Run a local instance of [MyTaskly-server](https://github.com/Gabry848/MyTaskly-server)
2. Modify the MyTaskly mobile app to point to your custom server URLs

---

### Self-Hosting Setup Guide

#### 1. Clone & Install

```bash
# Clone the repository
git clone https://github.com/Gabry848/MyTaskly-mcp.git
cd MyTaskly-mcp

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Environment Variables

Create `.env` file in the root directory:

```env
# ============ FASTAPI BACKEND ============
FASTAPI_BASE_URL=http://localhost:8080
FASTAPI_API_KEY=your_api_key_here

# ============ JWT CONFIGURATION ============
# CRITICAL: Must match FastAPI server configuration!
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
MCP_AUDIENCE=mytaskly-mcp

# ============ SERVER CONFIGURATION ============
MCP_SERVER_NAME=MyTaskly-MCP
MCP_SERVER_VERSION=2.0.0
LOG_LEVEL=INFO
```

⚠️ **CRITICAL:** `JWT_SECRET_KEY` MUST match your FastAPI server's `SECRET_KEY` environment variable!

#### 3. Start the MCP Server

```bash
python main.py
```

The server will start in **stdio mode** and display the available tools. Configure your MCP client to connect to this server.

---

## 🔐 Authentication & Security

### OAuth 2.1 Flow

The MCP server uses JWT tokens following OAuth 2.1 and RFC 8707 standards:

```
┌─────────────────┐
│  Mobile Client  │
│  (React Native) │
└────────┬────────┘
         │ 1. Login request
         ▼
┌─────────────────┐
│  FastAPI Server │  2. Validates credentials
│  (Auth Server)  │  3. Generates JWT with MCP audience claim
└────────┬────────┘
         │ 4. Returns JWT token
         ▼
┌─────────────────┐
│  Mobile Client  │  5. Stores token securely
└────────┬────────┘
         │ 6. Calls MCP tools with Authorization header
         ▼
┌─────────────────┐
│   MCP Server    │  7. Validates JWT signature
│ (This project)  │  8. Verifies audience claim
│                 │  9. Extracts user_id from token
└────────┬────────┘
         │ 10. Makes HTTP request to FastAPI with user_id
         ▼
┌─────────────────┐
│  FastAPI Server │  11. Returns user-specific data
│ (Resource API)  │
└────────┬────────┘
         │ 12. Formats data for mobile UI
         ▼
┌─────────────────┐
│   MCP Server    │  13. Returns formatted response
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Mobile Client  │  14. Renders UI / plays TTS
└─────────────────┘
```

### JWT Token Structure

The JWT must include these claims (following RFC 7519 and RFC 8707):

```json
{
  "sub": "123",                              // User ID (required)
  "aud": "mcp://mytaskly-mcp-server",       // Audience (required, RFC 8707)
  "iss": "https://api.mytasklyapp.com",     // Issuer (optional)
  "exp": 1735689600,                         // Expiration timestamp (required)
  "iat": 1735686000,                         // Issued at timestamp (required)
  "scope": "tasks:read tasks:write notes:write" // Scopes (optional)
}
```

**Security Features:**
| Feature | Implementation |
|---------|----------------|
| **Signature Validation** | HS256 with shared secret |
| **Audience Claim** | Prevents token reuse across services |
| **Expiration Check** | Automatic token invalidation |
| **User Isolation** | Each request scoped to authenticated user |

### Getting a JWT Token

**Option 1: From FastAPI (Production)**

You need to add this endpoint to your FastAPI server:

```python
# src/app/api/routes/auth.py

@router.post("/auth/mcp-token")
async def get_mcp_token(current_user: User = Depends(get_current_user)):
    """Generate JWT token for MCP server access."""
    payload = {
        "sub": str(current_user.user_id),
        "aud": "mcp://mytaskly-mcp-server",
        "iss": "https://api.mytasklyapp.com",
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow(),
        "scope": "tasks:read tasks:write categories:read notes:read notes:write"
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    return {"mcp_token": token, "expires_in": 1800}
```

**Option 2: Generate Test Token (Development)**

```python
from src.auth import create_test_token

# Generate test token for user_id=1
token = create_test_token(user_id=1, expires_minutes=30)
print(f"Test Token: {token}")
```

## 🧪 Testing & Development

### Manual Testing with Python

```python
import asyncio
from src.auth import create_test_token
from src.server import get_tasks, get_categories, create_note

async def test_mcp_tools():
    """Test all MCP tools with a generated token."""

    # Generate test token for user_id=1 (expires in 30 minutes)
    token = create_test_token(user_id=1, expires_minutes=30)
    auth_header = f"Bearer {token}"

    print("🔑 Generated test token for user_id=1\n")

    # Test 1: Get Tasks
    print("1️⃣ Testing get_tasks...")
    tasks = await get_tasks(authorization=auth_header)
    print(f"   ✅ Retrieved {tasks['summary']['total']} tasks")
    print(f"   📊 Summary: {tasks['summary']}")
    print(f"   🎤 Voice: {tasks['voice_summary']}\n")

    # Test 2: Get Categories
    print("2️⃣ Testing get_categories...")
    categories = await get_categories(authorization=auth_header)
    print(f"   ✅ Retrieved {categories['total']} categories")
    print(f"   📂 Owned: {categories.get('owned', 0)}")
    print(f"   🤝 Shared: {categories.get('shared_with_me', 0)}\n")

    # Test 3: Create Note
    print("3️⃣ Testing create_note...")
    note = await create_note(
        authorization=auth_header,
        title="Test note from MCP",
        color="#4CAF50",
        position_x=100.0,
        position_y=200.0
    )
    print(f"   ✅ Created note #{note['note_id']}")
    print(f"   📝 Title: {note['title']}")
    print(f"   🎨 Color: {note['color']}\n")

    print("✅ All tests completed successfully!")

# Run tests
if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
```

### Testing with cURL

```bash
# 1. Generate a test JWT token
python -c "from src.auth import create_test_token; print(create_test_token(1))"

# 2. Export token to environment variable (replace with actual token)
export MCP_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 3. Test get_tasks
curl -X POST http://localhost:8000/mcp/get_tasks \
  -H "Authorization: Bearer $MCP_TOKEN" \
  -H "Content-Type: application/json"

# 4. Test get_categories
curl -X POST http://localhost:8000/mcp/get_categories \
  -H "Authorization: Bearer $MCP_TOKEN" \
  -H "Content-Type: application/json"

# 5. Test create_note
curl -X POST http://localhost:8000/mcp/create_note \
  -H "Authorization: Bearer $MCP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Meeting notes",
    "color": "#FF5722",
    "position_x": 150.5,
    "position_y": 300.0
  }'

# 6. Test health_check (no auth required)
curl -X GET http://localhost:8000/mcp/health_check
```

### Automated Test Suite

```bash
# Run all unit tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_auth.py -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html

# Run with output
python -m pytest tests/ -v -s
```

---

## 📱 Integration with React Native

The `get_tasks` tool returns data optimized for React Native components:

```tsx
import { FlatList, View, Text } from 'react-native';

async function fetchTasks() {
  // Get JWT token from your auth system
  const token = await getAuthToken();

  // Call MCP server
  const response = await mcpClient.call('get_tasks', {
    authorization: `Bearer ${token}`
  });

  return response;
}

function TasksList() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchTasks().then(setData);
  }, []);

  if (!data) return <Loading />;

  return (
    <View>
      {/* Voice summary for accessibility */}
      <Text accessible>{data.voice_summary}</Text>

      {/* Render tasks list */}
      <FlatList
        data={data.tasks}
        renderItem={({ item }) => (
          <TaskCard
            title={item.title}
            date={item.endTimeFormatted}
            category={item.category}
            categoryColor={item.categoryColor}
            priority={item.priorityEmoji}
          />
        )}
      />
    </View>
  );
}
```

## 🎤 Integration with Voice Chat

The response includes `voice_summary` for TTS:

```python
# In your chatbot service
response = await mcp_client.call('get_tasks', {
    'authorization': f'Bearer {user_jwt}'
})

# For visual display
ui_data = response['tasks']

# For voice output
tts_text = response['voice_summary']
# "Hai 10 task, di cui 2 ad alta priorità. 5 sono in sospeso e 3 completati."
```

## 🔒 Security Best Practices

1. **Always use HTTPS** in production
2. **Keep JWT_SECRET_KEY secure** - never commit to git
3. **Use short-lived tokens** (15-30 minutes)
4. **Implement token refresh** in your client
5. **Validate audience claim** (RFC 8707) - prevents token reuse
6. **Log authentication failures** for monitoring

## 🏗️ Architecture & Project Structure

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MyTaskly Ecosystem                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│   ┌─────────────────┐                                       │
│   │  Mobile Client  │  1. User authentication               │
│   │ (React Native)  │  2. Receives JWT token                │
│   └────────┬────────┘  3. Calls MCP tools                   │
│            │                                                  │
│            ▼                                                  │
│   ┌─────────────────┐                                       │
│   │   MCP Server    │  4. Validates JWT (OAuth 2.1)        │
│   │ (This project)  │  5. Extracts user_id from token       │
│   └────────┬────────┘  6. Formats data for mobile UI        │
│            │                                                  │
│            ▼                                                  │
│   ┌─────────────────┐                                       │
│   │  FastAPI Server │  7. Handles business logic            │
│   │ (MyTaskly-API)  │  8. Manages database operations       │
│   └────────┬────────┘  9. Returns raw data                  │
│            │                                                  │
│            ▼                                                  │
│   ┌─────────────────┐                                       │
│   │   PostgreSQL    │  10. Persistent storage               │
│   │    Database     │  11. Triggers & notifications         │
│   └─────────────────┘                                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Project Structure

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
├── main.py                        # Main entry point
├── pyproject.toml                 # Project configuration
├── requirements.txt               # Python dependencies
├── ARCHITECTURE.md                # Detailed architecture documentation
└── README.md                      # This file
```

### Layer Architecture

| Layer | Files | Responsibility |
|-------|-------|----------------|
| **Core Layer** | `src/core/` | MCP server instance and tool registration |
| **Tools Layer** | `src/tools/` | MCP tool definitions with business logic (20 tools) |
| **Client Layer** | `src/client/` | HTTP communication with FastAPI server |
| **Formatters Layer** | `src/formatters/` | Transform API responses for React Native UI |

### Key Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **MCP Server** | FastMCP with asyncio | Request handling & tool orchestration |
| **JWT Authentication** | PyJWT with HS256 | Secure token-based authentication |
| **HTTP Client** | httpx (async) | FastAPI backend communication |
| **Data Formatting** | Custom formatters | Mobile-optimized response structure |

📚 **For detailed architecture information**, see [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🛠️ Development Guide

### Adding New MCP Tools

Follow the layered architecture pattern:

#### 1. Add HTTP Client Method

```python
# src/client/tasks.py
async def new_operation(self, user_id: int, params...) -> Dict[str, Any]:
    """Call new FastAPI endpoint."""
    token = await self._get_user_token(user_id)
    return await self._post("/new-endpoint", token, json={...})
```

#### 2. Add MCP Tool

```python
# src/tools/tasks.py
async def new_tool(authorization: str, params...) -> Dict[str, Any]:
    """Tool documentation here."""
    user_id = verify_jwt_token(authorization)
    result = await task_client.new_operation(user_id, params)
    return format_response(result)
```

#### 3. Register Tool

```python
# src/core/server.py
from src.tools.tasks import new_tool
mcp.tool()(new_tool)
```

#### 4. Update main.py Banner

Add the new tool to the list in `print_banner()`.

**For more details**, see [ARCHITECTURE.md](ARCHITECTURE.md#adding-new-tools)

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/

# Type checking with mypy
mypy src/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html
```

### Common Development Tasks

| Task | Command |
|------|---------|
| **Run server** | `python main.py` |
| **Generate test token** | `python -c "from src.auth import create_test_token; print(create_test_token(1))"` |
| **Run tests** | `pytest tests/ -v` |
| **Check coverage** | `pytest tests/ --cov=src` |
| **Format code** | `black src/ tests/` |
| **Install dependencies** | `pip install -r requirements.txt` |

---

## 📚 Resources & Related Projects

### MyTaskly Ecosystem

- **[MyTaskly Mobile App](https://github.com/Gabry848/MyTaskly-app)** - React Native frontend
- **[MyTaskly Server](https://github.com/Gabry848/MyTaskly-server)** - FastAPI backend
- **MyTaskly MCP** (this project) - Model Context Protocol server

### Documentation

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [RFC 8707 - Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707)
- [RFC 7519 - JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)

---

## 🤝 Contributing

We welcome contributions! This project is part of the MyTaskly ecosystem.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/my-feature`
3. **Make your changes** with clear commit messages
4. **Add tests** for new functionality
5. **Ensure tests pass**: `pytest tests/ -v`
6. **Format code**: `black src/ tests/`
7. **Submit a pull request**

### Development Workflow

```bash
# 1. Clone your fork
git clone https://github.com/YOUR_USERNAME/MyTaskly-mcp.git
cd MyTaskly-mcp

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Make changes and test
pytest tests/ -v

# 4. Commit with descriptive message
git commit -m "feat: add new MCP tool for task statistics"

# 5. Push and create PR
git push origin feature/my-feature
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

The MIT License allows you to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

---

## 📞 Support & Feedback

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/MyTaskly-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/MyTaskly-mcp/discussions)
- **Email**: support@mytasklyapp.com

---

<div align="center">

Made with ❤️ by [Gabry848](https://github.com/Gabry848) as part of the **MyTaskly** project

**Starring is appreciated!** ⭐

[⬆ Back to Top](#mytaskly-mcp-server)

</div>
