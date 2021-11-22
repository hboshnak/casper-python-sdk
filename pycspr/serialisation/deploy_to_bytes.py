import typing

from pycspr.serialisation.cl_value_to_bytes import encode as cl_value_to_bytes
from pycspr.serialisation.cl_type_to_bytes import encode as cl_type_to_bytes
from pycspr.serialisation.cl_value_to_cl_type import encode as cl_value_to_cl_type
from pycspr.types.cl import cl_values
from pycspr.types.deploys import Deploy
from pycspr.types.deploys import DeployApproval
from pycspr.types.deploys import DeployArgument
from pycspr.types.deploys import DeployHeader
from pycspr.types.deploys import ModuleBytes
from pycspr.types.deploys import StoredContractByHash
from pycspr.types.deploys import StoredContractByHashVersioned
from pycspr.types.deploys import StoredContractByName
from pycspr.types.deploys import StoredContractByNameVersioned
from pycspr.types.deploys import Transfer


def encode(entity: object) -> bytes:
    if isinstance(entity, Deploy):
        raise NotImplementedError()

    if isinstance(entity, DeployApproval):
        return entity.signer + entity.signature

    if isinstance(entity, DeployArgument):
        print(111, cl_value_to_bytes(cl_values.CL_String(entity.name)).hex())
        print(222, _u8_array_to_bytes(cl_value_to_bytes(entity.value)).hex())
        print(333, cl_type_to_bytes(cl_value_to_cl_type(entity.value)).hex())

        return \
            cl_value_to_bytes(cl_values.CL_String(entity.name)) + \
            _u8_array_to_bytes(cl_value_to_bytes(entity.value)) + \
            cl_type_to_bytes(cl_value_to_cl_type(entity.value))

    if isinstance(entity, DeployHeader):
        raise NotImplementedError()

    if isinstance(entity, ModuleBytes):
        for arg in entity.args:
            print(encode(arg).hex())
        # print(_vector_to_bytes(list(map(encode, entity.args))))
        return \
            bytes([0]) + \
            _u8_array_to_bytes(list(entity.module_bytes)) + \
            _vector_to_bytes(list(map(encode, entity.args)))

    if isinstance(entity, StoredContractByHash):
        return \
            bytes([1]) + \
            cl_value_to_bytes(cl_values.CL_ByteArray(entity.hash)) + \
            cl_value_to_bytes(cl_values.CL_String(entity.entry_point)) + \
            _vector_to_bytes(list(map(encode, entity.args)))

    if isinstance(entity, StoredContractByHashVersioned):
        return \
            bytes([2]) + \
            cl_value_to_bytes(cl_values.CL_ByteArray(entity.hash)) + \
            cl_value_to_bytes(cl_values.CL_U32(entity.version)) + \
            cl_value_to_bytes(cl_values.CL_String(entity.entry_point)) + \
            _vector_to_bytes(list(map(encode, entity.args)))

    if isinstance(entity, StoredContractByName):
        return \
            bytes([3]) + \
            cl_value_to_bytes(cl_values.CL_String(entity.name)) + \
            cl_value_to_bytes(cl_values.CL_String(entity.entry_point)) + \
            _vector_to_bytes(list(map(encode, entity.args)))

    if isinstance(entity, StoredContractByNameVersioned):
        return \
            bytes([4]) + \
            cl_value_to_bytes(cl_values.CL_String(entity.name)) + \
            cl_value_to_bytes(cl_values.CL_U32(entity.version)) + \
            cl_value_to_bytes(cl_values.CL_String(entity.entry_point)) + \
            _vector_to_bytes(list(map(encode, entity.args)))

    if isinstance(entity, Transfer):
        return \
            bytes([5]) + \
            _vector_to_bytes(list(map(encode, entity.args)))


def _u8_array_to_bytes(value: typing.List[int]) -> bytes:
    return cl_value_to_bytes(cl_values.CL_U32(len(value))) + bytes(value)


def _vector_to_bytes(value: typing.List) -> bytes:
    return \
        cl_value_to_bytes(cl_values.CL_U32(len(value))) + \
        bytes([i for j in value for i in j])