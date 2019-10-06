import json

from flask import Blueprint, current_app

routes = Blueprint('routes', __name__)


@routes.route('/todos', methods=['GET'])
def get_todos():
    todos = current_app.todos.fetch_all()
    return json.dumps(x.to_dict() for x in todos), 200
