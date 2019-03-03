import json
import time
import traceback

from flask import current_app, g, request
from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from iris import log_util


class Stats(Resource):

    def get(self):
        logger = current_app.config['app.logger']
        redis = current_app.config['app.config.redis']
        ticket_model = current_app.config['app.db.tickets']
        try:
            stats = redis.load('mayday_ticket_stats')
            if stats:
                result = stats
            else:
                result = ticket_model.get_ticket_stats()
                redis.save('TICKET_STATS', result)
            msg = log_util.get_log_msg(
                endpoint='ticketStats',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request='',
                response=result
            )
            logger.info(msg)
            return result
        except Exception:
            msg = log_util.get_log_msg(
                endpoint='ticketStats',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request='',
                response=result
            )
            logger.error(msg)
            return None
