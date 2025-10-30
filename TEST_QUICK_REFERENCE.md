# TEST CASES - QUICK REFERENCE GUIDE

## 🔵 INTEGRATION TESTS (BLACK-BOX) - User Perspective

| ID | Test Name | What It Does | Pass Criteria |
|----|-----------|--------------|---------------|
| **TC-INT-001** | `test_index_loads` | Opens home page | Page loads with 200, shows "To-Do List" |
| **TC-INT-002** | `test_add_task_integration_shows_task_and_timestamp` | Adds a task via form | Task appears with "Created:" timestamp |
| **TC-INT-003** | `test_prevent_empty_task_integration` | Tries to add empty task | Empty task is rejected |
| **TC-INT-004** | `test_prevent_duplicate_tasks_integration` | Adds same task twice | Only 1 task exists |
| **TC-INT-005** | `test_toggle_task_integration_marks_done` | Marks task complete | Task shows "done" class + "Completed:" time |
| **TC-INT-006** | `test_delete_task_integration_removes_task` | Deletes a task | Task disappears from page |
| **TC-INT-007** | `test_mark_multiple_tasks_complete` | Selects multiple tasks, marks complete | Selected tasks marked done with timestamps |
| **TC-INT-008** | `test_clear_all_tasks` | Clears pending tasks | Only completed tasks remain |
| **TC-INT-009** | `test_task_count_display` | Checks task counter | Shows "Total: X" correctly |

---

## 🟢 UNIT TESTS (WHITE-BOX) - Developer Perspective

| ID | Test Name | What It Tests | Pass Criteria |
|----|-----------|---------------|---------------|
| **TC-UNIT-001** | `test_add_task_function_unit` | `add_task()` function | Returns True for valid, False for invalid/duplicate |
| **TC-UNIT-002** | `test_toggle_task_function_unit` | `toggle_task()` function | Sets/clears `completed_at` correctly |
| **TC-UNIT-003** | `test_delete_task_function_unit` | `delete_task()` function | Removes correct task, handles invalid indices |
| **TC-UNIT-004** | `test_edit_task_function_unit` | `edit_task()` function | Changes text, rejects empty/duplicates |
| **TC-UNIT-005** | `test_clear_tasks_function_unit` | `clear_tasks()` function | Keeps completed, removes pending |
| **TC-UNIT-006** | `test_timestamp_persistence_unit` | Timestamp immutability | `created_at` never changes |
| **TC-UNIT-007** | `test_boundary_conditions_unit` | Edge cases | Handles long strings, special characters |

---

## 📊 COVERAGE BY FEATURE

| Feature | Integration Test | Unit Test | Total Coverage |
|---------|-----------------|-----------|----------------|
| **Add Task** | TC-INT-002, TC-INT-003 | TC-UNIT-001 | 3 tests |
| **Complete Task** | TC-INT-005, TC-INT-007 | TC-UNIT-002 | 3 tests |
| **Delete Task** | TC-INT-006 | TC-UNIT-003 | 2 tests |
| **Edit Task** | - | TC-UNIT-004 | 1 test |
| **Clear Pending** | TC-INT-008 | TC-UNIT-005 | 2 tests |
| **Timestamps** | TC-INT-002, TC-INT-005 | TC-UNIT-001, TC-UNIT-002, TC-UNIT-006 | 5 tests |
| **Validation** | TC-INT-003, TC-INT-004 | TC-UNIT-001, TC-UNIT-004, TC-UNIT-007 | 5 tests |
| **UI** | TC-INT-001, TC-INT-009 | - | 2 tests |

**TOTAL: 16 tests covering all features**

---

## 🎯 TEST PRIORITY

### Critical (Must Pass)
- TC-INT-001 (App loads)
- TC-INT-002 (Add task)
- TC-UNIT-001 (Add function)
- TC-UNIT-002 (Toggle function)

