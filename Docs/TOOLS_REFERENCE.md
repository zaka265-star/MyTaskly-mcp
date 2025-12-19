# MyTaskly MCP - Complete Tools Reference

Quick reference for all 20 available MCP tools.

---

## Authentication

All tools (except `health_check`) require authentication via JWT token:

```python
authorization = "Bearer <your_jwt_token>"
```

---

## Category Tools (4)

### 1. get_my_categories
Get all user categories

### 2. create_category
Create a new category

### 3. update_category
Update category by ID

### 4. search_categories
Search categories with fuzzy matching

---

## Task Tools (8)

### 5. get_tasks
Get tasks with filters (formatted for React Native)

### 6. update_task
Update task fields

### 7. complete_task
Quick shortcut to mark task as completed

### 8. get_task_stats
Get task statistics

### 9. get_next_due_task
Get N upcoming tasks

### 10. get_overdue_tasks
Get all overdue tasks

### 11. get_upcoming_tasks
Get tasks due in next N days

### 12. add_task
Create new task with smart category handling

---

## Note Tools (4)

### 13. get_notes
Get all user notes

### 14. create_note
Create new note (post-it style)

### 15. update_note
Update note text/position/color

### 16. delete_note
Delete a note

---

## Meta Tools (3)

### 17. get_or_create_category
Smart category finder/creator

### 18. move_all_tasks_between_categories
Bulk move tasks between categories

### 19. add_multiple_tasks
Bulk create tasks

---

## System Tools (1)

### 20. health_check
Check server health (NO AUTH REQUIRED)

---

For detailed usage and examples, see the tool implementations in src/tools/
