import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, tasks, add_task, edit_task, toggle_task, delete_task, clear_tasks

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        tasks.clear()
        yield client

# ========================================
# BLACK-BOX INTEGRATION TESTS
# Testing application behavior from user perspective
# ========================================

def test_index_loads(client):
    """TC-INT-001: Verify home page loads successfully"""
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert 'To-Do List' in text
    assert 'Pending Tasks' in text
    assert 'Completed Tasks' in text

def test_add_task_integration_shows_task_and_timestamp(client):
    """TC-INT-002: Verify task is added with creation timestamp"""
    client.post('/add', data={'task': 'Integration Task'}, follow_redirects=True)
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert 'Integration Task' in text
    assert 'Created:' in text
    # Verify timestamp format
    idx = text.find('Created:')
    assert idx != -1

def test_prevent_empty_task_integration(client):
    """TC-INT-003: Verify empty tasks are not added"""
    client.post('/add', data={'task': ''}, follow_redirects=True)
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert 'No pending tasks.' in text or len(tasks) == 0

def test_prevent_duplicate_tasks_integration(client):
    """TC-INT-004: Verify duplicate tasks are prevented"""
    client.post('/add', data={'task': 'Dup Task'}, follow_redirects=True)
    client.post('/add', data={'task': 'Dup Task'}, follow_redirects=True)
    assert len(tasks) == 1

def test_toggle_task_integration_marks_done(client):
    """TC-INT-005: Verify task can be marked as complete"""
    client.post('/add', data={'task': 'ToggleMe'}, follow_redirects=True)
    client.get('/toggle/0', follow_redirects=True)
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert 'task-text done' in text
    assert 'Completed:' in text

def test_delete_task_integration_removes_task(client):
    """TC-INT-006: Verify task can be deleted"""
    client.post('/add', data={'task': 'ToDelete'}, follow_redirects=True)
    client.get('/delete/0', follow_redirects=True)
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert 'ToDelete' not in text

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

def test_task_count_display(client):
    """TC-INT-009: Verify task count is displayed correctly"""
    client.post('/add', data={'task': 'Task1'}, follow_redirects=True)
    client.post('/add', data={'task': 'Task2'}, follow_redirects=True)
    resp = client.get('/')
    text = resp.get_data(as_text=True)
    assert 'Total: 2' in text

# ========================================
# WHITE-BOX UNIT TESTS
# Testing internal functions and logic
# ========================================

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

def test_timestamp_persistence_unit():
    """TC-UNIT-006: Test that created_at persists after toggle"""
    tasks.clear()
    add_task("Persist Test")
    original_created = tasks[0]['created_at']
    toggle_task(0)
    assert tasks[0]['created_at'] == original_created
    toggle_task(0)
    assert tasks[0]['created_at'] == original_created

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
