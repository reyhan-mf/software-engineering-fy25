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
    try:
        # Get query parameters
        category = request.args.get('category')
        priority = request.args.get('priority')
        deadline_from = request.args.get('deadline_from')
        deadline_to = request.args.get('deadline_to')
        sort_by = request.args.get('sort_by', 'created_at')
        order = request.args.get('order', 'desc')

        # Validate sort_by field exists
        if not hasattr(Task, sort_by):
            return jsonify({
                'message': f'Invalid sort field: {sort_by}. '
                'Available fields: title, category, priority, deadline, created_at'
            }), 400

        query = Task.query

        # Filtering
        if category:
            query = query.filter(Task.category == category)
        if priority:
            query = query.filter(Task.priority == priority)
        if deadline_from:
            try:
                from_dt = parse_datetime(deadline_from)
                query = query.filter(Task.deadline >= from_dt)
            except ValueError as e:
                return jsonify({'message': str(e)}), 400
        if deadline_to:
            try:
                to_dt = parse_datetime(deadline_to)
                query = query.filter(Task.deadline <= to_dt)
            except ValueError as e:
                return jsonify({'message': str(e)}), 400

        # Sorting
        sort_column = getattr(Task, sort_by)
        if order.lower() not in ['asc', 'desc']:
            return jsonify({
                'message': 'Invalid order value. Use "asc" or "desc"'
            }), 400
            
        query = query.order_by(desc(sort_column) if order.lower() == 'desc' else sort_column)

        tasks = query.all()
        if not tasks:
            return jsonify({
                'message': 'No tasks found matching the criteria',
                'data': []
            }), 200  # Return 200 with empty list instead of 404
            
        return jsonify({
            'message': 'Tasks retrieved successfully',
            'data': tasks_schema.dump(tasks)
        })

    except Exception as e:
        return jsonify({
            'message': 'An error occurred while processing your request',
            'error': str(e)
        }), 500
    
# Get by ID
@bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = db.session.get(Task, id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify(task_schema.dump(task))

@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = db.session.get(Task, id)
    data = request.get_json()

    if not task:
        return jsonify({'message': 'Task not found'}), 404

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

@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = db.session.get(Task, id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})