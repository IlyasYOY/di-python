import json

from flask import Blueprint, current_app, jsonify

routes = Blueprint('routes', __name__)


@routes.route('/todos', methods=['GET'])
def get_todos():
    todos = current_app.todos.fetch_all()
    return jsonify([x.to_dict() for x in todos])


@routes.route('/')
def index():
    return jsonify({
        'Hello': 'World'
    })
