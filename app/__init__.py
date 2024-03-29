import logging
from os import environ

from flask import Flask
from flask_caching import Cache

logging.basicConfig(level=logging.INFO)

# PORT=3000
# HOST=0.0.0.0
# TODOS_CACHE_TYPE=redis
# REDIS_TODOS_HOST=redis
# REDIS_TODOS_PORT=6379
# REDIS_TODOS_DB=toods
# MONGO_TODOS_COLLECTION=todos
# MONGO_DATABASE=todosApp
# MONGO_URL=mongocurrent_app.cache.delete_memoize('cached_fetch')
# MONGO_PORT=27017
# MONGO_USERNAME=root
# MONGO_PASSWORD=root

APPLICATION_HOST = environ.get('HOST', '0.0.0.0')
APPLICATION_PORT = environ.get('PORT', 3000)
MONGO_TODOS_COLLECTION_NAME = environ.get('MONGO_TODOS_COLLECTION', 'todos')
MONGO_DATABASE = environ.get('MONGO_DATABASE', 'test')
MONGO_HOST = environ.get('MONGO_URL', 'localhost')
MONGO_PORT = int(environ.get('MONGO_PORT', 27017))
MONGO_USERNAME = environ.get('MONGO_USERNAME')
MONGO_PASSWORD = environ.get('MONGO_PASSWORD')
CACHE_TYPE = environ.get('TODOS_CACHE_TYPE')
REDIS_HOST = environ.get('REDIS_TODOS_HOST')
REDIS_PORT = environ.get('REDIS_TODOS_PORT')
REDIS_DB = environ.get('REDIS_TODOS_DB')


def create_app():
    app = Flask(__name__)

    app.cache = Cache(app, config={
        'CACHE_TYPE': CACHE_TYPE,
        'CACHE_REDIS_HOST': REDIS_HOST,
        'CACHE_REDIS_PORT': REDIS_PORT,
        'CACHE_REDIS_DB': REDIS_DB
    })
    app.cache.init_app(app)

    app.logger.info(f'Creating application on port {APPLICATION_PORT}...')

    app.port = APPLICATION_PORT
    app.host = APPLICATION_HOST

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

    from app.route import routes
    app.logger.info('Initializing routes...')
    app.register_blueprint(routes, url_prefix='/api')

    return app
