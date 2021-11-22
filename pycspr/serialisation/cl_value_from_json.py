from pycspr.serialisation.cl_type_from_json import decode as cl_type_from_json
from pycspr.serialisation.cl_value_from_bytes import decode as cl_value_from_bytes


def decode(encoded: dict):
    assert "cl_type" in encoded and "bytes" in encoded

    if isinstance(encoded["bytes"], str):
        return cl_value_from_bytes(
            bytes.fromhex(encoded["bytes"]),
            cl_type_from_json(encoded["cl_type"])
            )
    else:
        return cl_value_from_bytes(
            encoded["bytes"],
            cl_type_from_json(encoded["cl_type"])
            )
