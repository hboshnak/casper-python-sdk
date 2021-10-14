import typing

from pycspr.api import constants
from pycspr.api.connection import NodeConnection



def execute(
    node: NodeConnection,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> dict:
    """Returns on-chain block information.

    :param node: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: On-chain block information.

    """
    params = get_params(block_id)
    response = node.get_rpc_response(constants.RPC_CHAIN_GET_BLOCK, params)

    return response["block"]


def get_params(block_id: typing.Union[None, str, int] = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if isinstance(block_id, type(None)):
        return None

    elif isinstance(block_id, (bytes, str)):
        return {
            "block_identifier":{
                "Hash": block_id.hex() if isinstance(block_id, bytes) else block_id
            }            
        }

    elif isinstance(block_id, int):
        return {
            "block_identifier":{
                "Height": block_id
            }            
        }