from flask import Blueprint, request, jsonify
from app import db
from sqlalchemy import desc

bp = Blueprint('tasks', __name__)

@bp.route('/test', methods=['POST'])
def index():
    return jsonify({'message': 'Welcome to the Task Management API'})
