import random

from flask import current_app as rgate_app
from flask import request

from rgate_app.dockermanager import dockerManager
from rgate_app.requestwrapper import requestsWrapper


class requestHandler:
    def __init__(self):
        self.rgate_config = rgate_app.config["RGATE_CONFIG"]
        self.request = request
        self.path = request.path
        self.method = request.method

    def default_response(self):
        message = self.rgate_config.get("default_response", {}).get("body")
        status = self.rgate_config.get("default_response", {}).get("status_code")
        return message, status

    def service_unavailable_resposne(self):
        return "SERVICE UNAVAILABLE", 503

    def get_one_container(self, backend_containers: list) -> object:
        return random.choice(backend_containers)

    def get_container_round_robin(
        self, backend_containers: list, backend_name: str
    ) -> object:
        """
        this method is used to get container based on round robin.

        Args:
            backend_containers(list): Containers list.
            backend_name(str): Backend name

        Example:
            rgate_app.BACKEND_CONTAINER_ROUNDROBIN = {'payment': [conatiner1, conatiner2]}
        """
        used_containers = rgate_app.BACKEND_CONTAINER_ROUNDROBIN.get(backend_name, [])
        if set(used_containers) == set(backend_containers):
            used_containers = []
        for container in backend_containers:
            if container not in used_containers:
                used_containers.append(container)
                rgate_app.BACKEND_CONTAINER_ROUNDROBIN[backend_name] = used_containers
                return container

    def get_redirect_url(self, ip: str, port: str) -> str:
        """This method is used to get an url"""
        return f"http://{ip}:{port}{self.path}"

    def handle_request(self):
        """This method handle the request.
        A container is selected as a backend if the container has all the match_labels present as
        Docker labels. If there are multiple containers matching, select a random container as a
        backend.
        - Incoming http requests are routed to the corresponding backend if the path starts with
        the given path_prefix.
        - If there are no routes matching the request, it should respond with the given body and
        status_code in the default_response
        - If the backend is down, respond with 503 code
        """
        backend_name, backend_containers = self.check_backend_exists()
        if backend_containers == "Not Matched":
            return self.default_response()
        elif not backend_containers:
            return self.service_unavailable_resposne()
        # container = self.get_one_container(backend_containers, backend_name)
        container = self.get_container_round_robin(backend_containers, backend_name)
        docmang = dockerManager()
        if docmang.is_conatiner_down(container):
            return self.service_unavailable_resposne()
        container_details = docmang.get_container_ip_and_port(container)
        if not container_details:
            return self.service_unavailable_resposne()
        url = self.get_redirect_url(container_details["ip"], container_details["port"])
        rw = requestsWrapper()
        reponse, status_code = rw.safe_request(url, self.request.data, self.method)
        if not status_code:
            return self.default_response()
        return reponse, status_code

    def check_backend_container_exists(self, backend_name: str):
        for backend in self.rgate_config.get("backends"):
            if (
                isinstance(backend, dict)
                and backend.get("name") == backend_name
                and backend.get("match_labels")
            ):
                return backend_name, dockerManager().get_containers(
                    backend["match_labels"]
                )

    def check_backend_exists(self):
        """This method is used to check if backend exists for given path."""
        for route in self.rgate_config.get("routes"):
            if (
                isinstance(route, dict)
                and self.path.startswith(route.get("path_prefix"))
                and route.get("backend")
            ):
                return self.check_backend_container_exists(route["backend"])
        return None, "Not Matched"
