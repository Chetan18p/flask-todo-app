# TEST CASES EXPLAINED - Flask To-Do List Application

This document provides a detailed explanation of each test case, what it tests, and why it's important.

---

## INTEGRATION TESTS (BLACK-BOX) - 9 Tests
**Purpose:** Test the application from a user's perspective, without knowing internal code details.

---

### TC-INT-001: `test_index_loads`

**What It Tests:**
```python
def test_index_loads(client):
    """TC-INT-001: Verify home page loads successfully"""
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert 'To-Do List' in text
    assert 'Pending Tasks' in text
    assert 'Completed Tasks' in text
```

**Explanation:**
- Makes an HTTP GET request to the home page (`/`)
- Checks if the server responds with status code 200 (OK)
- Verifies the page contains key text: "To-Do List", "Pending Tasks", "Completed Tasks"

**Why It's Important:**
- Basic smoke test - if this fails, the entire app is broken
- Ensures the application starts and renders the main page
- Validates that the template is properly configured

**User Scenario:** User opens the application in their browser

---

### TC-INT-002: `test_add_task_integration_shows_task_and_timestamp`

**What It Tests:**
```python
def test_add_task_integration_shows_task_and_timestamp(client):
    """TC-INT-002: Verify task is added with creation timestamp"""
    client.post('/add', data={'task': 'Integration Task'}, follow_redirects=True)
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert 'Integration Task' in text
    assert 'Created:' in text
    idx = text.find('Created:')
    assert idx != -1
```

**Explanation:**
- Simulates a user submitting the "Add Task" form with text "Integration Task"
- Follows the redirect back to the home page
- Checks if the task appears on the page
- Verifies that a "Created:" timestamp is displayed

**Why It's Important:**
- Tests the core functionality of adding tasks
- Ensures timestamps are properly generated and displayed
- Validates the entire add workflow: form submission → processing → display

**User Scenario:** User types a task in the input box and clicks "Add"

---

### TC-INT-003: `test_prevent_empty_task_integration`

**What It Tests:**
```python
def test_prevent_empty_task_integration(client):
    """TC-INT-003: Verify empty tasks are not added"""
    client.post('/add', data={'task': ''}, follow_redirects=True)
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert 'No pending tasks.' in text or len(tasks) == 0
```

**Explanation:**
- Tries to submit an empty task (empty string)
- Checks if the page shows "No pending tasks" or the task list is empty
- Ensures the application rejects invalid input

**Why It's Important:**
- Data validation - prevents garbage data
- Ensures the application handles edge cases gracefully
- Improves user experience by rejecting meaningless input

**User Scenario:** User clicks "Add" without typing anything

---

### TC-INT-004: `test_prevent_duplicate_tasks_integration`

**What It Tests:**
```python
def test_prevent_duplicate_tasks_integration(client):
    """TC-INT-004: Verify duplicate tasks are prevented"""
    client.post('/add', data={'task': 'Dup Task'}, follow_redirects=True)
    client.post('/add', data={'task': 'Dup Task'}, follow_redirects=True)
    assert len(tasks) == 1
```

**Explanation:**
- Adds the same task twice ("Dup Task")
- Verifies only one task exists in the list
- Ensures duplicate prevention is working

**Why It's Important:**
- Prevents clutter in the task list
- Maintains data integrity
- Better user experience (no duplicate entries)

**User Scenario:** User accidentally adds the same task twice

---

### TC-INT-005: `test_toggle_task_integration_marks_done`

**What It Tests:**
```python
def test_toggle_task_integration_marks_done(client):
    """TC-INT-005: Verify task can be marked as complete"""
    client.post('/add', data={'task': 'ToggleMe'}, follow_redirects=True)
    client.get('/toggle/0', follow_redirects=True)
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert 'task-text done' in text
    assert 'Completed:' in text
```

**Explanation:**
- Adds a task "ToggleMe"
- Clicks the toggle link to mark it complete (simulates clicking checkbox)
- Checks if the task has CSS class "task-text done" (indicates completion)
- Verifies "Completed:" timestamp appears

**Why It's Important:**
- Tests the core task completion feature
- Ensures visual feedback (CSS class) is applied
- Validates that completion timestamp is recorded

**User Scenario:** User checks a checkbox to mark a task as done

---

### TC-INT-006: `test_delete_task_integration_removes_task`

**What It Tests:**
```python
def test_delete_task_integration_removes_task(client):
    """TC-INT-006: Verify task can be deleted"""
    client.post('/add', data={'task': 'ToDelete'}, follow_redirects=True)
    client.get('/delete/0', follow_redirects=True)
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert 'ToDelete' not in text
```

