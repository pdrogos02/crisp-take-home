def test_home_page_with_fixture(test_client):
    """
    Given a Flask application configured for testing
    when the '/' page is requested (GET)
    then check that the response is valid
    """
    response = test_client.get('/')

    assert response.status_code == 200
        
    assert b"Welcome to the Crisp Transformation App" not in response.data


def test_home_page_post_with_fixture(test_client):
    """
    Given a Flask application configured for testing
    when the '/' page is requested (POST)
    then check that the response is invalid via 405 returned status code
    """
    response = test_client.post('/')

    assert response.status_code == 405
        
    assert b"Welcome to the Crisp Transformation App" not in response.data

        