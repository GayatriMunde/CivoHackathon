import json
def test_home(client):
    """
    GIVEN a flask application configured for testing
    WHEN we send request to '/' 
    THEN check it return status_code 200 and a message 'App successfully loaded'
    """

    response = client.get('/')
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data['status']
    assert response_data['data'] == 'App successfully loaded'
