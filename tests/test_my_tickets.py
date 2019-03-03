import json

import pytest

from flask import url_for

TICKET = dict(
    category_id=1,
    date=501,
    price_id=1,
    quantity=1,
    section='BROWN',
    row='46',
    status_id=1,
    wish_date=[502, 501],
    wish_price_id=[1],
    wish_quantity=[1],
    remarks='',
    user_id=123456789,
    username='test'
)


UPDATED_TICKET = dict(
    category_id=1,
    date=501,
    price_id=1,
    quantity=1,
    section='BROWN',
    row='46',
    status_id=2,
    wish_date=[502, 501],
    wish_price_id=[1],
    wish_quantity=[1],
    remarks='',
    user_id=123456789,
    username='test'
)


@pytest.mark.usefixtures("app")
class TestApp:

    @pytest.fixture(autouse=True)
    def before_after_all(self, app):
        ticket_model = app.config['app.db.tickets']
        ticket_model.metadata.drop_all()
        ticket_model.metadata.create_all()

    def test_create_ticket(self, app):
        with app.app_context():
            url = url_for('controllers.mytickets')

        with app.test_client() as c:
            res = c.put(
                url,
                data=json.dumps(TICKET, ensure_ascii=False, sort_keys=True),
                content_type='application/json'
            )
            result = res.json

            assert 200 == res.status_code
            assert 'application/json' == res.mimetype
            del result['id']
            assert json.dumps(result, sort_keys=True) == json.dumps(TICKET, sort_keys=True)

    def test_get_my_ticket(self, app):
        # Check My Ticket
        with app.app_context():
            url = url_for('controllers.mytickets', user_id=123456789)

        with app.test_client() as c:
            c.put(
                url,
                data=json.dumps(TICKET, ensure_ascii=False, sort_keys=True),
                content_type='application/json'
            )
            res = c.get(url, content_type='application/json')
            result = res.json[0]
            assert 200 == res.status_code
            assert 'application/json' == res.mimetype
            del result['id']
            del result['updated_at']
            assert json.dumps(result, sort_keys=True) == json.dumps(TICKET, sort_keys=True)

    def test_update_my_ticket(self, app):
        # Check My Ticket
        with app.app_context():
            url = url_for('controllers.mytickets')

        with app.test_client() as c:
            c.put(
                url,
                data=json.dumps(TICKET, ensure_ascii=False, sort_keys=True),
                content_type='application/json'
            )
            res = c.post(
                url_for('controllers.mytickets', ticket_id=1),
                data=json.dumps(UPDATED_TICKET, ensure_ascii=False, sort_keys=True),
                content_type='application/json'
            )
            result = res.json
            assert 200 == res.status_code
            assert 'application/json' == res.mimetype
            assert result['status_id'] == UPDATED_TICKET['status_id']
