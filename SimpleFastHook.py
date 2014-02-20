#!/usr/bin/python
import immlib
DESC = "FastLogHook"

def main(args) :
    imm = immlib.Debugger()
    fastHook = imm.getKnowledge("fast")
    if fastHook : 
	loggingResults = fastHook.getAllLog()
	imm.log(str(loggingResults))
	(functionAddress, (esp, esp_4, esp_8)) = loggingResults[0]
	dataReceived = imm.readString(esp_8)
	imm.log(dataReceived)
	    
    functionToHook = "msvcrt.strcpy"
    functionAddress = imm.getAddress(functionToHook)
    fastHook = immlib.FastLogHook(imm) 
    fastHook.logFunction(functionAddress) 
    fastHook.logBaseDisplacement('ESP', 0) 
    fastHook.logBaseDisplacement('ESP', 4)
    fastHook.logBaseDisplacement('ESP', 8) 
    fastHook.Hook()
    imm.addKnowledge("fast", fastHook, force_add = 1) 
    return "Success!"
