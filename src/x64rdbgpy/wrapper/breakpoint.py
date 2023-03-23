
class BP:
    def __init__(self, rpc_bp):
        self.type = rpc_bp.type
        self.addr = rpc_bp.addr.address
        self.enabled = rpc_bp.enabled.boolean
        self.single_shoot = rpc_bp.single_shoot.boolean
        self.active = rpc_bp.active.boolean
        self.name = rpc_bp.name.value
        self.mod = rpc_bp.mod.value
        self.typeEx = rpc_bp.typeEx.value
        self.hw_size = rpc_bp.hw_size.value
        self.hit_count = rpc_bp.hit_count.value
        self.fast_resume = rpc_bp.fast_resume.boolean
        self.silent = rpc_bp.silent.boolean
        self.break_condition = rpc_bp.break_condition.value
        self.log_text = rpc_bp.log_text.value
        self.log_condition = rpc_bp.log_condition.value
        self.command_text = rpc_bp.command_text.value
        self.command_condition = rpc_bp.command_condition.value

    def __str__(self):
        return f"{self.addr:#x} " \
               f"{self.get_bp_type_str(self.type)} " \
               f"{'enable' if self.enabled else 'disable'} " \
               f"{self.name}"

    def __repr__(self):
        pass

    @staticmethod
    def get_bp_type_str(bp_type):
        bp_type_str_map = {
            0: "bp_none",
            1: "bp_normal",
            2: "bp_hardware",
            4: "bp_memory",
            8: "bp_dll",
            16: "bp_exception",
        }

        if bp_type in bp_type_str_map:
            return bp_type_str_map[bp_type]


class BPs:
    def __init__(self, msg_bp_list):
        self.bp_list = sorted([BP(msg_bp) for msg_bp in msg_bp_list],
                              key=lambda bp: bp.addr)

    def __str__(self):
        hdr = f"total {len(self.bp_list)} breakpoint(s): \n"
        bps_info = ""
        for x in self.bp_list:
            bps_info += f"[+] {x} \n"
        return hdr + bps_info

    def __repr__(self):
        pass

    def __iter__(self):
        self.bp_index = 0
        return self

    def __next__(self):
        if self.bp_index >= len(self.bp_list):
            raise StopIteration
        bp = self.bp_list[self.bp_index]
        self.bp_index += 1
        return bp

    def __getitem__(self, addr_or_name):
        if isinstance(addr_or_name, str):
            return self.get_bp_by_name(addr_or_name)
        elif isinstance(addr_or_name, int):
            return self.get_bp_by_addr(addr_or_name)
        else:
            raise KeyError(f"{addr_or_name}")

    def get_bp_by_addr(self, addr):
        for bp in self.bp_list:
            if bp.addr == addr:
                return bp
        return None

    def get_bp_by_name(self, name):
        for bp in self.bp_list:
            if bp.name == name:
                return bp
        return None

    def get_bps_by_attr(self):
        pass

    @property
    def active_bps(self):
        pass

    @property
    def enabled_bps(self):
        pass

    @property
    def type_bps(self):
        pass

    @property
    def module_bps(self):
        pass

