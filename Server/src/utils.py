import sys
import bcrypt
import jwt
import datetime

from src.connector import get_env_value
CONFIG = get_env_value()

def hash_password(password):
    '''
    Args:
        password (str)
    Returns:
        str: hashed password
    '''
    password = password.encode('utf8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt).decode('utf8')

def check_password(hashed_password, password):
    '''
    Args:
        hashed_password (str)
        password (str)
    Returns:
        bool :true if password matches else false
    '''
    password = password.encode('utf8')
    hashed_password = hashed_password.encode('utf8')
    return bcrypt.checkpw(password, hashed_password)

def create_jwt_token(payload,exp = 1800):
    """
    Args:
        payload (dict): the payload which will be used to create the jwt token
        exp (int): the exp time in seconds
    Returns:
        str: the jwt token
    """
    
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=exp)
    return jwt.encode(payload, CONFIG['SECRET'], algorithm="HS256")

def decode_jwt_token(token):
    """
    Args:
        token (str)
    
    Returns:
        dict|None: the payload in case successful
        str|None: the error message
    """
    data = None
    err = None
    try:
        data = jwt.decode(token, CONFIG['SECRET'], algorithms=["HS256"])
    except jwt.InvalidTokenError :
        err = 'Invalid token'
    except jwt.ExpiredSignatureError:
        err = 'Token expired'
    except Exception as e:
        print(e, file=sys.stderr)
        err = 'Something went wrong'

    return data, err

