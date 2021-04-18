import json
import time

from flask import Flask, request

from rgate_app.requesthandler import requestHandler
from rgate_app.requeststats import requestStats

rgate_app = Flask(__name__)


@rgate_app.route("/stats")
def stats():
    out_put = dict(rgate_app.REQUEST_STATE)
    out_put.pop("requests_time")
    return json.dumps(out_put)


@rgate_app.before_request
def before_request():
    request.start_time = time.time()
    if not request.path == "/stats":
        return requestHandler().handle_request()


@rgate_app.after_request
def after_request(response):
    if not request.path == "/stats":
        requestStats(response).update_request_metadata()
    return response