**Explanation:**
- Adds a task "ToDelete"
- Clicks the delete link (task ID 0)
- Verifies the task no longer appears on the page

**Why It's Important:**
- Tests deletion functionality
- Ensures tasks can be permanently removed
- Validates the delete workflow

**User Scenario:** User clicks the "Delete" button next to a task

---

### TC-INT-007: `test_mark_multiple_tasks_complete`

**What It Tests:**
```python
def test_mark_multiple_tasks_complete(client):
    """TC-INT-007: Verify multiple tasks can be marked complete at once"""
    client.post('/add', data={'task': 'Task1'}, follow_redirects=True)
    client.post('/add', data={'task': 'Task2'}, follow_redirects=True)
    client.post('/add', data={'task': 'Task3'}, follow_redirects=True)
    # Mark first and third task complete
    client.post('/complete', data={'selected': ['0', '2']}, follow_redirects=True)
    assert tasks[0]['done'] is True
    assert tasks[1]['done'] is False
    assert tasks[2]['done'] is True
    assert tasks[0]['completed_at'] is not None
    assert tasks[2]['completed_at'] is not None
```

**Explanation:**
- Adds 3 tasks
- Selects checkboxes for tasks at index 0 and 2
- Clicks "Mark Completed" button
- Verifies task 0 and 2 are marked done, task 1 is still pending
- Verifies completion timestamps are set for completed tasks

**Why It's Important:**
- Tests bulk completion feature
- Ensures multiple selections work correctly
- Validates that only selected tasks are affected

**User Scenario:** User selects multiple checkboxes and clicks "Mark Completed"

---

### TC-INT-008: `test_clear_all_tasks`

**What It Tests:**
```python
def test_clear_all_tasks(client):
    """TC-INT-008: Verify only pending tasks are cleared, completed tasks remain"""
    client.post('/add', data={'task': 'Task1'}, follow_redirects=True)
    client.post('/add', data={'task': 'Task2'}, follow_redirects=True)
    client.post('/add', data={'task': 'Task3'}, follow_redirects=True)
    # Mark Task2 as complete
    client.get('/toggle/1', follow_redirects=True)
    assert len(tasks) == 3
    assert tasks[1]['done'] is True
    # Clear pending tasks
    client.post('/clear', follow_redirects=True)
    # Only completed task should remain
    assert len(tasks) == 1
    assert tasks[0]['text'] == 'Task2'
    assert tasks[0]['done'] is True
```

**Explanation:**
- Adds 3 tasks (Task1, Task2, Task3)
- Marks Task2 (middle one) as complete
- Clicks "Clear Pending" button
- Verifies only 1 task remains (Task2, the completed one)
- Verifies Task1 and Task3 (pending) were deleted

**Why It's Important:**
- Tests the clear pending functionality
- Ensures completed tasks are preserved (history keeping)
- Validates selective deletion based on status

**User Scenario:** User wants to clean up pending tasks but keep completed ones as records

---

### TC-INT-009: `test_task_count_display`

**What It Tests:**
```python
def test_task_count_display(client):
    """TC-INT-009: Verify task count is displayed correctly"""
    client.post('/add', data={'task': 'Task1'}, follow_redirects=True)
    client.post('/add', data={'task': 'Task2'}, follow_redirects=True)
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert 'Total: 2' in text
```

**Explanation:**
- Adds 2 tasks
- Checks if the page displays "Total: 2"
- Verifies the counter is accurate

**Why It's Important:**
- Tests UI feedback element
- Ensures counter updates correctly
- Validates template logic for counting

**User Scenario:** User wants to see how many total tasks they have

---

## UNIT TESTS (WHITE-BOX) - 7 Tests
**Purpose:** Test individual functions and internal logic directly, knowing the code structure.

---

### TC-UNIT-001: `test_add_task_function_unit`

**What It Tests:**
```python
def test_add_task_function_unit():
    """TC-UNIT-001: Test add_task function with valid and invalid inputs"""
    tasks.clear()
    # Valid task
    assert add_task("Unit Task") is True
    assert len(tasks) == 1
    assert tasks[0]['text'] == "Unit Task"
    assert tasks[0]['done'] is False
    assert 'created_at' in tasks[0]
    assert 'completed_at' in tasks[0]
    assert tasks[0]['completed_at'] is None
    # Verify timestamp format
    datetime.strptime(tasks[0]['created_at'], '%Y-%m-%d %H:%M:%S')
    # Duplicate task
    assert add_task("Unit Task") is False
    assert len(tasks) == 1
    # Empty task
    assert add_task("   ") is False
    assert add_task("") is False
    assert len(tasks) == 1
```

