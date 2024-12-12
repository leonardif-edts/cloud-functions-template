import functions_framework
from flask.wrappers import Request

from core.config import get_config
from core.schemas import (
    parse_data,
    RequestSchema
)
from core.adapters.request import (
    cors_handler,
    authentication,
    error_handler
)
from core.adapters.pubsub import PubSubAdapter


@functions_framework.http
@cors_handler
@authentication(False)
@error_handler
def main(request: Request):
    """
    Validate User Data and Push to Pub/Sub

    Method: POST
    Body: RequestSchema (refer: ./core/schemas.py)
    """
    body_data = dict(request.json)
    data = parse_data(body_data, RequestSchema)

    C = get_config()
    pb = PubSubAdapter(C.PUBSUB_PROJECT)

    pb_data = data.model_dump_json()
    pb.publish(C.PUBSUB_TOPIC, pb_data)

    return {
        "message": "OK",
        "body": data.model_dump()
    }
