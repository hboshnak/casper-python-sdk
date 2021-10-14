from pycspr.api import constants
from pycspr.api.connection import NodeConnection



def execute(node: NodeConnection) -> dict:
    """Returns node status information.

    :param node: Information required to connect to a node.
    :returns: Node status information.

    """
    return node.get_rpc_response(constants.RPC_INFO_GET_STATUS)