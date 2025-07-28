from flask import Blueprint, request, jsonify
from app import db
from app.models import Task
from app.schemas import task_schema, tasks_schema
from sqlalchemy import desc

from app.utils import parse_datetime

bp = Blueprint('tasks', __name__)

@bp.route('/test', methods=['POST'])
def index():
    return jsonify({'message': 'Welcome to the Task Management API'})

# Insert tasks to database
@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 404
    
    errors = task_schema.validate(data)
    if errors:
        return jsonify({'message': '400 Bad Request', 'errors': errors}), 400

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

# Get with filter
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    # Get query parameters
    category = request.args.get('category')
    priority = request.args.get('priority')
    deadline_from = request.args.get('deadline_from')
    deadline_to = request.args.get('deadline_to')
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')

    query = Task.query

    # Filtering
    if category:
        query = query.filter(Task.category == category)
    if priority:
        query = query.filter(Task.priority == priority)
    if deadline_from:
        from_dt = parse_datetime(deadline_from)
        query = query.filter(Task.deadline >= from_dt)
    if deadline_to:
        to_dt = parse_datetime(deadline_to)
        query = query.filter(Task.deadline <= to_dt)

    sort_column = getattr(Task, sort_by, Task.created_at)
    if order == 'desc':
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(sort_column)

    # Category and Priority: http://127.0.0.1:5000/tasks?category=Work&priority=High
    # Deadline: http://127.0.0.1:5000/tasks?deadline_from=2023-01-01&deadline_to=2023-12-31
    # Sorting Ascending: http://127.0.0.1:5000/tasks?sort_by=priority&order=asc
    # Sorting Descending: http://127.0.0.1:5000/tasks?sort_by=priority&order=desc

    tasks = query.all()
    if not tasks:
        return jsonify({'message': 'No tasks found'}), 404
    return jsonify(tasks_schema.dump(tasks))

# Get by ID
@bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task_schema.dump(task))

@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    errors = task_schema.validate(data, partial=True)
    if errors:
        print("Validation errors:", errors)  # Debug print
        return jsonify({'message': 'Invalid input', 'errors': errors}), 400

    allowed_fields = ['title', 'description', 'category', 'priority', 'deadline']
    for field in allowed_fields:
        if field in data:
            if field == 'deadline':
                setattr(task, field, parse_datetime(data[field]))
            else:
                setattr(task, field, data[field])

    db.session.commit()

    return jsonify({
        'message': 'Task updated successfully',
        'task': task_schema.dump(task)
    })