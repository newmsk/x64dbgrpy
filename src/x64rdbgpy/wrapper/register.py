from x64rdbgpy.proto import register_pb2_grpc
from x64rdbgpy.proto.base_pb2 import Empty
from x64rdbgpy.proto.register_pb2 import RegisterId, RegisterValue, RegisterIdValuePair
import x64rdbgpy.proto.register_pb2 as regs_id
import grpc


class RegisterConstant:
    DR0 = regs_id.DR0
    DR1 = regs_id.DR1
    DR2 = regs_id.DR2
    DR3 = regs_id.DR3
    DR6 = regs_id.DR6
    DR7 = regs_id.DR7
    EAX = regs_id.EAX
    AX = regs_id.AX
    AH = regs_id.AH
    AL = regs_id.AL
    EBX = regs_id.EBX
    BX = regs_id.BX
    BH = regs_id.BH
    BL = regs_id.BL
    ECX = regs_id.ECX
    CX = regs_id.CX
    CH = regs_id.CH
    CL = regs_id.CL
    EDX = regs_id.EDX
    DX = regs_id.DX
    DH = regs_id.DH
    DL = regs_id.DL
    EDI = regs_id.EDI
    DI = regs_id.DI
    ESI = regs_id.ESI
    SI = regs_id.SI
    EBP = regs_id.EBP
    BP = regs_id.BP
    ESP = regs_id.ESP
    SP = regs_id.SP
    EIP = regs_id.EIP
    EFLAGS_x86 = regs_id.EFLAGS_x86

    RAX = regs_id.RAX
    RBX = regs_id.RBX
    RCX = regs_id.RCX
    RDX = regs_id.RDX
    RSI = regs_id.RSI
    SIL = regs_id.SIL
    RDI = regs_id.RDI
    DIL = regs_id.DIL
    RBP = regs_id.RBP
    BPL = regs_id.BPL
    RSP = regs_id.RSP
    SPL = regs_id.SPL
    RIP = regs_id.RIP
    R8 = regs_id.R8
    R8D = regs_id.R8D
    R8W = regs_id.R8W
    R8B = regs_id.R8B
    R9 = regs_id.R9
    R9D = regs_id.R9D
    R9W = regs_id.R9W
    R9B = regs_id.R9B
    R10 = regs_id.R10
    R10D = regs_id.R10D
    R10W = regs_id.R10W
    R10B = regs_id.R10B
    R11 = regs_id.R11
    R11D = regs_id.R11D
    R11W = regs_id.R11W
    R11B = regs_id.R11B
    R12 = regs_id.R12
    R12D = regs_id.R12D
    R12W = regs_id.R12W
    R12B = regs_id.R12B
    R13 = regs_id.R13
    R13D = regs_id.R13D
    R13W = regs_id.R13W
    R13B = regs_id.R13B
    R14 = regs_id.R14
    R14D = regs_id.R14D
    R14W = regs_id.R14W
    R14B = regs_id.R14B
    R15 = regs_id.R15
    R15D = regs_id.R15D
    R15W = regs_id.R15W
    R15B = regs_id.R15B
    EFLAGS_x64 = regs_id.EFLAGS_x64

    CIP = regs_id.CIP
    CSP = regs_id.CSP
    CAX = regs_id.CAX
    CBX = regs_id.CBX
    CCX = regs_id.CCX
    CDX = regs_id.CDX
    CDI = regs_id.CDI
    CSI = regs_id.CSI
    CBP = regs_id.CBP
    CFLAGS = regs_id.CFLAGS


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
