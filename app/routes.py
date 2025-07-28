from flask import Blueprint, request, jsonify
from app import db
from app.models import Task
from app.schemas import task_schema
from sqlalchemy import desc

from app.utils import parse_datetime

bp = Blueprint('tasks', __name__)

@bp.route('/test', methods=['POST'])
def index():
    return jsonify({'message': 'Welcome to the Task Management API'})

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    errors = task_schema.validate(data)
    if errors:
        return jsonify({'message': 'Invalid input', 'errors': errors}), 400

    task = Task(
        title=data['title'],
        description=data.get('description'),
        category=data['category'],
        priority=data['priority'],
        deadline=parse_datetime(data['deadline'])
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        'message': 'Task created successfully',
        'task': task_schema.dump(task)
    }), 201