import time
import traceback

from flask import current_app, g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from iris import log_util

post_parser = RequestParser()
post_parser.add_argument('user_id', dest='user_id', type=int, required=True)
post_parser.add_argument('username', dest='username', type=str, required=True)
post_parser.add_argument('first_name', dest='first_name', type=str, required=True)
post_parser.add_argument('last_name', dest='last_name', type=str, required=True)


class Auth(Resource):

    def post(self):
        logger = current_app.config['app.logger']
        args = post_parser.parse_args(strict=True)
        logger.debug(args)
        try:
            users = current_app.config['app.db.users']
            result = users.get_auth(args)
        except Exception:
            result = traceback.format_exc()

        process_time = (int(time.time()) - g.request_start_time) * 1000
        msg = log_util.get_log_msg(
            endpoint='/auth',
            process_time=process_time,
            request=args,
            response=result
        )
        logger.info(msg)
        return result
