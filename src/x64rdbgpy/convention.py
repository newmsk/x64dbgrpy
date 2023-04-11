from abc import ABC, abstractmethod
from x64rdbgpy.wrapper.register import RegisterConstant

_all_calling_conventions = {}


class Convention(ABC):
    @staticmethod
    @abstractmethod
    def setup(dbg, args):
        pass

    @staticmethod
    @abstractmethod
    def cleanup(dbg, args):
        pass


def register_calling_convention(*cnv_names):
    def decorator(cnv):
        if len(cnv_names) <= 0:
            raise Exception("You must give at least one name when register a new calling convention")
        global _all_calling_conventions
        _all_calling_conventions[cnv_names] = cnv
        return cnv
    return decorator


register_cnv = register_calling_convention


def get_calling_convention(cnv_name):
    global _all_calling_conventions
    for cnv_names, cnv in _all_calling_conventions.items():
        if cnv_name in cnv_names:
            return cnv
    raise Exception(f"No calling convention {cnv_name} found")


@register_cnv('fastcall', '__fastcall')
class FastCall(Convention):
    @staticmethod
    def setup(dbg, args):
        if dbg.x64:
            reg_ids = [RegisterConstant.RCX, RegisterConstant.RDX, RegisterConstant.R8, RegisterConstant.R9]
            for reg_id, value in zip(reg_ids, args):
                dbg.register.set(reg_id, value)

            if len(args) > 4:
                stack_vars = reversed(args[4:])
                for stack_var in stack_vars:
                    dbg.stack.push(stack_var)
        else:
            reg_ids = [RegisterConstant.ECX, RegisterConstant.EDX]
            for reg_id, value in zip(reg_ids, args):
                dbg.register.set(reg_id, value)

            if len(args) > 2:
                stack_vars = reversed(args[2:])
                for stack_var in stack_vars:
                    dbg.stack.push(stack_var)

    @staticmethod
    def cleanup(dbg, args):
        pass


@register_cnv('cdecl', '__cdecl')
class CdeclCall(Convention):
    @staticmethod
    def setup(dbg, args):
        stack_vars = reversed(args)
        for stack_var in stack_vars:
            dbg.stack.push(stack_var)

    @staticmethod
    def cleanup(dbg, args):
        for i in range(len(args)):
            dbg.stack.pop()


@register_cnv('stdcall', '__stdcall')
class StdCall(Convention):
    @staticmethod
    def setup(dbg, args):
        stack_vars = reversed(args)
        for stack_var in stack_vars:
            dbg.stack.push(stack_var)

    @staticmethod
    def cleanup(dbg, args):
        pass
