from pydbg import *
from pydbg.defines import *

def bp_process_recv(dbg):
    print 'Recv Called!!'
    print dbg.dump_context(dbg.context)
    return DBG_CONTINUE

def bp_process_send(dbg):
    print 'Send Called!!'
    print dbg.dump_context(dbg.context)
    return DBG_CONTINUE

dbg = pydbg()
for pid, name in dbg.enumerate_processes():
    if name == 'minishare.exe':
        dbg.attach(pid)

send_api = dbg.func_resolve('ws2_32', 'send')
recv_api = dbg.func_resolve('ws2_32', 'recv')
dbg.bp_set(send_api, handler=bp_process_send)
dbg.bp_set(recv_api, handler=bp_process_recv)
dbg.run()
