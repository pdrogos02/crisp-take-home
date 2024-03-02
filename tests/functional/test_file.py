import pytest
from flask import session, g

def test_index(client):
    response = client.get('/')
    assert b"Welcome to the Crisp Transformation App" in response.data