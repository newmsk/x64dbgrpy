from x64rdbgpy.proto import bridgemain_pb2_grpc
from x64rdbgpy.proto.base_pb2 import String, Empty
from x64rdbgpy.proto.bridgemain_pb2 import RegDump
from x64rdbgpy.breakpoint import BPs
import grpc


class RegDumpInfo:
    def __init__(self, reg_dump):
        self.r = reg_dump

    def __str__(self):
        pass

    @property
    def cax(self):
        return self.r.reg_context.cax.value
    eax = rax = cax

    @property
    def ccx(self):
        return self.r.reg_context.ccx.value
    ecx = rcx = ccx

    @property
    def cdx(self):
        return self.r.reg_context.cdx.value
    edx = rdx = cdx

    @property
    def cbx(self):
        return self.r.reg_context.cbx.value
    ebx = rbx = cbx

    @property
    def csp(self):
        return self.r.reg_context.csp.value

    @property
    def cbp(self):
        return self.r.reg_context.cbp.value
    ebp = rbp = cbp

    @property
    def csi(self):
        return self.r.reg_context.csi.value
    esi = rsi = csi

    @property
    def cdi(self):
        return self.r.reg_context.cdi.value
    edi = rdi = cdi

    @property
    def r8(self):
        return self.r.reg_context.r8.value

    @property
    def r9(self):
        return self.r.reg_context.r9.value

    @property
    def r10(self):
        return self.r.reg_context.r10.value

    @property
    def r11(self):
        return self.r.reg_context.r11.value

    @property
    def r12(self):
        return self.r.reg_context.r12.value

    @property
    def r13(self):
        return self.r.reg_context.r13.value

    @property
    def r14(self):
        return self.r.reg_context.r14.value

    @property
    def r15(self):
        return self.r.reg_context.r15.value

    @property
    def cip(self):
        return self.r.reg_context.cip.value
    eip = rip = cip

    @property
    def last_error(self):
        return self.r.last_error.name.value

    @property
    def last_status(self):
        return self.r.last_status.name.value

    # TODO wrap x87fpu xmm register here


class BridgeMain:
    def __init__(self, channel):
        self.channel = channel
        self.stub = bridgemain_pb2_grpc.BridgeMainStub(self.channel)

    @classmethod
    def from_target(cls, target):
        return cls(grpc.insecure_channel(target))

    def dbg_exec_cmd(self, cmd):
        return self.stub.DbgCmdExec(String(value=cmd)).boolean

    def dbg_exec_cmd_direct(self, cmd):
        return self.stub.DbgCmdExecDirect(String(value=cmd)).boolean

    def dbg_eval(self, expr):
        expr_value = self.stub.DbgEval(String(value=expr))
        return expr_value.value if expr_value.success else None

    def var_value(self, var_name):
        if not var_name.startswith("$"):
            var_name = "$" + var_name
        return self.dbg_eval(var_name)

    def dbg_exit(self):
        return self.stub.GuiCloseApplication(Empty())

    def dbg_get_bps(self):
        bps = BPs(self.stub.DbgGetBpList(Empty()).bps)
        return bps

    def dbg_get_reg_dump_ex(self):
        reg_dump = RegDumpInfo(self.stub.DbgGetRegDumpEx(Empty()))
        return reg_dump



