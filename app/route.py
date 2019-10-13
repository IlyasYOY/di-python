import logging

from flask import Blueprint, current_app, jsonify, request

routes = Blueprint('routes', __name__)
logger = logging.getLogger(__name__)


@routes.route('/todos', methods=['GET'])
def get_todos():
    todos = current_app.todos.fetch_all()
    return jsonify([x.to_dict() for x in todos])


@routes.route('/todos/<string:identity>', methods=['GET'])
def get_todo(identity: str):
    todo_fetched_by_id = current_app.todos.fetch_by_id(identity)
    return jsonify(todo_fetched_by_id.to_dict()), 200


@routes.route('/todos/<string:identity>', methods=['DELETE'])
def remove_todo(identity: str):
    try:
        was_removed = current_app.todos.remove_by_id(identity)
        return jsonify({'removed': was_removed}), 200
    except:
        return jsonify({'message': 'error removing'}), 500


@routes.route('/todos', methods=['POST'])
def create_todo():
    try:
        data = request.get_json()
        if isinstance(data, list):
            saved_todos = current_app.todos.save_all(data)
            return jsonify(saved_todos), 201
        else:
            saved_todo = current_app.todos.save(data)
            return jsonify(saved_todo), 201
    except ValueError:
        return jsonify({'message': 'error parsing body'}), 400
    except:
        return jsonify({'message': 'error saving todos'}), 500
