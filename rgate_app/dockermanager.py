from typing import List

import docker


class dockerManager:
    def __init__(self):
        self.client = self.get_client()

    def get_client(self):
        try:
            return docker.from_env()
        except docker.errors.DockerException:
            return None

    def get_containers(self, labels: List[str] = []):
        """This method is used to get containers based on the given labels

        Args:
            labels: Container labels

        Returs:
            list: List of matched containers

        """
        return (
            self.client.containers.list(filters={"label": labels})
            if self.client
            else []
        )

    def get_container_ip_and_port(self, container: object) -> dict:
        """This method is used to get conatiner ip and port"""
        container_ports = container.ports
        if container_ports:
            port_key = list(container_ports.keys())[0]
            return {
                "ip": container_ports[port_key][0].get("HostIp"),
                "port": container_ports[port_key][0].get("HostPort"),
            }

    def is_conatiner_down(self, conatiner: object):
        """This method is used to check if conatiner is running or not."""
        return False if conatiner.status == "running" else True
