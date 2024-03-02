import pytest
from crisp_app.app import create_app


@pytest.fixture(scope='module')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    app = create_app()

    app.config.from_object('crisp_app.flask_config.TestingConfig')

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!