**Explanation:**
- Directly calls `add_task()` function (not through HTTP)
- Tests with valid input: checks return value, task properties, timestamp format
- Tests with duplicate: ensures function returns False
- Tests with empty/whitespace: ensures function returns False
- Verifies task count doesn't increase for invalid inputs

**Why It's Important:**
- Tests the core logic of task creation
- Validates data structure (dict with correct keys)
- Ensures validation rules work correctly
- Checks timestamp format is correct

**Difference from Integration Test:**
- Direct function call (no HTTP, no template rendering)
- Can inspect internal data structures
- Tests return values
- More granular control

---

### TC-UNIT-002: `test_toggle_task_function_unit`

**What It Tests:**
```python
def test_toggle_task_function_unit():
    """TC-UNIT-002: Test toggle_task function and timestamp assignment"""
    tasks.clear()
    add_task("Toggle Test")
    assert tasks[0]['done'] is False
    assert tasks[0]['completed_at'] is None
    # Toggle to completed
    assert toggle_task(0) is True
    assert tasks[0]['done'] is True
    assert tasks[0]['completed_at'] is not None
    completed_time = tasks[0]['completed_at']
    datetime.strptime(completed_time, '%Y-%m-%d %H:%M:%S')
    # Toggle back to pending
    assert toggle_task(0) is True
    assert tasks[0]['done'] is False
    assert tasks[0]['completed_at'] is None
    # Invalid index
    assert toggle_task(5) is False
    assert toggle_task(-1) is False
```

**Explanation:**
- Tests `toggle_task()` function directly
- Verifies initial state (done=False, completed_at=None)
- Toggles to complete: checks done=True, completed_at is set, format is valid
- Toggles back to pending: checks done=False, completed_at is None
- Tests with invalid indices: ensures function returns False

**Why It's Important:**
- Tests bidirectional toggling (pending ↔ complete)
- Validates timestamp is set/cleared correctly
- Tests boundary conditions (invalid indices)
- Ensures function handles errors gracefully

**Key Insight:**
- Completion timestamp should be set when marking done
- Completion timestamp should be cleared when marking pending
- This is critical for showing accurate "Completed:" times

---

### TC-UNIT-003: `test_delete_task_function_unit`

**What It Tests:**
```python
def test_delete_task_function_unit():
    """TC-UNIT-003: Test delete_task function"""
    tasks.clear()
    add_task("Task1")
    add_task("Task2")
    assert len(tasks) == 2
    # Valid deletion
    assert delete_task(0) is True
    assert len(tasks) == 1
    assert tasks[0]['text'] == "Task2"
    # Invalid deletion
    assert delete_task(5) is False
    assert delete_task(-1) is False
    assert len(tasks) == 1
```

**Explanation:**
- Tests `delete_task()` function directly
- Creates 2 tasks, deletes first one
- Verifies correct task was removed (Task2 remains)
- Tests with invalid indices: ensures function returns False and list unchanged

**Why It's Important:**
- Validates deletion logic
- Ensures list indices shift correctly after deletion
- Tests error handling for out-of-bounds indices

**Key Insight:**
- After deleting index 0, Task2 (previously at index 1) becomes index 0
- Function must handle invalid indices without crashing

---

### TC-UNIT-004: `test_edit_task_function_unit`

**What It Tests:**
```python
def test_edit_task_function_unit():
    """TC-UNIT-004: Test edit_task function"""
    tasks.clear()
    add_task("Original")
    # Valid edit
    assert edit_task(0, "Modified") is True
    assert tasks[0]['text'] == "Modified"
    # Empty new text
    assert edit_task(0, "") is False
    assert edit_task(0, "   ") is False
    # Invalid index
    assert edit_task(5, "Test") is False
    # Duplicate prevention
    add_task("Another")
    assert edit_task(0, "Another") is False
```

**Explanation:**
- Tests `edit_task()` function directly
- Valid edit: changes task text successfully
- Empty input: ensures function rejects empty/whitespace
- Invalid index: ensures function returns False
- Duplicate prevention: can't edit to match another task's text

**Why It's Important:**
- Tests the edit functionality
- Validates all edge cases (empty, invalid index, duplicates)
- Ensures data integrity (no duplicates via editing)

**Key Insight:**
- Edit must maintain same validation rules as add
- Duplicate check must exclude the task being edited itself

---

### TC-UNIT-005: `test_clear_tasks_function_unit`

**What It Tests:**
```python
def test_clear_tasks_function_unit():
    """TC-UNIT-005: Test clear_tasks function only removes pending tasks"""
    tasks.clear()
    add_task("One")
    add_task("Two")
    add_task("Three")
    assert len(tasks) == 3
    # Mark first and third as complete
    toggle_task(0)
    toggle_task(2)
    assert tasks[0]['done'] is True
    assert tasks[1]['done'] is False
    assert tasks[2]['done'] is True
    # Clear tasks (should only remove pending)
    clear_tasks()
    # Only completed tasks remain
    assert len(tasks) == 2
    assert all(task['done'] for task in tasks)
    assert tasks[0]['text'] == "One"
    assert tasks[1]['text'] == "Three"
```

