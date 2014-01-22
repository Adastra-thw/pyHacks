import immlib

DESC = "PyCommand Description"

def main(args):
    imm = immlib.Debugger()
    imm.log("Log Entry!")
    imm.updateLog()

    '''
    table = imm.createTable("PyCommand Example", ["PID", "NAME", "PATH", "SERVICES"])
    psList = imm.ps()
    for ps in psList:
        table.add(0, [str(ps[0]), ps[1], ps[2], str(ps[3])])
    
    imm.Attach(2564)
    imm.restartProcess()

    

    table = imm.createTable("Modules PyCommand", ["NAME", "BASE", "ENTRY", "SIZE", "VERSION"])

    modules = imm.getAllModules()

    for module in modules.values():
        table.add(0, [module.getName(), "%08x" %module.getBaseAddress(), "%08x" %module.getEntry(), "%08x" %module.getSize(), module.getVersion()])

    '''
    opcodes = imm.assemble("jmp esp\nret")
    for opcode in opcodes:
        imm.log("Assemble Func: "+hex(ord(opcode)))

    addresses = imm.search("\xff\xe4\xc3")
    for address in addresses:
        opcode = imm.disasm(address).getDisasm()
        imm.log("Disassmble Func: "+opcode)
    imm.updateLog()
    
    return "PyCommand Return!!"
