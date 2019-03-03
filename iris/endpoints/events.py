import time
import traceback

from flask import current_app, g
from flask_restful import Resource
from iris import log_util


class Events(Resource):

    def get(self):
        logger = current_app.config['app.logger']
        redis = current_app.config['app.config.redis']
        sp_event = current_app.config['app.db.events']

        try:
            events = redis.load('MAYDAY_SUPPORT_EVENT')
            if events:
                result = events
            else:
                result = sp_event.get_events()
                redis.save('MAYDAY_SUPPORT_EVENT', result)

            msg = log_util.get_log_msg(
                endpoint='getEvent',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request=None,
                response=result
            )
            logger.info(msg)
            return result

        except Exception:
            msg = log_util.get_log_msg(
                endpoint='getEvent',
                process_time=int((time.time() - g.request_start_time) * 1000),
                request=None,
                response=traceback.format_exc(),
            )
            logger.error(msg)
            return None
