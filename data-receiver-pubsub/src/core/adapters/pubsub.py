from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.futures import Future


class PubSubAdapter:
    """
    Pub/Sub Adapter

    Adapter for sending or publish message to Pub/Sub

    params:
        - project: [str] Project ID for Pub/Sub
    """
    __project_id: str
    __pub: PublisherClient

    def __init__(self, project: str):
        self.__project_id = project
        self.__pub = PublisherClient()


    def publish(self, topic: str, data: str):
        """
        Publish

        Publish string to Pub/Sub.

        params:
            - topic: [str] Pub/Sub topic to be published
            - data: [str] Message to be published
        """
        __topic = f"projects/{self.__project_id}/topics/{topic}"
        future: Future = self.__pub.publish(__topic, data.encode())
        future.result()
