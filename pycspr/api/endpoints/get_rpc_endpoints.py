import typing

from pycspr.api.endpoints.get_rpc_schema import execute as get_rpc_schema
from pycspr.api.connection import NodeConnection



def execute(node: NodeConnection) -> typing.List[str]:
    """Returns set of JSON-RPC constants.

    :param node: Information required to connect to a node.
    :returns: A list of all supported RPC constants.

    """
    schema = get_rpc_schema(node)

    return sorted([i["name"] for i in schema["methods"]])