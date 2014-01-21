from pydbg import *
from pydbg.defines import *
import struct

def bp_callback(dbg):
    pointer_on_stack = dbg.read_process_memory(dbg.context.Esp + 0x04, 4)
    unpacked_pointer = struct.unpack("<L", pointer_on_stack)[0]
    fileName = dbg.smart_dereference(unpacked_pointer, True)
    print 'File Name '+ fileName
    return DBG_CONTINUE

dbg = pydbg()
for pid, name in dbg.enumerate_processes():
    if name == 'AbilityServer.exe':
        dbg.attach(pid)

bp1 = dbg.func_resolve_debuggee("kernel32.dll", "CreateFileA")
bp2 = dbg.func_resolve_debuggee("kernel32.dll", "CreateFileW")

dbg.bp_set(bp1, description='BP 1', handler=bp_callback)
dbg.bp_set(bp2, description='BP 2', handler=bp_callback)
dbg.debug_event_loop()
