from capstone import *

from fa.commands import utils

try:
    import idc
    import idaapi
    import _idaapi
    import idautils
except ImportError:
    pass


def locate_start_ppc(segments, ea):
    inf = idaapi.get_inf_structure()
    opcode_size = 4

    mode = CS_MODE_32
    mode |= CS_MODE_BIG_ENDIAN if inf.mf else CS_MODE_LITTLE_ENDIAN
    cs = Cs(CS_ARCH_PPC, mode)

    while True:
        inst = list(cs.disasm(utils.read_memory(segments, ea, opcode_size), ea))[0]

        if ((inst.mnemonic == 'stwu') and (inst.op_str.startswith('r1'))) or \
                ((inst.mnemonic == 'mr') and (inst.op_str.startswith('r12, r1'))):
            return ea

        ea -= opcode_size


LOCATE_START_BY_ARCH = {
    'PPC': locate_start_ppc
}


def get_function_start(segments, ea):
    start = idc.GetFunctionAttr(ea, idc.FUNCATTR_START)
    if start != idc.BADADDR:
        # get from ida
        return start

    # extract load address ourselves
    inf = idaapi.get_inf_structure()
    proc_name = inf.procName

    if proc_name in LOCATE_START_BY_ARCH.keys():
        return LOCATE_START_BY_ARCH[proc_name](segments, ea)


def run(segments, manners, addresses, args, **kwargs):
    utils.verify_ida()
    return list(set([get_function_start(segments, ea) for ea in addresses]))
