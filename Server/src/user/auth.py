from Server.src.exceptions import InvalidAPIException
from src.user import model
from src.utils import hash_password, create_jwt_token, check_password, decode_jwt_token
from src.constants import REFRESH_TOKEN_TYPE, ACCESS_TOKEN_TYPE

def register(email, name, password):
    """
    This function will hash the password, check if the email is unique or not and save the user to the 
    DB and will generate access and refresh token.

    Args:
        email (str): email of the new user
        name (str): name of the new user
        password (str): password of the new user
    """
    hashed_password = hash_password(password)
    model.create_user(name, email, hashed_password)
    user_dict = model.get_user_by_email(email)

    del user_dict['created_at']
    user_dict['token_type'] = ACCESS_TOKEN_TYPE
    access_token = create_jwt_token(user_dict)
    exp = user_dict['exp']
    del user_dict['exp']

    user_dict['token_type'] = REFRESH_TOKEN_TYPE
    refresh_token = create_jwt_token(user_dict, exp= 30*24*60*60)

    del user_dict['token_type']
    return {
        'user': user_dict,
        'exp': exp,
        'access_token': access_token,
        'refresh_token': refresh_token
    }

def login(email, password):
    """
    This function will check if the user with that email exists or not and will check the hashed password
    Args:
        email (str)
        password (str)
    
    Raises:
        InvalidAPIUsage: in case no user is found or if incorrect password
    Returns:
        dict: response dictonary
    """

    user_dict = model.get_password_from_email(email)

    if len(user_dict) == 0:
        raise InvalidAPIException(message='email or password is encorrect', payload={
            'status': False
        })
    
    hashed_password = user_dict[email]
    if check_password(hashed_password, password):
        user_dict = model.get_user_by_email(email)

        del user_dict['created_at']
        user_dict['token_type'] = ACCESS_TOKEN_TYPE
        access_token = create_jwt_token(user_dict)
        exp = user_dict['exp']
        del user_dict['exp']

        user_dict['token_type'] = REFRESH_TOKEN_TYPE
        refresh_token = create_jwt_token(user_dict, exp= 30*24*60*60)

        del user_dict['token_type']
        return {
            'user': user_dict,
            'exp': exp,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    raise InvalidAPIException(message='email or password is encorrect', payload={
            'status': False
        })

def token(refresh_token, user_id):
    """
    This function will handle the new access_token generation using the refresh token
    Args:
        token (str)
    Raises:
        InvalidAPIException
    Returns:
        dict: response dict with access token
    """

    user_dict = model.get_user_by_id(user_id)
    
    payload, err = decode_jwt_token(refresh_token)
    if err:
        raise InvalidAPIException(err, 402, {'status': False})

    if payload['token_type'] != REFRESH_TOKEN_TYPE:
        raise InvalidAPIException('invalid token type', 403, {'status': False})
    
    if payload['id'] != user_dict['id']:
        raise InvalidAPIException('invalid token type', 403, {'status': False})
    
    user_dict = payload
    user_dict['token_type'] = ACCESS_TOKEN_TYPE
    access_token = create_jwt_token(user_dict)

    exp = user_dict['exp']
    del user_dict['exp']

    user_dict['token_type'] = REFRESH_TOKEN_TYPE
    refresh_token = create_jwt_token(user_dict, exp= 30*24*60*60)
    del user_dict['token_type']

    return {
        'exp': exp,
        'access_token': access_token,
        'refresh_token': refresh_token
    }