import logging
from os import environ

from flask import Flask

logging.basicConfig(level=logging.INFO)

APPLICATION_PORT = environ.get('PORT', 3000)
MONGO_TODOS_COLLECTION_NAME = environ.get('MONGO_TODOS_COLLECTION', 'todos')
MONGO_DATABASE = environ.get('MONGO_DATABASE', 'test')
MONGO_HOST = environ.get('MONGO_URL', 'localhost')
MONGO_PORT = int(environ.get('MONGO_PORT', 27017))
MONGO_USERNAME = environ.get('MONGO_USERNAME')
MONGO_PASSWORD = environ.get('MONGO_PASSWORD')


def create_app():
    app = Flask(__name__)

    app.logger.info(f'Creating application on port {APPLICATION_PORT}...')

    app.port = APPLICATION_PORT

    init_database(app)

    init_routes(app)

    return app


def init_routes(app):
    from app.route import routes
    app.logger.info('Initializing routes...')
    app.register_blueprint(routes)


def init_database(app):
    app.logger.info(
        f'Initializing Mongo host: {MONGO_HOST}, port: {MONGO_PORT}, user: {MONGO_USERNAME}, pass: {MONGO_PASSWORD}, database: {MONGO_DATABASE}')

    from pymongo import MongoClient
    client = MongoClient(host=MONGO_HOST,
                         port=MONGO_PORT,
                         username=MONGO_USERNAME,
                         password=MONGO_PASSWORD)

    from app.database import Todos
    app.todos = Todos(database=MONGO_DATABASE, collection=MONGO_TODOS_COLLECTION_NAME, mongo_client=client)
    app.logger.info(f'Initializing todos repo {app.todos}...')
