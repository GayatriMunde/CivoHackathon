def get_all_users_query(order_by='created_at'):
    return f'''
    SELECT id, name,email, created_at, propic_url
    FROM users
    ORDER BY {order_by}
    '''

def get_user_with_attribute_query(attr_dict):
    q= f'''
    SELECT id, name,email, created_at, propic_url
    FROM users
    WHERE TRUE  
    '''
    attr = ' AND '.join([f"{key} = '{attr_dict[key]}'" for key in attr_dict])
    ' AND '.join([q, attr])

    return q

def get_user_by_email_query(email):
    return f'''
    SELECT id, name,email, created_at, propic_url
    FROM users
    WHERE email='{email}'
    LIMIT 1
    '''

def get_user_by_id_query(id):
    return f'''
    SELECT id, name,email, created_at, propic_url
    FROM users
    WHERE id='{id}'
    LIMIT 1
    '''

def get_insert_user_data_query():
    return f'''
    INSERT INTO users (name, email, password)
    VALUES (%s, %s, %s)
    '''

def get_insert_user_data_in_bulk_query(n):
    q = f'''
    INSERT INTO users (name, email, password)
    VALUES
    '''
    l = ','.join(['(%s, %s, %s)' for _ in range(n)])
    q = ' '.join([q, l])
    return q

def update_user_data_query(list_of_colums, id):
    q = f'''
    UPDATE users
    SET 
    '''
    l = ','.join([f'{key} = %s' for key in list_of_colums])
    q = ' '.join([q, l, f'WHERE id={id}'])

    return update_user_data_query

def get_email_and_password_query(email):
    return f'''
    SELECT email, password
    FROM users
    WHERE email='{email}'
    LIMIT 1
    '''
