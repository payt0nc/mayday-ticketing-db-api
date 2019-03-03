import time
import traceback

from flask import current_app, g
from flask_restful import Resource
from iris import log_util


class Matching(Resource):

    def get(self, user_id):
        logger = current_app.config['app.logger']
        ticket_model = current_app.config['app.db.tickets']
        try:
            result = [x for x in ticket_model.get_matched_wish_tickets(user_id)]
            msg = log_util.get_log_msg(
                endpoint='matchingMyTickets',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request='',
                response=result
            )
            logger.info(msg)
            return result
        except Exception:
            msg = log_util.get_log_msg(
                endpoint='matchingMyTickets',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request='',
                response=traceback.format_exc()
            )
            logger.error(msg)
            return None
