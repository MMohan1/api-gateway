from unittest import mock
from unittest import TestCase

from rgate_app.api import rgate_app
from rgate_app.requesthandler import requestHandler
from rgate_app.dockermanager import dockerManager
from rgate_app.requestwrapper import requestsWrapper


class requestHandlerTest(TestCase):
    def setUp(self):
        self.app_context = rgate_app.app_context()
        self.app_context.push()
        self.rgate_config = {'routes': [{'path_prefix': '/api/payment', 'backend': 'payment'}, {'path_prefix': '/api/orders', 'backend': 'orders'}], 'default_response': {'body': 'This is not reachable', 'status_code': 403}, 'backends': [{'name': 'payment', 'match_labels': ['app_name=payment', 'env=production']}, {'name': 'orders', 'match_labels': ['app_name=orders', 'env=production']}]}
        rgate_app.config['RGATE_CONFIG'] = self.rgate_config
        self.safe_request = requestsWrapper.safe_request
        mockrequest = requestsWrapper
        mockrequest.safe_request = mock.Mock(return_value=('Good', 200))

    def tearDown(self):
        self.app_context.pop()
        requestsWrapper.safe_request = self.safe_request

    def test_default_response(self):
        with rgate_app.test_request_context('/'):
            response = requestHandler().default_response()
            self.assertEqual
            (
                response,
                (
                    self.rgate_config['default_response']['body'],
                    self.rgate_config['default_response']['status_code']

                )
            )

    def test_service_unavailable_resposne(self):
        with rgate_app.test_request_context('/'):
            response = requestHandler().service_unavailable_resposne()
            self.assertEqual(response, ('SERVICE UNAVAILABLE', 503))

    def test_get_redirect_url(self):
        with rgate_app.test_request_context('/test'):
            ip = '127.0.0.1'
            port = '4000'
            response = requestHandler().get_redirect_url(ip, port)
            self.assertEqual(response, 'http://127.0.0.1:4000/test')

    def test_check_backend_container_exists(self):
        mockObject = dockerManager
        mockObject.get_containers = mock.Mock(return_value=True)
        with self.subTest('When backend name dont match'):
            backend_name = 'test'
            with rgate_app.test_request_context('/'):
                response = requestHandler().check_backend_container_exists(backend_name)
                self.assertIsNone(response)

        with self.subTest('When backend name exists'):
            backend_name = 'payment'
            with rgate_app.test_request_context('/'):
                response = requestHandler().check_backend_container_exists(backend_name)
                self.assertTrue(response)

    def test_check_backend_exists(self):
        mockObject = dockerManager
        mockObject.get_containers = mock.Mock(return_value=True)
        with self.subTest('When path prefix dont match'):
            with rgate_app.test_request_context('/'):
                response = requestHandler().check_backend_exists()
                self.assertEqual(response, 'Not Matched')

        with self.subTest('When path prefix match'):
            with rgate_app.test_request_context('/api/orders'):
                response = requestHandler().check_backend_exists()
                self.assertTrue(response)

    def test_handle_request(self):
        mockObject = dockerManager
        mockObject.get_containers = mock.Mock(return_value=None)

        with self.subTest('When backend not exists'):
            with rgate_app.test_request_context('/'):
                response = requestHandler().handle_request()
                self.assertEqual
                (
                    response,
                    (
                        self.rgate_config['default_response']['body'],
                        self.rgate_config['default_response']['status_code']

                    )
                )

        with self.subTest('When backend container not exists'):
            with rgate_app.test_request_context('/api/orders'):
                response = requestHandler().handle_request()
                self.assertEqual(response, ('SERVICE UNAVAILABLE', 503))

        with self.subTest('When backend container exists but down'):
            mockObject.get_containers = mock.Mock(return_value=[1])
            mockObject.is_conatiner_down = mock.Mock(return_value=True)
            with rgate_app.test_request_context('/api/orders'):
                response = requestHandler().handle_request()
                self.assertEqual(response, ('SERVICE UNAVAILABLE', 503))

        with self.subTest('When backend container exists and running'):
            mockObject.is_conatiner_down = mock.Mock(return_value=False)
            ip_and_port_return_value = {'ip': '127.0.0.1', 'port': 4000}
            mockObject.get_container_ip_and_port = mock.Mock(return_value=ip_and_port_return_value)

            with rgate_app.test_request_context('/api/orders'):
                response = requestHandler().handle_request()
                self.assertEqual(response, ('Good', 200))
