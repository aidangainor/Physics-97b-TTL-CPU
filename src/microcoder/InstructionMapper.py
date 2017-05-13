from Instruction import Instruction
from MicroInstruction import MicroInstruction
from Encoders import *

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Opcodes import asm_insts

# Map assembly mnemonic to instruction object
asm_to_object = {}

for inst in asm_insts:
    inst_obj = Instruction()
    # Reset CPU (IJ, FB reg, PC)
    if inst == "RESET":
        inst_obj.add_u_instructions(inst_obj.get_reset_sequence())
    # Halt CPU by not incrementing program counter and feeding back into self (don't do instruction fetch!)
    elif inst == "HALT":
        inst_obj.add_u_instruction(MicroInstruction(inc_PC="0"))
    # Load immediate byte
    elif inst == "LOAD_BYTE":
        load_byte_u_insts = [MicroInstruction(inc_PC="1", device_onto_ab=AB_DEVICE_TO_BITSTRING["PC"]),
                             MicroInstruction(inc_PC="0", device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                              device_write_enable=DB_DEVICE_TO_BITSTRING["T"],
                                              device_onto_ab=AB_DEVICE_TO_BITSTRING["PC"]),
                             MicroInstruction(inc_PC="1", device_onto_ab=AB_DEVICE_TO_BITSTRING["PC"])]
        inst_obj.add_u_instructions(load_byte_u_insts)
    # Load a byte indirectly from address stored in IJ pair
    elif inst == "LOAD_IND":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["IJ"]))
    # Store a byte indirectly from address stored in IJ pair
    elif inst == "STORE_IND":
        # Write occurs during overlap of write enable and chip select going low
        # We first allow chip select to go low (done when IJ is enabled onto address bus)
        # Then write occurs during 2nd cycle
        # Data must be valid for a small period after both write enable and chip select go high, so let T still output onto data bus
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"], inc_PC="0",
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["IJ"]))
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"], inc_PC="0",
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["IJ"]))
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"], inc_PC="1", device_onto_ab=AB_DEVICE_TO_BITSTRING["IJ"]))
    # Add, T = A + B
    elif inst == "ADD":
        inst_obj.add_u_instruction(MicroInstruction(enable_carry_in="0", status_reg_load_select="0", inv_A="0", write_status_reg="1",
                                                    device_onto_db=DB_DEVICE_TO_BITSTRING["ALU"], device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    # Add with carry, T = A + B + carry
    elif inst == "ADD_WC":
        inst_obj.add_u_instruction(MicroInstruction(enable_carry_in="1", status_reg_load_select="0", inv_A="0", write_status_reg="1",
                                                    device_onto_db=DB_DEVICE_TO_BITSTRING["ALU"], device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    # Subtract, T = B - A
    elif inst == "SUB":
        inst_obj.add_u_instruction(MicroInstruction(enable_carry_in="0", status_reg_load_select="0", inv_A="1", write_status_reg="1",
                                                    device_onto_db=DB_DEVICE_TO_BITSTRING["ALU"], device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
        # inv_A will be OR'ed with carry in of ALU, thus giving us two's compliment representation of the contents in A register
    # And, T = A bitwise AND B
    elif inst == "AND":
        inst_obj.add_u_instruction(MicroInstruction(ALU_f0_f1=ALU_OP_TO_BITSTRING["AND"], status_reg_load_select="0", inv_A="0", write_status_reg="1",
                                                    device_onto_db=DB_DEVICE_TO_BITSTRING["ALU"], device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    # Or, T = A bitwise OR B
    elif inst == "OR":
        inst_obj.add_u_instruction(MicroInstruction(ALU_f0_f1=ALU_OP_TO_BITSTRING["OR"], status_reg_load_select="0", inv_A="0", write_status_reg="1",
                                                    device_onto_db=DB_DEVICE_TO_BITSTRING["ALU"], device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    # Xor, T = A bitwise XOR B
    elif inst == "XOR":
        inst_obj.add_u_instruction(MicroInstruction(ALU_f0_f1=ALU_OP_TO_BITSTRING["XOR"], status_reg_load_select="0", inv_A="0", write_status_reg="1",
                                                    device_onto_db=DB_DEVICE_TO_BITSTRING["ALU"], device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    # MOV, copy T contents into A
    elif inst == "MOV A,T":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["A"]))
    elif inst == "MOV B,T":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["B"]))
    elif inst == "MOV C,T":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["C"]))
    elif inst == "MOV I,T":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["I"]))
    elif inst == "MOV J,T":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["J"]))
    # MOV, copy T contents into processor status word (flags register)
    elif inst == "MOV FLAGS,T":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                                    status_reg_load_select="1",
                                                    write_status_reg="1"))
    elif inst == "MOV T,FLAGS":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["FLAGS"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    elif inst == "MOV T,J":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["J"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    elif inst == "MOV T,I":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["I"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    # MOV, copy C register contents into T (temp register)
    elif inst == "MOV T,C":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["C"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    elif inst == "MOV T,B":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["B"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    elif inst == "MOV T,A":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["A"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["T"]))
    elif inst == "JMP_UN":
        inst_obj.add_u_instruction(MicroInstruction(condition_code=CONDITION_TO_BITSTRING["UN"], write_condition_bit="0"))
        inst_obj.add_skip_two_bytes_u_insts() # A jump instruction takes up 3 bytes in memory, so we must skip them when condition not met
    elif inst == "JMP_Z":
        inst_obj.add_u_instruction(MicroInstruction(condition_code=CONDITION_TO_BITSTRING["Z"], write_condition_bit="0"))
        inst_obj.add_skip_two_bytes_u_insts()
    elif inst == "JMP_NZ":
        inst_obj.add_u_instruction(MicroInstruction(condition_code=CONDITION_TO_BITSTRING["NZ"], write_condition_bit="0"))
        inst_obj.add_skip_two_bytes_u_insts()
    elif inst == "JMP_C":
        inst_obj.add_u_instruction(MicroInstruction(condition_code=CONDITION_TO_BITSTRING["C"], write_condition_bit="0"))
        inst_obj.add_skip_two_bytes_u_insts()
    elif inst == "JMP_NC":
        inst_obj.add_u_instruction(MicroInstruction(condition_code=CONDITION_TO_BITSTRING["NC"], write_condition_bit="0"))
        inst_obj.add_skip_two_bytes_u_insts()
    elif inst == "JMP_N":
        inst_obj.add_u_instruction(MicroInstruction(condition_code=CONDITION_TO_BITSTRING["N"], write_condition_bit="0"))
        inst_obj.add_skip_two_bytes_u_insts()
    elif inst == "JMP_NN":
        inst_obj.add_u_instruction(MicroInstruction(condition_code=CONDITION_TO_BITSTRING["NN"], write_condition_bit="0"))
        inst_obj.add_skip_two_bytes_u_insts()
    elif inst == "CALL":
        # Save high 8 bits of program counter onto stack
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"], inc_PC="0",
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"]))
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["PC_HIGH"], inc_PC="0",
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"]))
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"], inc_PC="0"))
        inst_obj.add_u_instruction(MicroInstruction(inc_PC="0", inc_SP="1")) # increment stack pointer

        # Now save low 8 bits
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"], inc_PC="0",
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"]))
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["PC_LOW"], inc_PC="0",
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"]))
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"], inc_PC="0"))
        inst_obj.add_u_instruction(MicroInstruction(inc_PC="1", inc_SP="1")) # increment stack pointer and PC

        # Swap out program counter with operand
        inst_obj.add_fetch_pc_sequence()
    elif inst == "RETURN":
        inst_obj.add_u_instruction(MicroInstruction(inc_PC="0", dec_SP="0")) # decrement stack pointer
        # program counter low is on top of stack
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"], inc_PC="0",
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["PC_LOW"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"]))
        inst_obj.add_u_instruction(MicroInstruction(inc_PC="0", dec_SP="0")) # decrement stack pointer
        # now program counter high is on top of stack
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"], inc_PC="0",
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["PC_HIGH"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"]))
        # increment program counter once
        inst_obj.add_u_instruction(MicroInstruction(inc_PC="1"))
        # now increment it twice, we must do this because program counter stored on stack was location of call operator in memory.
        # to get to new instruction: new_pc = old_pc + 3
        inst_obj.add_skip_two_bytes_u_insts()
    elif inst == "NOP":
        inst_obj.add_def_instruction()
    elif inst == "OUTPUT":
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["OUTPUT"]))
    elif inst == "INC IJ":
        inst_obj.add_u_instruction(MicroInstruction(inc_MAR="1"))
    elif inst == "PUSH":
        # Follow exactly what we do in STORE_IND instruction except stack pointer drives address bus
        # Increment stack pointer and program counter by 1 before next instruction fetch
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"], inc_PC="0",
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"]))
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"], inc_PC="0",
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"]))
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"], inc_PC="0"))
        inst_obj.add_u_instruction(MicroInstruction(inc_PC="1", inc_SP="1")) # increment stack pointer
    elif inst == "POP":
        inst_obj.add_u_instruction(MicroInstruction(inc_PC="0", dec_SP="0")) # decrement stack pointer
        inst_obj.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                                    device_write_enable=DB_DEVICE_TO_BITSTRING["T"],
                                                    device_onto_ab=AB_DEVICE_TO_BITSTRING["SP"]))

    # Instruction fetch routine is done completely in microcode
    # Instruction fetch routine is special for reset and halt instruction
    if inst != "RESET" and inst != "HALT":
        inst_obj.add_fetch_ir_sequence()
    asm_to_object[inst] = inst_obj
