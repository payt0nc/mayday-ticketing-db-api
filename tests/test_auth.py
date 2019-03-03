import json

import pytest

import flask_restful
from flask import url_for

PROFILE = dict(
    user_id=123456789,
    username='test',
    first_name='test',
    last_name='test'
)


@pytest.mark.usefixtures("app")
class TestApp:

    @pytest.fixture(autouse=True)
    def before_after_all(self, app):
        users = app.config['app.db.users']
        users.metadata.drop_all()
        users.metadata.create_all()

    def test_auth(self, app):
        with app.app_context():
            url = url_for('controllers.auth')
        res = app.test_client().post(
            url,
            data=json.dumps(PROFILE, ensure_ascii=False),
            content_type='application/json'
        )

        assert 200 == res.status_code
        assert res.json['is_banned'] is False
        assert res.json['is_admin'] is False
