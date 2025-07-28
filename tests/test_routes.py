from datetime import datetime
import pytest
from app import create_app, db
from app.models import Task
from flask import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_index(client):
    response = client.post('/test')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Welcome to the Task Management API'

def test_create_task(client):
    data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'category': 'Work',
        'priority': 'High',
        'deadline': '2025-12-31 23:59:59'
    }
    response = client.post('/tasks', json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Task created successfully'
    assert response.get_json()['task']['title'] == 'Test Task'


def test_create_task_no_data(client):
    response = client.post('/tasks', json={})
    assert response.status_code == 404
    assert 'No input data provided' in response.get_json()['message']

def test_create_task_invalid_data(client):
    data = {'title': '', 'category': '', 'priority': '', 'deadline': 'invalid-date'}
    response = client.post('/tasks', json=data)
    assert response.status_code == 400
    assert '400 Bad Request' in response.get_json()['message']

def test_get_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 404
    assert 'No tasks found' in response.get_json()['message']

def test_get_tasks(client):
    data = {
        'title': 'Task1',
        'description': 'Desc',
        'category': 'Work',
        'priority': 'High',
        'deadline': '2025-12-31 23:59:59'
    }
    response_create = client.post('/tasks', json=data)
    assert response_create.status_code == 201

    response = client.get('/tasks')
    assert response.status_code == 200
    tasks = response.get_json()
    assert isinstance(tasks, list)
    assert any(task['title'] == 'Task1' for task in tasks)

def test_get_tasks_with_filters(client):
    # Add tasks
    t1 = Task(title='Task1', description='Desc', category='Work', priority='High', deadline=datetime(2025, 12, 31, 23, 59, 59))
    t2 = Task(title='Task2', description='Desc', category='Home', priority='Low', deadline=datetime(2025, 12, 31, 23, 59, 59))
    db.session.add_all([t1, t2])
    db.session.commit()
    response = client.get('/tasks?category=Work')
    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]['category'] == 'Work'


def test_get_task_by_id(client):
    task = Task(title='Task1', description='Desc', category='Work', priority='High', deadline=datetime(2025, 12, 31, 23, 59, 59))
    db.session.add(task)
    db.session.commit()
    response = client.get(f'/tasks/{task.id}')
    assert response.status_code == 200
    assert response.get_json()['title'] == 'Task1'


def test_update_task(client):
    task = Task(title='Task1', description='Desc', category='Work', priority='High', deadline=datetime(2025, 12, 31, 23, 59, 59))
    db.session.add(task)
    db.session.commit()
    update_data = {'title': 'Updated Task', 'priority': 'Low'}
    response = client.put(f'/tasks/{task.id}', json=update_data)
    assert response.status_code == 200
    assert response.get_json()['task']['title'] == 'Updated Task'
    assert response.get_json()['task']['priority'] == 'Low'

def test_update_task_invalid(client):
    task = Task(title='Task1', description='Desc', category='Work', priority='High', deadline=datetime(2025, 12, 31, 23, 59, 59))
    db.session.add(task)
    db.session.commit()
    response = client.put(f'/tasks/{task.id}', json={'deadline': 'invalid-date'})
    assert response.status_code == 400
    assert 'Invalid input' in response.get_json()['message']

def test_update_task_no_data(client):
    task = Task(title='Task1', description='Desc', category='Work', priority='High', deadline=datetime(2025, 12, 31, 23, 59, 59))
    db.session.add(task)
    db.session.commit()
    response = client.put(f'/tasks/{task.id}', json={})
    assert response.status_code == 400
    assert 'No input data provided' in response.get_json()['message']


def test_delete_task(client):
    task = Task(title='Task1', description='Desc', category='Work', priority='High', deadline=datetime(2025, 12, 31, 23, 59, 59), created_at=datetime(2025, 12, 31, 23, 59, 59))
    db.session.add(task)
    db.session.commit()
    response = client.delete(f'/tasks/{task.id}')
    assert response.status_code == 200
    assert 'Task deleted successfully' in response.get_json()['message']