### High Priority
- TC-INT-005 (Mark complete)
- TC-INT-006 (Delete)
- TC-INT-007 (Bulk complete)
- TC-UNIT-003 (Delete function)

### Medium Priority
- TC-INT-004 (Duplicates)
- TC-INT-008 (Clear pending)
- TC-UNIT-004 (Edit function)
- TC-UNIT-005 (Clear function)
- TC-UNIT-006 (Timestamp persistence)

### Low Priority
- TC-INT-003 (Empty validation)
- TC-INT-009 (Counter display)
- TC-UNIT-007 (Boundary cases)

---

## 🔍 WHAT EACH TEST TYPE DOES

### Integration Tests (Black-Box)
```
User Action → HTTP Request → Server Processing → HTML Response → Validation
```
**Example:** User clicks "Add" button
- Sends POST to `/add`
- Server processes request
- Redirects to home page
- Check if task appears in HTML

### Unit Tests (White-Box)
```
Input → Function Call → Return Value/State Change → Validation
```
**Example:** Call `add_task("Test")`
- Function validates input
- Adds to tasks list
- Returns True
- Check return value and list contents

---

## 🚀 QUICK TEST COMMANDS

```powershell
# Run all tests
python -m pytest tests/test_app.py -v

# Run only integration tests
python -m pytest tests/test_app.py -k "integration" -v

# Run only unit tests
python -m pytest tests/test_app.py -k "unit" -v

# Run specific test
python -m pytest tests/test_app.py::test_add_task_function_unit -v

# Run with coverage report
python -m pytest tests/test_app.py --cov=app --cov-report=html
```

---

## 📝 COMMON TEST PATTERNS

### Pattern 1: Add and Verify (Integration)
```python
client.post('/add', data={'task': 'MyTask'})
resp = client.get('/')
assert 'MyTask' in resp.get_data(as_text=True)
```

### Pattern 2: Direct Function Test (Unit)
```python
result = add_task("MyTask")
assert result is True
assert len(tasks) == 1
assert tasks[0]['text'] == "MyTask"
```

### Pattern 3: Invalid Input Test
```python
result = add_task("")  # Empty input
assert result is False  # Should reject
assert len(tasks) == 0  # No task added
```

### Pattern 4: State Change Test
```python
add_task("Test")
assert tasks[0]['done'] is False  # Initial state
toggle_task(0)
assert tasks[0]['done'] is True   # State changed
```

---

## ❓ WHEN TESTS FAIL

### If Integration Test Fails:
- Check if route exists in `app.py`
- Check if template renders correctly
- Check if form data is processed
- Check if redirect works

### If Unit Test Fails:
- Check function logic in `app.py`
- Check return values
- Check data structure changes
- Check validation rules

---

## 📌 KEY REMINDERS

1. **Integration tests = User view** (HTTP, HTML, workflows)
2. **Unit tests = Code view** (functions, logic, data)
3. **Both are needed** for complete coverage
4. **Timestamps matter**: `created_at` never changes, `completed_at` changes on toggle
5. **Validation is important**: Empty strings, duplicates, invalid indices
6. **Clear Pending** only removes pending tasks, keeps completed

---

## 🎓 FOR YOUR PRESENTATION/VIVA

**Question:** "What's the difference between black-box and white-box testing?"

**Answer:** 
- **Black-box (Integration):** Tests what users see and do. We send HTTP requests and check HTML responses. We don't look at internal code.
- **White-box (Unit):** Tests internal functions directly. We call Python functions and check return values and data structures. We know the code.

**Question:** "Why do you have both types?"

**Answer:**
- Integration tests catch UI and workflow issues
- Unit tests catch logic and edge case issues
- Together, they ensure both the surface and internals work correctly

**Question:** "How many tests do you have?"

**Answer:** 16 total - 9 integration tests (black-box) and 7 unit tests (white-box), covering all features including task management, timestamps, and validation.
