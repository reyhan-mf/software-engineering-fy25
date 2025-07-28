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
