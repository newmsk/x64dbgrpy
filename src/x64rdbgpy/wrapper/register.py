from x64rdbgpy.proto import register_pb2_grpc
from x64rdbgpy.proto.base_pb2 import Empty
from x64rdbgpy.proto.register_pb2 import RegisterId, RegisterValue, RegisterIdValuePair
import grpc


class Register:
    def __init__(self, channel):
        self.channel = channel
        self.stub = register_pb2_grpc.RegisterStub(self.channel)

    @classmethod
    def from_target(cls, target):
        return cls(grpc.insecure_channel(target))

    def get(self, reg):
        return self.stub.Get(RegisterId(id=reg)).value

    def set(self, reg, value):
        reg_id = RegisterId(id=reg)
        reg_value = RegisterValue(value=value)
        reg_id_value_pair = RegisterIdValuePair(id=reg_id, value=reg_value)
        return self.stub.Set(reg_id_value_pair).boolean

    # def get_arch_reg_size(self):
    #     return self.stub.Size(Empty()).value
    #
    # @property
    # def size(self):
    #     return self.get_arch_reg_size()

    def size(self):
        return self.stub.Size(Empty()).value