import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, tasks  # <-- import tasks

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset tasks before each test
        tasks.clear()
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'To-Do List' in response.data

def test_add_task(client):
    response = client.post('/add', data={'task': 'Test Task'}, follow_redirects=True)
    assert b'Test Task' in response.data

def test_delete_task(client):
    client.post('/add', data={'task': 'Task to Delete'}, follow_redirects=True)
    response = client.get('/delete/0', follow_redirects=True)
    assert b'Task to Delete' not in response.data