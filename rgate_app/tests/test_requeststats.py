import time
from unittest import TestCase

import flask

from rgate_app.api import rgate_app
from rgate_app.requeststats import requestStats


class requestStatsTest(TestCase):
    def setUp(self):
        self.app_context = rgate_app.app_context()
        self.app_context.push()

        REQUEST_STATE = {
            'request_count': {
                'success': 0,
                'error': 0
            },
            'latency_ms': {
                'average': 0,
                'p95': 0,
                'p99': 0
            },
            'requests_time': []
        }
        rgate_app.REQUEST_STATE = REQUEST_STATE

    def tearDown(self):
        self.app_context.pop()

    def test_update_request_time_in_ms(self):
        with rgate_app.test_request_context('/'):
            flask.request.start_time = time.time()
            self.assertEqual(rgate_app.REQUEST_STATE['requests_time'], [])
            requestStats(None).update_request_time_in_ms()
            self.assertNotEqual(rgate_app.REQUEST_STATE['requests_time'], [])
            self.assertEqual(len(rgate_app.REQUEST_STATE['requests_time']), 1)
            requestStats(None).update_request_time_in_ms()
            self.assertEqual(len(rgate_app.REQUEST_STATE['requests_time']), 2)

    def test_update_latency_info(self):
        with rgate_app.test_request_context('/'):
            flask.request.start_time = time.time()
            rs = requestStats(None)
            rs.update_request_time_in_ms()
            self.assertEqual(rgate_app.REQUEST_STATE['latency_ms']['average'], 0)
            self.assertEqual(rgate_app.REQUEST_STATE['latency_ms']['p95'], 0)
            self.assertEqual(rgate_app.REQUEST_STATE['latency_ms']['p99'], 0)
            rs.update_latency_info()
            self.assertTrue(rgate_app.REQUEST_STATE['latency_ms']['average'] > 0)
            self.assertTrue(rgate_app.REQUEST_STATE['latency_ms']['p95'] > 0)
            self.assertTrue(rgate_app.REQUEST_STATE['latency_ms']['p99'] >  0)
