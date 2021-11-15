import os
from flask import Flask, jsonify

from src.connector import teardown_connections
from src.constants import BASE_PREFIX
from src.exceptions import InvalidAPIException
def create_app(config=None):
    '''
    This is the driver function which will allow all the blueprints and add connectors and middlewares
    Args:
        config (dict|None):  the data which is will be added to config, this will be used for testing and many things
    Returns:
        Flask: application instance
    '''
    app = Flask(__name__, instance_relative_config=True)

    #in case of testing config will be provided so we will be importing the env directly from this
    if config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(config)
    

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    #this will allow us to raise InvalidAPIException and flask will handle it automatically
    @app.errorhandler(InvalidAPIException)
    def invalid_exception_handler(e):
        return jsonify(e.to_dict()), e.status_code
    
    # this will be called after every request has been handled
    app.teardown_appcontext(teardown_connections)

    @app.route('/')
    def home():
        return {
            'status': True,
            'data': 'App successfully loaded'
        }
    # importing the blueprints
    from src.user.route import User

    app.register_blueprint(User, url_prefix=f'{BASE_PREFIX}/user')
    
    return app