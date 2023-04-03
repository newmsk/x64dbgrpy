from x64rdbgpy.proto import stack_pb2_grpc
from x64rdbgpy.proto.base_pb2 import Empty, UnsignedNumberValue
import grpc


class Stack:
    def __init__(self, channel):
        self.channel = channel
        self.stub = stack_pb2_grpc.StackStub(self.channel)

    @classmethod
    def from_target(cls, target):
        return cls(grpc.insecure_channel(target))

    def pop(self):
        return self.stub.Pop(Empty()).value

    def push(self, value):
        return self.stub.Push(UnsignedNumberValue(value=value)).value

    def peek(self, offset):
        return self.stub.Peek(UnsignedNumberValue(value=offset)).value
