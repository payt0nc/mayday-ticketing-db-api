import json
import pytest
from flask import url_for


@pytest.mark.usefixtures("app")
class TestApp:

    def test_health(self, app):
        # insert test data

        with app.app_context():
            url = url_for('controllers.health')

        # test match passwd
        res = app.test_client().get(url, content_type='application/json')
        result = json.loads(res.data, encoding='UTF-8')
        assert res.status_code == 200
        assert result['info'] == 'OK'
