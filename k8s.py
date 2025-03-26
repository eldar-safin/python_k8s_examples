import json
from kubernetes import client, config
from datetime import datetime


DEFAULT_NAMESPACE = 'default'


class Pod:
    def __init__(self, raw_data) -> None:
        raw_container = raw_data.spec.containers[0]
        raw_resources = raw_container.resources
        self.name = raw_data.metadata.name
        self.namespace = raw_data.metadata.namespace
        self.image = raw_container.image
        self.cpu_limit = raw_resources.limits.get('cpu')
        self.cpu_request = raw_resources.requests.get('cpu')
        self.memory_limit = raw_resources.limits.get('memory')
        self.memory_request = raw_resources.requests.get('memory')
        self.created_at = raw_data.metadata.creation_timestamp
        self.ip = raw_data.status.pod_ip

    def to_json(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.isoformat() if isinstance(o, datetime) else o.__dict__,
            sort_keys=True,
            indent=4
        )


class K8S:

    def __init__(self) -> None:
        config.load_kube_config()
        self.api_client = client.CoreV1Api()

    def get_pods(self, namespace: str = DEFAULT_NAMESPACE) -> list[Pod]:
        raw_pods = self.api_client.list_namespaced_pod(namespace=namespace)
        return [Pod(raw_data=data) for data in raw_pods.items]

    def get_images(self, namespace: str = DEFAULT_NAMESPACE) -> list[str]:
        return [pod.image for pod in self.get_pods(namespace)]