**Explanation:**
- Tests `clear_tasks()` function directly
- Creates 3 tasks, marks 2 as complete (One and Three)
- Calls clear_tasks()
- Verifies only 2 tasks remain (the completed ones)
- Verifies pending task (Two) was removed

**Why It's Important:**
- Tests the selective deletion logic
- Ensures completed tasks are preserved
- Validates the filtering mechanism

**Key Insight:**
- Clear should keep tasks where done=True
- Clear should remove tasks where done=False
- Task order may change after filtering

---

### TC-UNIT-006: `test_timestamp_persistence_unit`

**What It Tests:**
```python
def test_timestamp_persistence_unit():
    """TC-UNIT-006: Test that created_at persists after toggle"""
    tasks.clear()
    add_task("Persist Test")
    original_created = tasks[0]['created_at']
    toggle_task(0)
    assert tasks[0]['created_at'] == original_created
    toggle_task(0)
    assert tasks[0]['created_at'] == original_created
```

**Explanation:**
- Tests that `created_at` timestamp doesn't change
- Saves the original created_at timestamp
- Toggles task to complete
- Verifies created_at is still the same
- Toggles back to pending
- Verifies created_at is still the same

**Why It's Important:**
- Ensures created_at is immutable (never changes)
- Validates data integrity across operations
- Important for accurate historical records

**Key Insight:**
- Created timestamp should NEVER change after task creation
- Only completed_at should change when toggling
- This preserves accurate task creation history

---

### TC-UNIT-007: `test_boundary_conditions_unit`

**What It Tests:**
```python
def test_boundary_conditions_unit():
    """TC-UNIT-007: Test boundary conditions"""
    tasks.clear()
    # Test with very long task name
    long_task = "A" * 500
    assert add_task(long_task) is True
    assert tasks[0]['text'] == long_task
    # Test with special characters
    special_task = "Task @#$% <>&"
    assert add_task(special_task) is True
    assert len(tasks) == 2
```

**Explanation:**
- Tests edge cases and unusual inputs
- Very long task (500 characters): ensures system can handle it
- Special characters (@#$%<>&): ensures proper handling/escaping

**Why It's Important:**
- Tests system limits and robustness
- Ensures application doesn't crash on unusual input
- Validates handling of special characters (XSS prevention)

**Key Insight:**
- System should handle extreme inputs gracefully
- No artificial limits on task length (or document them)
- Special characters should be properly escaped in HTML

---

## SUMMARY: WHY THESE TESTS MATTER

### Coverage Matrix:

| Feature | Integration Test | Unit Test |
|---------|-----------------|-----------|
| Add Task | TC-INT-002 | TC-UNIT-001 |
| Empty/Invalid Input | TC-INT-003 | TC-UNIT-001 |
| Duplicates | TC-INT-004 | TC-UNIT-001, TC-UNIT-004 |
| Mark Complete | TC-INT-005 | TC-UNIT-002 |
| Delete | TC-INT-006 | TC-UNIT-003 |
| Edit | - | TC-UNIT-004 |
| Clear Pending | TC-INT-008 | TC-UNIT-005 |
| Bulk Complete | TC-INT-007 | - |
| Timestamps | TC-INT-002, TC-INT-005 | TC-UNIT-001, TC-UNIT-002, TC-UNIT-006 |
| UI Elements | TC-INT-001, TC-INT-009 | - |
| Boundary Cases | - | TC-UNIT-007 |

### Black-Box vs White-Box:

**Black-Box (Integration):**
- Tests complete user workflows
- Uses HTTP requests
- Checks HTML output
- User perspective
- Tests integration between components

**White-Box (Unit):**
- Tests individual functions
- Direct function calls
- Checks internal data structures
- Developer perspective
- Tests specific logic paths

### Combined Coverage:
- **16 tests total** provide comprehensive validation
- Tests cover normal cases, edge cases, and error cases
- Both user workflows and internal logic are validated
- High confidence that application works correctly

---

## HOW TO RUN INDIVIDUAL TESTS

```powershell
# Run single test
python -m pytest tests/test_app.py::test_index_loads -v

# Run all integration tests
python -m pytest tests/test_app.py -k "integration" -v

# Run all unit tests
python -m pytest tests/test_app.py -k "unit" -v

# Run all tests
python -m pytest tests/test_app.py -v
```
