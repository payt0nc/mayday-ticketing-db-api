import pytest

from iris import app as test_app


@pytest.fixture
def app():
    test_app.config['SERVER_NAME'] = 'localhost'
    return test_app
