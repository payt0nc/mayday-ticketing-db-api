import time

from flask import Blueprint, g
from flask_restful import Api

from iris.endpoints.auth import Auth
from iris.endpoints.events import Events
from iris.endpoints.health import Health
from iris.endpoints.matching import Matching
from iris.endpoints.stats import Stats
from iris.endpoints.tickets import MyTickets, Ticket, Tickets

controllers = Blueprint('controllers', __name__)
api = Api(controllers)

MIMETYPE = 'application/json'


@controllers.before_request
def before_request():
    g.request_start_time = time.time()


api.add_resource(Health, '/health')
api.add_resource(Auth, '/auth')

# Ticketings
api.add_resource(MyTickets, '/myTickets')
api.add_resource(Ticket, '/ticket')
api.add_resource(Tickets, '/tickets')
api.add_resource(Matching, '/matching/<user_id>')

# Constants
api.add_resource(Stats, '/stats')
api.add_resource(Events, '/events')
