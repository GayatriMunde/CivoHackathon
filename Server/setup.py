import os
from pathlib import Path
 
cwd = Path.cwd()
DOTENV = os.path.join(cwd, '.env')

def get_db_details():
    """
        Takes all the db details from user
        Args:
        
        Returns:
            dict: holding database cred
    """
    print('-----Database settings (postgres)------')
    db_name = input('Database name: ').strip()
    db_user = input('Database username: ').strip()
    db_host = input('Database host: ').strip()
    db_port = input('Database port: ').strip()
    db_password = input('Database password: ')

    return {
        'DB_NAME': db_name,
        'DB_USER': db_user,
        'DB_HOST': db_host ,
        'DB_PORT': db_port,
        'DB_PASSWORD': db_password
    }

def create_dotenv(data):
    '''
    This function will take all the environmental variables and create a dotenv from that
    Args:
        data (dict): will contain all the environment variables
    '''

    with open(DOTENV, 'a') as dotenv:
        for key in data:
            line = f'{key}={data[key]}\n'
            dotenv.write(line)

def generate_secret_key():
    import secrets
    return secrets.token_urlsafe(64)


def get_env():
    """
    Setting up Environment
    Returns:
        dict: containing the port and env
    """

    print("-------Environmental settings---------")
    env = dict()
    env['SECRET'] = generate_secret_key()
    if os.environ.get('ENV') is not None:
        env['ENV'] = 'prod'
    else:
        env['ENV'] = 'dev'
    
    return env



if __name__ == '__main__':
    # TODO: once database is finalised will be adding sqldump option so that on production tables can automatically get created (will be optional)
    # TODO: once all the tests are ready we will run tests on the sample data that will be present in the sqldump and then truncate all the table (will be optional)
    if os.path.exists(DOTENV):
        print('Set up is already completed.')
        exit(0)
    try:
        env_variables = dict()

        env_variables.update(get_db_details())
        env_variables.update(get_env())

        env_variables.update(os.environ)
        create_dotenv(env_variables)
    except KeyboardInterrupt:
        
        if os.path.exists(DOTENV):
            os.unlink(DOTENV)
        print('Exiting...')
