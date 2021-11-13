import psycopg2
from flask import g
from dotenv import dotenv_values


CONFIG = dotenv_values(".env")

def get_db_connection():
    """Return a database connection.
    If a connection already exists in request context then that is 
    if it does not exist then a new database connection is created and 
    pushed into the flask `g` stack.
    A new connection is created for every request. Multiple connections
    are not created for a single request.
    The database connection should always be initiated 
    with this function, using `conn = get_db_connection()`.
    Using this function ensures that only one connection to database
    will be created for a request. If a connection has already been
    created in the request then the same connection will be returned 
    by the function
    Returns:
        psycopg2 connection: The connection object to postgres database
    """
    if 'db_connection' not in g:
        g.db_connection = psycopg2.connect(
            user = CONFIG['DB_USER'], 
            password = CONFIG['DB_PASSWORD'],
            host = CONFIG['DB_HOST'],
            port = CONFIG['DB_PORT'],
            database = CONFIG['DB_NAME']
        )
    return g.db_connection

def get_env_value(key):
    """
    Returns enviroment dictonary or a single value according to
    the value of key.
    If a env dict already exists in request context then that is 
    if it does not exists then a new dict is pushed onto the flask `g`
    stack.
    Args:
        key (str|None): the key to the enviromental value
    Returns:
        Any| dict: the value depends on the key
    """

    if 'app_data_env' not in g:
        g.app_data_env = CONFIG
    
    if key is None:
        return g.app_data_env
    else:
        return g.app_data_env.get(key)

def teardown_connections(Exception):
    """Close the connections established during request if they
    still exist in memory.
    This registered method will automatically be called by flask at the end 
    of every request hence it is good practice to close or delete
    idle connections to DB or other services that will no longer be used.
    Args:
        exception (Exception): (Optional) Exception to raise
    """
    db = g.pop('db_connection', None)

    if db is not None:
        db.close()