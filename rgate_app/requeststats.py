import time

from flask import request
from flask import current_app as rgate_app


class requestStats:
    def __init__(self, response):
        self.request = request
        self.response = response
        self.request_state = rgate_app.REQUEST_STATE

    def update_request_metadata(self):
        self.update_request_time_in_ms()
        self.update_response_request_count()
        self.update_latency_info()

    def update_request_time_in_ms(self):
        request_time = (time.time() - self.request.start_time) * 1000
        self.request_state['requests_time'].append(request_time)

    def update_latency_info(self):
        total_request = len(self.request_state['requests_time'])
        average_latency = sum(self.request_state['requests_time'])/total_request
        self.request_state['latency_ms']['average'] = average_latency
        percentile_95 = (round(0.95 * total_request) - 1)
        percentile_99 = (round(0.99 * total_request) - 1)
        sorted_letency_time = sorted(self.request_state['requests_time'])
        self.request_state['latency_ms']['p95'] = sorted_letency_time[percentile_95]
        self.request_state['latency_ms']['p99'] = sorted_letency_time[percentile_99]

    def update_response_request_count(self):
        if 199 < self.response.status_code < 400:
            self.request_state['request_count']['success'] += 1
        elif self.response.status_code > 399:
            self.request_state['request_count']['error'] += 1
