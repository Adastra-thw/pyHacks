from pydbg import *
from pydbg.defines import *

dbg = pydbg()
dbg.attach(1884)

def detect_overflow(dbg):
    if dbg.dbg.u.Exception.dwFirstChance:
        return DBG_EXCEPTION_NOT_HANDLED
    print 'Access Violation Happened!!'
    print 'EIP %0x' %dbg.context.Eip
    return DBG_EXCEPTION_NOT_HANDLED

dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, detect_overflow)
dbg.run()
