from flask import Blueprint, request

from src.connector import get_env_value
from src.sanitize import sanitize_input
from src.user.auth import register, login, token
User = Blueprint('user', __name__)

@User.route('/register', methods=['POST'])
def register_user():
    unsafe_data, errors = request.get_json(), dict()

    response_data = sanitize_input(unsafe_data, errors, 'register_user')
    email = response_data['email']
    name = response_data['name']
    password = response_data['password']
    
    data = register(email, name, password)

    return {
        'status': True,
        'data': data
    }

@User.route('/login', methods=['POST'])
def login_user():
    unsafe_data, errors = request.get_json(), dict()

    response_data = sanitize_input(unsafe_data, errors, 'login_user')
    email = response_data['email']
    password = response_data['password']
    
    data = login(email, password)

    return {
        'status': True,
        'data': data
    }

@User.route('/token', methods=['POST'])
def generate_token():
    unsafe_data, errors = request.get_json(), dict()
    response_data = sanitize_input(unsafe_data, errors, 'token')

    refresh_token = response_data['refresh_token']
    user_id = response_data['user_id']

    data = token(refresh_token, user_id)

    return {
        'status': True,
        'data': data
    }