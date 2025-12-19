#!/usr/bin/env python
"""
Run the MyTaskly MCP server with all registered tools.

Usage:
    python run_server.py              # Run MCP server in stdio mode
"""

from src.core.server import mcp
from src.config import settings


def print_banner():
    """Print startup banner with server information."""
    print("=" * 60)
    print(f"[*] Starting {settings.mcp_server_name} v{settings.mcp_server_version}")
    print("=" * 60)
    print(f"FastAPI Backend: {settings.fastapi_base_url}")
    print(f"JWT Audience: {settings.mcp_audience}")
    print(f"Log Level: {settings.log_level}")
    print("=" * 60)
    print("\n[+] Registered Tools:")

    # Category tools
    print("\n  Category Management:")
    print("    1. get_my_categories - Get all user categories")
    print("    2. create_category - Create new category")
    print("    3. update_category - Update category by ID")
    print("    4. search_categories - Search categories by name")

    # Task tools
    print("\n  Task Management:")
    print("    5. get_tasks - Get tasks with filters (formatted for React Native)")
    print("    6. update_task - Update task fields")
    print("    7. complete_task - Mark task as completed")
    print("    8. get_task_stats - Get task statistics")
    print("    9. get_next_due_task - Get upcoming tasks")
    print("   10. get_overdue_tasks - Get overdue tasks")
    print("   11. get_upcoming_tasks - Get tasks due in N days")
    print("   12. add_task - Create new task with smart category handling")

    # Note tools
    print("\n  Note Management:")
    print("   13. get_notes - Get all user notes")
    print("   14. create_note - Create new note (post-it style)")
    print("   15. update_note - Update note text/position/color")
    print("   16. delete_note - Delete a note")

    # Meta tools
    print("\n  Advanced Operations:")
    print("   17. get_or_create_category - Smart category finder/creator")
    print("   18. move_all_tasks_between_categories - Bulk move tasks")
    print("   19. add_multiple_tasks - Bulk create tasks")

    # Health check
    print("\n  System:")
    print("   20. health_check - Check server health (no auth required)")

    print("\n[+] Authentication: OAuth 2.1 JWT (Bearer token)")
    print("=" * 60)
    print()


if __name__ == "__main__":
    print_banner()

    # Run the MCP server
    print("[+] Starting MCP server in stdio mode...")
    print("[+] Ready to accept connections\n")
    mcp.run()
