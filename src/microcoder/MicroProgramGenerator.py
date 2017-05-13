from MicroInstruction import MicroInstruction
from Instruction import Instruction
import InstructionMapper as IM
from Encoders import DECIMAL_TO_BITSTRING, CONDITION_TO_BITSTRING
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from HexWriter import HexWriter

# We need to generate 4 HEX files for each EEPROM connected in parallel
prefix = "control_unit" + os.path.sep + "micro_insts_rom"
file_writer_EE1 = HexWriter(prefix + "1.hex")
file_writer_EE2 = HexWriter(prefix + "2.hex")
file_writer_EE3 = HexWriter(prefix + "3.hex")
file_writer_EE4 = HexWriter(prefix + "4.hex")
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

# Take in instruction object and index for current micro instruction
# Will set the FB register for next micro instruction
def set_fb_reg_addr(inst_obj, i):
    u_inst = inst_obj.get_u_instructions()[i]
    # If last micro instruction is used, set its next FB addr to 0
    if i == 15 and u_inst is not None:
        u_inst.set_next_u_inst_addr(DECIMAL_TO_BITSTRING[0])
    # Means we are at last u-inst, so loop back to 0 on next instruction
    elif u_inst is not None and i != 15:
        if inst_obj.get_u_instructions()[i+1] is None:
            u_inst.set_next_u_inst_addr(DECIMAL_TO_BITSTRING[0])
        else:
            # We have another micro instruction after this one, so make sure we execute that micro instruction next
            u_inst.set_next_u_inst_addr(DECIMAL_TO_BITSTRING[i+1])

# There are 512 instructions, each with 16 possible state transitions (micro instructions), and only 64 possible opcodes
# The reason behind only 64 opcodes is that we must reserve 3 lines for JMP, interrupt, and reset handling
for addr in range(512):
    if addr < 64: # For all vanilla instructions (no reset/interrupt/condition)
        if len(IM.asm_insts) > addr:
            asm_mnemonic = IM.asm_insts[addr] # Addr = opcode, get name of inst from opcode
            print("\t\t   Instruction: " + asm_mnemonic)
            print("\t\t   Opcode: " + str(hex(addr)))
            print ("\t   EEPROM 1     EEPROM 2    EEPROM 3    EEPROM 4")
            inst_obj = IM.asm_to_object[asm_mnemonic] # Get object that corresponds to name of inst
            for i in range(16): # Go through 16 possible microinstructions
                u_inst = inst_obj.get_u_instructions()[i]
                set_fb_reg_addr(inst_obj, i)
                write_micro_instruction(u_inst, all_file_writers)
                if u_inst is not None:
                    print("u-inst " + str(i) + ": " + str(u_inst.pretty_print()))
            print()
        else:
            # Means there is no op code corresponding to this address, just write all 11111....s
            for i in range(16):
                write_micro_instruction(None, all_file_writers)

    elif addr < 128: # Addr 64 to 127 = for condition met
        jmp_condition_met_inst = Instruction()
        # Dummy u-instruction
        jmp_condition_met_inst.add_u_instruction(MicroInstruction(inc_PC="1"))
        # Fetch the new program counter
        jmp_condition_met_inst.add_fetch_pc_sequence()
        # Get instruction new program counter value points to
        jmp_condition_met_inst.add_fetch_ir_sequence()

        if len(IM.asm_insts) > addr-64: # Subtract 64 to take into account the condition met signal being on
            asm_mnemonic = IM.asm_insts[addr-64]
            if asm_mnemonic.startswith("JMP"):
                for i in range(16):
                    set_fb_reg_addr(jmp_condition_met_inst, i)
                    u_inst = jmp_condition_met_inst.get_u_instructions()[i]
                    write_micro_instruction(u_inst, all_file_writers)
            else:
                for i in range(16):
                    write_micro_instruction(None, all_file_writers)
        else:
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
