from x64rdbgpy.wrapper.debug import Debug
from x64rdbgpy.wrapper.register import Register
from x64rdbgpy.wrapper.memory import Memory
from x64rdbgpy.wrapper.bridgemain import BridgeMain
from x64rdbgpy.wrapper.module import Module
import grpc


class X64RDbg:
    def __init__(self, remote_ip, remote_port):
        self.remote_ip = remote_ip
        self.remote_port = str(remote_port)
        self.target = ":".join((self.remote_ip, self.remote_port))
        self.channel = grpc.insecure_channel(self.target)

        self.ctx = {}

        self.debug = Debug(self.channel)
        self.register = Register(self.channel)
        self.memory = Memory(self.channel)
        self.bridgemain = BridgeMain(self.channel)
        self.module = Module(self.channel)

    def hello(self):
        self.debug.Hello()

    def start(self, remote_path="", cmdline=""):
        pid = self.debug.init(remote_path, cmdline)
        if pid != 0:
            self.ctx["pid"] = pid
            return True
        return False

    def stop(self):
        return self.debug.stop()

    def exit(self):
        return self.bridgemain.dbg_exit()

    def attach(self):
        pass

    def detach(self):
        pass

    def run(self):
        return self.debug.run()

    @property
    def modules(self):
        return self.module.get_modules()

    @property
    def memory_map(self):
        pass

    @property
    def registers(self):
        return self.bridgemain.dbg_get_reg_dump_ex()

    @property
    def threads(self):
        pass

    @property
    def breakpoints(self):
        return self.bridgemain.dbg_get_bps()

    @property
    def pid(self):
        return self.bridgemain.var_value("pid")

    def set_breakpoint(self):
        pass

    def set_software_breakpoint(self, va, name="", bp_type="short", single_shot=False):
        ss = ""
        if single_shot:
            ss = "ss"
        self.bridgemain.dbg_exec_cmd_direct(f"bp {va:#x},{name},{ss}{bp_type}")

    def set_hardware_breakpoint(self, va, bp_type="x", bp_size=1):
        self.bridgemain.dbg_exec_cmd_direct(f"bph {va:#x},{bp_type},{bp_size}")

    def set_memory_breakpoint(self, va, bp_type="a", single_shot=False):
        ss = "0"
        if single_shot:
            ss = "1"
        self.bridgemain.dbg_exec_cmd_direct(f"bpm {va:#x}, {ss}, {bp_type}")

    def clear_software_breakpoint(self, va):
        self.bridgemain.dbg_exec_cmd_direct(f"bpc {va:#x}")

    def clear_hardware_breakpoint(self, va):
        self.bridgemain.dbg_exec_cmd_direct(f"bphc {va:#x}")

    def clear_breakpoint(self, va):
        self.clear_software_breakpoint(va)
        self.clear_hardware_breakpoint(va)

    def clear_all_breakpoints(self):
        self.bridgemain.dbg_exec_cmd_direct("bpc")
        self.bridgemain.dbg_exec_cmd_direct("bphc")

    def disassemble(self):
        pass

    def bp(self, base, rva, bp_type=""):
        self.bridgemain.dbg_exec_cmd_direct()

    def bpc(self, ):
        pass
    bps = set_software_breakpoint


