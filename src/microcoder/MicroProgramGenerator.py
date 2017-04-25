from MicroInstruction import MicroInstruction
from Instruction import Instruction
import InstructionMapper as IM
from HexWriter import HexWriter
from Encoders import DECIMAL_TO_BITSTRING

# We need to generate 4 HEX files for each EEPROM connected in parallel
file_writer_EE1 = HexWriter("rom1.hex")
file_writer_EE2 = HexWriter("rom2.hex")
file_writer_EE3 = HexWriter("rom3.hex")
file_writer_EE4 = HexWriter("rom4.hex")
all_file_writers = [file_writer_EE1, file_writer_EE2, file_writer_EE3, file_writer_EE4]

# Go through all possible EEPROM addresses
# Pin 0 to 3 = Feedback Resgister
# Pin 4 to 9 = Instruction register
# Pin 10 = Condition Met
# Pin 11 = Interrupt
# Pin 12 = Reset

# Write a micro instruction to all EEPROMs
def write_micro_instruction(u_inst, file_writers):
    # If there is no u_inst, write junk
    if u_inst is None:
        for file_writer in file_writers:
            file_writer.write_default_byte()
    else:
        for i in range(len(file_writers)):
            file_writer = file_writers[i]
            # Get flag layout for a specific EEPROM
            EEPROM_flag_layout = u_inst.get_EEPROM_flag_layout(i+1)
            byte_bitstring = u_inst.generate_EEPROM_bitstring(EEPROM_flag_layout)
            file_writer.write_byte(byte_bitstring)


# There are 512 instructions, in that there exist 64 possible opcodes with
for addr in range(512):
    if addr < 64: # For all vanilla instructions (no reset/interrupt/condition)
        if len(IM.asm_insts) > addr:
            asm_mnemonic = IM.asm_insts[addr] # Addr = opcode, get name of inst from opcode
            inst_obj = IM.asm_to_object[asm_mnemonic] # Get object that corresponds to name of inst
            for i in range(16):
                u_inst = inst_obj.get_u_instructions()[i]
                # If last micro instruction is used, set its next FB addr to 0
                if i == 15 and u_inst is not None:
                    inst_obj.set_next_u_inst_addr(DECIMAL_TO_BITSTRING[0])
                # Means we are at last u-inst, so loop back to 0 on next instruction
                elif u_inst is not None and i != 15:
                    if inst_obj.get_u_instructions()[i+1] is None:
                        u_inst.set_next_u_inst_addr(DECIMAL_TO_BITSTRING[0])
                # Go to next sequential u-inst
                elif u_inst is not None:
                    u_inst.set_next_u_inst_addr(DECIMAL_TO_BITSTRING[i+1])

                write_micro_instruction(u_inst, all_file_writers)
        else:
            # Means there is no op code corresponding to this address, just write all 11111....s
            write_micro_instruction(None, all_file_writers)
    elif addr < 128: # Addr 64 to 127 = for condition met
        for i in range(16):
            write_micro_instruction(None, all_file_writers)
    elif addr < 256: # Addr 128 - 255 = for interrupt
        for i in range(16):
            write_micro_instruction(None, all_file_writers)
    else: # Addr 256 - 511 = for reset
        for i in range(16):
            write_micro_instruction(None, all_file_writers)

# Write all hex files to disk
for file_writer in all_file_writers:
    file_writer.commit()
