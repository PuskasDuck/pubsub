from google.api_core.exceptions import NotFound
from google.cloud.pubsub import PublisherClient
from google.protobuf.json_format import MessageToJson
from google.pubsub_v1.types import Encoding

from utilities import us_states_pb2  # type: ignore

# TODO(developer): Replace these variables before running the sample.
# project_id = "your-project-id"
# topic_id = "your-topic-id"

publisher_client = PublisherClient()
topic_path = publisher_client.topic_path(project_id, topic_id)

try:
    # Get the topic encoding type.
    topic = publisher_client.get_topic(request={"topic": topic_path})
    encoding = topic.schema_settings.encoding

    # Instantiate a protoc-generated class defined in `us-states.proto`.
    state = us_states_pb2.StateProto()
    state.name = "Alaska"
    state.post_abbr = "AK"

    # Encode the data according to the message serialization type.
    if encoding == Encoding.BINARY:
        data = state.SerializeToString()
        print(f"Preparing a binary-encoded message:\n{data}")
    elif encoding == Encoding.JSON:
        json_object = MessageToJson(state)
        data = str(json_object).encode("utf-8")
        print(f"Preparing a JSON-encoded message:\n{data}")
    else:
        print(f"No encoding specified in {topic_path}. Abort.")
        exit(0)

    future = publisher_client.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

except NotFound:
    print(f"{topic_id} not found.")
