import json
import time
import traceback

from flask import current_app, g, request
from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from iris import log_util

parser = RequestParser()
parser.add_argument('ticket_id', type=int, location='args')
parser.add_argument('user_id', type=int, location='args')

ticket_fields = dict(
    id=fields.Integer,
    user_id=fields.Integer,
    username=fields.String,
    category_id=fields.Integer,
    date=fields.Integer,
    price_id=fields.Integer,
    quantity=fields.Integer,
    section=fields.String,
    row=fields.String,
    status_id=fields.Integer,
    wish_date=fields.List(fields.Integer),
    wish_price_id=fields.List(fields.Integer),
    wish_quantity=fields.List(fields.Integer),
    remarks=fields.String
)


class MyTickets(Resource):

    def get(self):
        logger = current_app.config['app.logger']
        ticket_model = current_app.config['app.db.tickets']
        args = parser.parse_args()
        user_id = args['user_id']
        try:
            tickets = [x for x in ticket_model.get_tickets_by_user_id(user_id)]
            msg = log_util.get_log_msg(
                endpoint='myTickets',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request=user_id,
                response=tickets
            )
            logger.info(msg)
            return tickets
        except Exception:
            msg = log_util.get_log_msg(
                endpoint='myTickets',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request=user_id,
                response=traceback.format_exc()
            )
            logger.error(msg)
            return None

    @marshal_with(ticket_fields)
    def post(self):
        logger = current_app.config['app.logger']
        ticket_model = current_app.config['app.db.tickets']
        args = parser.parse_args()
        ticket_id = args['ticket_id']
        if ticket_id:
            try:
                ticket_model.update_ticket(ticket_id, request.get_json())
                result = ticket_model.get_ticket_by_ticket_id(ticket_id)
                msg = log_util.get_log_msg(
                    endpoint='updateTicket',
                    process_time=int((time.time() - g.request_start_time) * 1000),
                    request=args,
                    response=result
                )
                logger.info(msg)
                return result
            except Exception:
                msg = log_util.get_log_msg(
                    endpoint='updateTicket',
                    process_time=int((time.time() - g.request_start_time) * 1000),
                    request=args,
                    response=traceback.format_exc()
                )
                logger.error(msg)
        return None

    @marshal_with(ticket_fields)
    def put(self):
        logger = current_app.config['app.logger']
        ticket_model = current_app.config['app.db.tickets']
        args = parser.parse_args()
        try:
            del args['ticket_id']
            ticket = request.get_json()
            ticket_model.create_ticket(ticket)
            result = ticket_model.get_tickets_by_user_id(ticket.get('user_id')).__next__()
            msg = log_util.get_log_msg(
                endpoint='createTicket',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request=args,
                response=result
            )
            logger.info(msg)
            return result
        except Exception:
            msg = log_util.get_log_msg(
                endpoint='createTicket',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request=args,
                response=traceback.format_exc()
            )
            logger.error(msg)
            return None


class Ticket(Resource):
    # @app.route('/findTicketByTicketId/<ticket_id>', methods=['GET'])
    # @app.route('/findTicketByUserId/<user_id>', methods=['GET'])
    def get(self):
        logger = current_app.config['app.logger']
        ticket_model = current_app.config['app.db.tickets']
        args = parser.parse_args()
        ticket_id = args['ticket_id']
        user_id = args['user_id']
        if ticket_id:
            try:
                result = list(ticket_model.get_ticket_by_ticket_id(ticket_id))
                msg = log_util.get_log_msg(
                    endpoint='findTicketByTicketId',
                    process_time=int((time.time() - g.request_start_time) * 1000),
                    request=args,
                    response=result
                )
                logger.info(msg)
                return result
            except Exception:
                msg = log_util.get_log_msg(
                    endpoint='findTicketByTicketId',
                    process_time=int((time.time() - g.request_start_time) * 1000),
                    request=args,
                    response=traceback.format_exc()
                )
                logger.error(msg)
                return None
        if user_id:
            try:
                result = [x for x in ticket_model.get_tickets_by_user_id(user_id)]
                msg = log_util.get_log_msg(
                    endpoint='findTicketByUserId',
                    process_time=int((time.time() - g.request_start_time) * 1000),
                    request=args,
                    response=result
                )
                logger.info(msg)
                return result
            except Exception:
                msg = log_util.get_log_msg(
                    endpoint='findTicketByUserId',
                    process_time=int((time.time() - g.request_start_time) * 1000),
                    request=args,
                    response=traceback.format_exc()
                )
                logger.error(msg)
                return None
        return None


ticket_parser = RequestParser()
ticket_parser.add_argument('status_id', location=['args'], default=None)
ticket_parser.add_argument('category_id', location=['args'], default=None)
ticket_parser.add_argument('price_id', location=['args'], default=None)
ticket_parser.add_argument('date', location=['args'], default=None)
ticket_parser.add_argument('quantity', location=['args'], default=None)


class Tickets(Resource):
    # @app.route('/findTickets', methods=['POST'])

    def _concat_condition(self):
        args = ticket_parser.parse_args()
        return dict(
            status_id=args['status_id'],
            category_id=args['category_id'],
            price_id=args['price_id'],
            date=args['date'],
            quantity=args['quantity']
        )

    def get(self):
        logger = current_app.config['app.logger']
        ticket_model = current_app.config['app.db.tickets']
        conditions = self._concat_condition()
        try:
            result = [x for x in ticket_model.get_tickets_by_conditions(conditions)]
            msg = log_util.get_log_msg(
                endpoint='findTickets',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request=conditions,
                response=result
            )
            logger.info(msg)
            return result
        except Exception:
            msg = log_util.get_log_msg(
                endpoint='findTickets',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request=conditions,
                response=traceback.format_exc()
            )
            logger.error(msg)
            return None
