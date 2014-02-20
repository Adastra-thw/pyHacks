#!/usr/bin/env python

__VERSION__ = '1.0'
import immlib
from immlib import AllExceptHook
DESC = "Simple PyHook" 


class DemoHook(AllExceptHook): 
    def __init__(self):
	AllExceptHook.__init__(self)

    def run(self, regs): 
	imm = immlib.Debugger()
	for key in regs.keys():
	    reg = regs[key]
	    imm.log("REGISTER %s at 0x%08X " %(key, reg)) 
    
def main(args):
    imm = immlib.Debugger()
    newHook = DemoHook()
    newHook.add("Demo Hook") 
    return "Success!" 
