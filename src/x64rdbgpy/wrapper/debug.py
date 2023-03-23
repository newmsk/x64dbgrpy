from x64rdbgpy.proto import debug_pb2_grpc
from x64rdbgpy.proto.base_pb2 import Empty, Address
from x64rdbgpy.proto.debug_pb2 import HardwareBreakpoint
from x64rdbgpy.bridgemain import BridgeMain
import grpc


class Debug:
    def __init__(self, channel):
        self.channel = channel
        self.stub = debug_pb2_grpc.DebugStub(self.channel)
        self.bridge_main = BridgeMain(self.channel)
        self.dbg_exec_cmd = self.bridge_main.dbg_exec_cmd

    @classmethod
    def from_target(cls, target):
        return cls(grpc.insecure_channel(target))

    def hello(self):
        self.stub.Hello(Empty())

    def init(self, remote_path, cmdline=""):
        cmd = " ".join(("init", remote_path, cmdline))
        if self.bridge_main.dbg_exec_cmd(cmd):
            return self.bridge_main.var_value("$pid")

    def wait(self):
        self.stub.Wait(Empty())

    def run(self):
        self.stub.Run(Empty())

    def pause(self):
        self.stub.Pause(Empty())

    def stop(self):
        self.stub.Stop(Empty())

    def step_into(self):
        self.stub.StepIn(Empty())

    def step_over(self):
        self.stub.StepOver(Empty())

    def step_out(self):
        self.stub.StepOut(Empty())

    def set_breakpoint(self, address):
        return self.stub.SetBreakpoint(Address(address=address)).boolean

    def delete_breakpoint(self, address):
        return self.stub.DeleteBreakpoint(Address(address=address)).boolean

    def disable_breakpoint(self, address):
        return self.stub.DisableBreakpoint(Address(address=address)).boolean

    def set_hardware_breakpoint(self, address, hardware_type):
        addr = Address(address=address)
        hbp = HardwareBreakpoint(address=addr, type=hardware_type)
        return self.stub.SetHardwareBreakpoint(hbp).boolean

    def delete_hardware_breakpoint(self, address):
        return self.stub.DeleteHardwareBreakpoint(Address(address=address)).boolean
