import sys
import pandas as pd, psycopg2 as psql
from Server.src.user.queries import get_email_and_password_query, get_user_by_id_query

from src.exceptions import InvalidAPIException
from src.connector import get_db_connection
from src.user.queries import get_insert_user_data_query, get_user_by_email_query

def create_user(name, email, password):
    '''
    This is the model function which will help us in creating a new user
    Args:
        name (str)
        email (str)
        password (str)
    
    Raises: 
        InvalidAPIException in case of integrity error
    '''
    conn = get_db_connection()
    query = get_insert_user_data_query()

    try:
        cursor = conn.cursor()
        cursor.execute(query, (name, email, password))
        conn.commit()
        return
    except psql.IntegrityError as ie:
        print(ie, file=sys.stderr)
        raise InvalidAPIException(message='User already exists')
    except Exception as e:
        print(e, file=sys.stderr)
        raise InvalidAPIException(message='Something went wrong', status_code=500)
    

def get_user_by_email(email):
    '''
    This is the model function which will help us getting an dict containing the data of a user
    Args:
        email (str) the email for which we want to search
    Returns:
        dict|None : the user dictonary
    '''
    conn = get_db_connection()
    query = get_user_by_email_query(email)

    try:
        data = pd.read_sql_query(query, conn)
        user_dict = dict()
        for index,data_obj in data.iterrows():
            user_dict[data_obj['email']] = data_obj.to_dict()
        return user_dict[email]
    except IndexError:
        raise InvalidAPIException(message='user doesnt exists', status_code=401)
    except Exception as e:
        raise InvalidAPIException(message='Something went wrong', status_code=500)

def get_password_from_email(email):
    '''
    This is the model function which will help us to fetch password for a user
    Args:
        email (str)
    Retruns:
        dict|None: dict mapped with user email to password
    '''

    conn = get_db_connection()
    query = get_email_and_password_query(email)

    try:
        data = pd.read_sql_query(query, conn)
        user_dict = dict(zip(data.email, data.password))
        return user_dict[email]
    except IndexError:
        raise InvalidAPIException(message='user doesnt exists', status_code=401)
    except Exception as e:
        print(e)
        raise InvalidAPIException('something went wrong', 500)
    
def get_user_by_id(user_id):
    '''
    This model function will fetch user by their ids
    Args:
        user_id (str|int)
    Returns:
        dict|None: dict mapped with user id to user_data
    '''
    conn = get_db_connection()
    query = get_user_by_id_query(user_id)

    try:
        data = pd.read_sql_query(query, conn)
        user_dict = dict()
        for index,data_obj in data.iterrows():
            user_dict[data_obj['id']] = data_obj.to_dict()
        return user_dict[user_id]
    except IndexError:
        raise InvalidAPIException(message='user doesnt exists', status_code=401)
    except Exception as e:
        raise InvalidAPIException(message='Something went wrong', status_code=500)
