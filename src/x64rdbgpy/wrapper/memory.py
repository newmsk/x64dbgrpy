from x64rdbgpy.proto import memory_pb2_grpc
from x64rdbgpy.proto.base_pb2 import Address, BinaryData
from x64rdbgpy.proto.memory_pb2 import AddressAndSizePair, MemoryWriteParam
import grpc


class Memory:
    def __init__(self, channel):
        self.channel = channel
        self.stub = memory_pb2_grpc.MemoryStub(self.channel)

    @classmethod
    def from_target(cls, target):
        return cls(grpc.insecure_channel(target))

    def read(self, address, size):
        addr = Address(address=address)
        addr_and_size_pair = AddressAndSizePair(address=addr, size=size)
        return self.stub.Read(addr_and_size_pair).data

    def write(self, address, data):
        addr = Address(address=address)
        bin_data = BinaryData(data=data)
        mem_write_param = MemoryWriteParam(address=addr, data=bin_data)
        return self.stub.Write(mem_write_param).value

    def is_valid_ptr(self, address):
        return self.stub.IsValidPtr(Address(address=address))

    def remote_alloc(self, address, size):
        addr = Address(address=address)
        addr_and_size_pair = AddressAndSizePair(address=addr, size=size)
        return self.stub.RemoteAlloc(addr_and_size_pair).address

    def remote_free(self, address):
        return self.stub.RemoteFree(Address(address=address)).boolean

    def get_protect(self, address):
        return self.stub.GetProtect(Address(address=address)).value

    def get_base(self, address):
        return self.stub.GetBase(Address(Address=address)).address

    def get_size(self, address):
        return self.stub.GetSize(Address(address=address)).value
