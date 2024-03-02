import os, pytest

from crisp_app import create_app

@pytest.fixture
def app():
    app = create_app()

    app.config.from_object("config.TestingConfig")

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()