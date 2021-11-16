import re
from sre_constants import error
from src.exceptions import InvalidAPIException
from src.constants import EMAIL_REGULAR_EXPRESSION


def sanitize_input(data, error_dict, endpoint):
    '''
    This function is a mapper function, which maps endpoint to the corresponding
    sanitizer function, in case some error occurs them it will raise InvalidApiException

    Args:
        data (dict): Request data
        error_dict (dict): Error dictionary that will be 
            populated with errors if any
        endpoint (str): The endpoint for which sanitization
            will happen
    
    Raises:
        InvalidAPIException: if any data is missing or in wrong format
    
    Returns:
        data: Validated and cleaned request data
    '''
    if not isinstance(data, dict):
        data = {}
    params = list(data.keys())

    if endpoint == 'register_user':
        data, error_dict = sanitize_register_user(data, params, error_dict)
    elif endpoint == 'login_user':
        data, error_dict = sanitize_login_user(data, params, error_dict)
    elif endpoint == 'token':
        data, error_dict = sanitize_refresh_token(data, params, error_dict)
    
    if error_dict:
        error_dict['status'] = False
        raise InvalidAPIException(message='Validation error', status_code=200, payload=error_dict)

    return data

def sanitize_register_user(data, params,errors):
    
    if 'email' not in params:
        errors['email'] = 'Email is required'
    
    if 'name' not in params:
        errors['name'] = 'Name is required'
    else:
        data['name'] = data['name'].strip()
        if len(data['name']) == 0:
            errors['name'] = 'Name is required'
    
    if 'password' not in params:
        errors['password'] = 'Password is required'
    elif len(data['password']) < 6:
        errors['password'] = 'Minimum length of the password must be more than 6 characters'

    return data, errors

def sanitize_login_user(data, params,errors):
    
    if 'email' not in params:
        errors['email'] = 'Email is required'
    
    if 'password' not in params:
        errors['password'] = 'Password is required'

    return data, errors

def sanitize_refresh_token(data, params, errors):

    if 'refresh_token' not in params:
        errors['refresh_token'] = 'refresh token is required'
    
    if 'user_id' not in params:
        errors['user_id'] = 'user_id is required'

    return data, errors
    