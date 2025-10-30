# CHANGELOG - Flask To-Do List Application

## Latest Update - Critical Indexing Bug Fix (v1.1)

### 🐛 BUG FIX: Task Indexing Issue
**Date:** 2025-10-30  
**Severity:** High - Critical functionality bug  
**Status:** ✅ FIXED

**Problem:**
- When marking tasks as complete after some tasks were already completed, the WRONG task would be toggled
- Example: If tasks A and B were complete, trying to mark task C complete would unmark task A instead
- Same issue affected delete operations - deleting wrong tasks

**Root Cause:**
- Template used filtered loops: `{% for task in tasks if not task['done'] %}`
- This created new indices for filtered items (0, 1, 2...)
- But the backend expected original indices from the full task list
- Mismatch between displayed index and actual index

**Solution:**
- Changed to full loop with conditional display inside:
  ```html
  {% for task in tasks %}
      {% if not task['done'] %}
          <!-- display task -->
      {% endif %}
  {% endfor %}
  ```
- Now `loop.index0` correctly reflects position in original list
- All operations (mark complete, delete) now target correct tasks

**Files Changed:**
- `templates/index.html` - Fixed both pending and completed task loops

**Impact:**
- ✅ Mark complete now works correctly
- ✅ Delete now removes correct task
- ✅ Multiple selection works accurately
- ✅ All task operations reliable

**Documentation:**
- See `BUGFIX_INDEXING.md` for detailed explanation
- See `MANUAL_TEST_GUIDE.md` for verification steps

---

## Previous Update - Clear Pending Functionality (v1.0)

### Changes Made:

#### 1. **Modified `clear_tasks()` Function** (`app.py`)
**Before:**
```python
def clear_tasks() -> None:
    tasks.clear()
```

**After:**
```python
def clear_tasks() -> None:
    """Clear only pending (not completed) tasks"""
    global tasks
    tasks[:] = [task for task in tasks if task['done']]
```

**Reason:** Now only removes pending tasks, preserving completed tasks.

---

#### 2. **Updated UI Button** (`templates/index.html`)
**Before:**
- Button text: "Clear All"
- Confirmation: "Clear all tasks?"

**After:**
- Button text: "Clear Pending"
- Confirmation: "Clear all pending tasks?"

**Reason:** Better user communication about what will be deleted.

---

#### 3. **Updated Test Cases** (`tests/test_app.py`)

**Test TC-INT-008: `test_clear_all_tasks()`**
**Before:**
```python
def test_clear_all_tasks(client):
    """TC-INT-008: Verify all tasks can be cleared"""
    client.post('/add', data={'task': 'Task1'}, follow_redirects=True)
    client.post('/add', data={'task': 'Task2'}, follow_redirects=True)
    client.post('/clear', follow_redirects=True)
    assert len(tasks) == 0
```

**After:**
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

---

**Test TC-UNIT-005: `test_clear_tasks_function_unit()`**
**Before:**
```python
def test_clear_tasks_function_unit():
    """TC-UNIT-005: Test clear_tasks function"""
    tasks.clear()
    add_task("One")
    add_task("Two")
    add_task("Three")
    assert len(tasks) == 3
    clear_tasks()
    assert len(tasks) == 0
```

**After:**
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

---

#### 4. **Updated Documentation**

**Files Updated:**
- `TEST_PLAN.md`
- `TEST_REPORT.md`
- `PROJECT_OVERVIEW.md`

**Changes:**
- "Clear all tasks" → "Clear pending tasks"
- "Clear All" → "Clear Pending"
- Updated test case descriptions
- Updated feature descriptions

---

### Why This Change Makes Sense:

1. **Better User Experience:** Completed tasks are archived and should be preserved
2. **More Practical:** Users typically want to clear pending tasks while keeping completed history
3. **Follows Best Practices:** Completed items serve as a record of accomplishment
4. **Test Coverage:** Tests now validate this important behavior

---

### Impact on Problem Statement Compliance:

✅ **Still Fully Compliant** - All requirements are met:
- Feature still tested (TC-INT-008, TC-UNIT-005)
- Both black-box and white-box testing maintained
- Documentation updated accordingly
- Test procedures remain valid

---

### How to Verify:

```powershell
# Run tests
python -m pytest tests/test_app.py::test_clear_all_tasks -v
python -m pytest tests/test_app.py::test_clear_tasks_function_unit -v

# Or run all tests
python -m pytest tests/test_app.py -v
```

**Expected Result:** All tests should pass, demonstrating that clear functionality only removes pending tasks.

---

### Manual Testing Steps:

1. Start the application: `python app.py`
2. Add 3 tasks: "Task A", "Task B", "Task C"
3. Mark "Task B" as complete (checkbox)
4. Click "Clear Pending" button
5. Verify: Only "Task B" remains in the Completed section
6. Verify: "Task A" and "Task C" are removed

---

## Summary

The "Clear Pending" functionality now:
- ✅ Only removes pending (incomplete) tasks
- ✅ Preserves completed tasks
- ✅ Has updated and comprehensive test coverage
- ✅ Maintains all problem statement requirements
- ✅ Provides better user experience
