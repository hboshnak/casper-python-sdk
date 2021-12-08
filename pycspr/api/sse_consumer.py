import json
import typing

import requests
import sseclient

from pycspr.api.connection import NodeConnection
from pycspr.api.sse_types import NodeEventChannel
from pycspr.api.sse_types import NodeEventType
from pycspr.api.sse_types import NodeEventInfo
from pycspr.api.sse_types import SSE_CHANNEL_TO_SSE_EVENT


def get_events(
    node: NodeConnection,
    callback: typing.Callable[[NodeEventInfo], None],
    event_channel: NodeEventChannel,
    event_type: NodeEventType = None,
    event_id: int = 0
):
    """Binds to a node's event stream - events are passed to callback for processing.

    :param node: Information required to connect to a node.
    :param callback: Callback to invoke whenever an event of relevant type is received.
    :param event_channel: Type of event channel to which to bind.
    :param event_type: Type of event type to listen for (all if unspecified).
    :param event_id: Identifier of event from which to start stream listening.

    """
    iterator = yield_events(node, event_channel, event_type, event_id)
    for event_info in iterator:
        callback(event_info)


def yield_events(
    node: NodeConnection,
    event_channel: NodeEventChannel,
    event_type: NodeEventType = None,
    event_id: int = 0
) -> typing.Generator[NodeEventInfo, None, None]:
    """Yields information about event being emitted by a node's event stream.

    :param node: Information required to connect to a node.
    :param event_channel: Type of event channel to which to bind.
    :param event_type: Type of event type to listen for (all if unspecified).
    :param event_id: Identifier of event from which to start stream listening.

    """
    if event_channel not in SSE_CHANNEL_TO_SSE_EVENT:
        raise ValueError(f"Unsupported SSE channel: {event_channel.name}.")
    if event_type is not None and event_type not in SSE_CHANNEL_TO_SSE_EVENT[event_channel]:
        raise ValueError(f"Unsupported channel/event: {event_channel.name}:{event_type.name}.")

    sse_client = _get_sse_client(node, event_channel, event_id)
    try:
        for sse_event in sse_client.events():
            try:
                event_payload = json.loads(sse_event.data)
            except json.JSONDecodeError:
                event_payload = str(sse_event.data)
            event_type = _get_event_type(event_payload)
            yield NodeEventInfo(event_channel, event_type, sse_event.id, event_payload)
    except Exception as err:
        try:
            sse_client.close()
        except Exception as inner_err:
            print(inner_err)
        finally:
            raise err


def _get_sse_client(node: NodeConnection, event_channel: NodeEventChannel, event_id: int) -> sseclient.SSEClient:
    """Returns SSE client.

    """
    url = f"{node.address_sse}/{event_channel.name.lower()}"
    if event_id:
        url = f"{url}?start_from={event_id}"
    stream = requests.get(url, stream=True)

    return sseclient.SSEClient(stream)


def _get_event_type(payload: dict) -> NodeEventType:
    """Maps incoming event payload to associated event type.

    """
    for event_type in NodeEventType:
        if event_type.name in payload:
            return event_type

    print("TODO: process unknown event: {payload}")
