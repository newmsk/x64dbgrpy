from x64rdbgpy.proto import module_pb2_grpc
from x64rdbgpy.proto.base_pb2 import Empty
from collections import namedtuple
import grpc


class ModuleInfo(namedtuple("ModuleInfo", ["base", "size", "entry", "section_count", "name", "path"])):
    def __repr__(self):
        return f"[{self.base:#018x}|{self.name}]: {self.path}"

    def __str__(self):
        return f"[{self.base:#018x}|{self.name}]: {self.path}"


class Module:
    def __init__(self, channel):
        self.channel = channel
        self.stub = module_pb2_grpc.ModuleStub(self.channel)

    @classmethod
    def from_target(cls, target):
        return cls(grpc.insecure_channel(target))

    def get_modules(self):
        modules = []
        mods = self.stub.GetList(Empty()).modules
        for mod in mods:
            modules.append(ModuleInfo(
                mod.base.address,
                mod.size.value,
                mod.entry.address,
                mod.section_count.value,
                mod.name.value,
                mod.path.value
            ))

        return modules

    def get_main_module_base(self):
        return self.stub.GetMainModuleBase(Empty()).address

    def get_main_module_size(self):
        return self.stub.GetMainModuleSize(Empty()).value

    def get_main_module_entry(self):
        return self.stub.GetMainModuleEntry(Empty()).address



