import docker
import socket


class DockerManager:
    def __init__(self):
        self.client = docker.from_env() #создание клиента для работы с контейнером

    def create_container(self, image, mem_limit, cpus):
        try:
            ssh_port = self._get_available_port()#получает свободный порт на хост машине
            ports = {'22/tcp': ssh_port}
            container = self.client.containers.run(
                image,
                detach=True,
                ports=ports,
                mem_limit=mem_limit,
                #cpus=cpus
            )
            container_id = container.id
            return container_id, ssh_port
        except Exception as e:
            return f"Error creating container: {e}", None


    def get_container_ip(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            return container.attrs['NetworkSettings']['IPAddress']
        except Exception as e:
            return f"Error getting container IP: {e}"


    def start_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.start()
            return f"Container {container_id} started"
        except Exception as e:
            return f"Error starting container: {e}"

    def stop_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            return f"Container {container_id} stopped"
        except Exception as e:
            return f"Error stopping container: {e}"

    def remove_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.remove()
            return f"Container {container_id} removed"
        except Exception as e:
            return f"Error removing container: {e}"
    def _get_available_port(self):

        sock = socket.socket()
        sock.bind(('localhost', 0))#0 - выбираем свободный
        return sock.getsockname()[1]
