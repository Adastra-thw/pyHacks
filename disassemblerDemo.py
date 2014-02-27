import pefile
import pydasm

def disassemble(file, num_bytes, att=False):	if att:		format = pydasm.FORMAT_ATT	else:
		format = pydasm.FORMAT_INTEL
		pe = pefile.PE(file)	entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint	ibase = pe.OPTIONAL_HEADER.ImageBase	data = pe.get_memory_mapped_image()[entry_point:entry_point + num_bytes]	offset=0	while offset < len(data):		instruction = pydasm.get_instruction(data[offset:], pydasm.MODE_32)		print "0x%08X"%offset, 		print pydasm.get_instruction_string(instruction,format, entry_point + ibase + offset)		if not instruction:			break		offset += instruction.length

if __name__=='__main__':
    disassemble('C:\\vulnserver\\vulnserver.exe', 20)