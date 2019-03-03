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
        ticket_model.create_ticket(TICKET)

    def test_get_ticket_by_conditions(self, app):
        # search by status
        with app.app_context():
            url = url_for('controllers.tickets', status_id=1)
        with app.test_client() as client:
            res = client.get(url, content_type='application/json')
            assert res.status_code == 200
            assert len(res.json) == 1
            ticket = res.json[0]
            assert ticket['status_id'] == 1

        # search by category_id
        with app.app_context():
            url = url_for('controllers.tickets', category_id=1)
        with app.test_client() as client:
            res = client.get(url, content_type='application/json')
            assert res.status_code == 200
            assert len(res.json) == 1
            ticket = res.json[0]
            assert ticket['category_id'] == 1

        # search by price_id
        with app.app_context():
            url = url_for('controllers.tickets', price_id=1)
        with app.test_client() as client:
            res = client.get(url, content_type='application/json')
            assert res.status_code == 200
            assert len(res.json) == 1
            ticket = res.json[0]
            assert ticket['price_id'] == 1

        # search by date
        with app.app_context():
            url = url_for('controllers.tickets', date=501)
        with app.test_client() as client:
            res = client.get(url, content_type='application/json')
            assert res.status_code == 200
            assert len(res.json) == 1
            ticket = res.json[0]
            assert ticket['date'] == 501

        with app.app_context():
            url = url_for('controllers.tickets', date=[501, 502])
        with app.test_client() as client:
            res = client.get(url, content_type='application/json')
            assert res.status_code == 200
            assert len(res.json) == 1
            ticket = res.json[0]
            assert ticket['date'] == 501

        # search by quantity
        with app.app_context():
            url = url_for('controllers.tickets', quantity=1)
        with app.test_client() as client:
            res = client.get(url, content_type='application/json')
            assert res.status_code == 200
            assert len(res.json) == 1
            ticket = res.json[0]
            assert ticket['quantity'] == 1

        # search by max conditions
        with app.app_context():
            url = url_for('controllers.tickets', price_id=1, category_id=1, status_id=1, date=501, quantity=1)
        with app.test_client() as client:
            res = client.get(url, content_type='application/json')
            assert res.status_code == 200
            assert len(res.json) == 1
            ticket = res.json[0]
            assert ticket['price_id'] == 1
            assert ticket['category_id'] == 1
            assert ticket['status_id'] == 1
            assert ticket['date'] == 501
            assert ticket['quantity'] == 1
            assert ticket['quantity'] == 1
