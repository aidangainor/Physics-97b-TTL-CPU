from MicroInstruction import MicroInstruction
from Instruction import Instruction
import InstructionMapper as IM
from HexWriter import HexWriter

# We need to generate 4 HEX files for each EEPROM connected in parallel
file_writer_EE1 = HexWriter()
file_writer_EE2 = HexWriter()
file_writer_EE3 = HexWriter()
file_writer_EE4 = HexWriter()

# Go through all possible EEPROM addresses
# Pin 0 to 3 = Feedback Resgister
# Pin 4 to 9 = Instruction register
# Pin 10 = Condition Met
# Pin 11 = Interrupt
# Pin 12 = Reset

# There are 512 instructions, in that there exist 64 possible opcodes with
for addr in range(512):
    if addr < 64: # For all vanilla instructions (no reset/interrupt/condition)
        if len(IM.asm_insts) > addr:
            asm_mnemonic = IM.asm_insts[addr] # Addr = opcode, get name of inst from opcode
            inst_obj = IM.asm_to_object[asm_mnemonic] # Get object that corresponds to name of inst
            for i in range(16):
                u_inst = inst_obj.get_u_instructions[i]
                # If last micro instruction is used, set its next FB addr to 0
                if i == 15 and u_inst != None:
                    inst_obj.set_next_u_inst_addr(DECIMAL_TO_BITSTRING[0])
                # If there is no u_inst, write junk
                elif u_inst is None:
                    file_writer.write_default_byte()
                # Means we are at last u-inst, so loop back to 0 on next instruction
                elif inst_obj.get_u_instructions[i+1] is None:
                    u_inst.set_next_u_inst_addr(DECIMAL_TO_BITSTRING[0])
                else:
                    u_inst.set_next_u_inst_addr(DECIMAL_TO_BITSTRING[i+1])
        else:
            # Means there is no op code corresponding to this address, just write all 11111....s
            for i in range(16):
                file_writer.write_default_byte()
    elif addr < 128: # Addr 64 to 127 = for condition met
        pass
    elif addr < 256: # Addr 128 - 255 = for interrupt
        pass
    else: # Addr 256 - 511 = for reset
        pass
