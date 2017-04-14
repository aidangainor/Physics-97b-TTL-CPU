from Instruction import Instruction
from MicroInstruction import MicroInstruction
from Decoders import *

# T register acts as a temporary register for all memory transfers
asm_insts = ["RESET", "HALT", "LOAD_IMD", "LOAD_IND", "STORE_IND", "ADD", "ADD_WC", "SUB", "AND", "OR", "XOR",
             "MOV A,T", "MOV B,T", "MOV C,T", "MOV I,T", "MOV J,T", "MOV T,J", "MOV T,I", "MOV T,C", "MOV T,B", "MOV T,A",
             "JMP_UN", "JMP_Z", "JMP_NZ", "JMP_C", "JMP_NC", "JMP_N", "JMP_NN", "CALL", "RETURN"]


# Map assembly mnemonic to integer opcode
asm_to_opcode = {}
opcode = 0
for inst in asm_insts:
    asm_to_opcode[inst] = opcode
    opcode += 1

# Map assembly mnemonic to instruction object
asm_to_object = {}

# Reset CPU (IJ, FB reg, PC)
reset = Instruction()
asm_to_object["RESET"] = reset
reset.add_u_instructions(Instruction.get_reset_sequence())

# Halt CPU clock
halt = Instruction()
asm_to_object["HALT"] = halt
halt.add_u_instruction(MicroInstruction(halt="1"))

# Load immediate byte
load_byte = Instruction()
asm_to_object["LOAD_IMD"] = load_byte
load_byte_u_insts = [MicroInstruction(inc_PC="1"),
                     MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                      device_write_enable=DB_DEVICE_TO_BITSTRING["T"],
                                      device_onto_ab=AB_DEVICE_TO_BITSTRING["PC"]])
load_byte.add_u_instructions(load_byte_u_insts)

# Load a byte indirectly from address stored in IJ pair
load_ind = Instruction()
load_ind.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                            device_write_enable=DB_DEVICE_TO_BITSTRING["T"],
                                            device_onto_ab=AB_DEVICE_TO_BITSTRING["IJ"]]))


# Store a byte indirectly from address stored in IJ pair
store_ind = Instruction()
store_ind.add_u_instruction(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["T"],
                                             device_write_enable=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                             device_onto_ab=AB_DEVICE_TO_BITSTRING["IJ"]]))

# Add, T = A + B
add = Instruction()
add.add_u_instruction(MicroInstruction(enable_carry_in="0", status_reg_load_select="0", inv_A="0",
                                       device_onto_db=DEVICE_TO_BITSTRING["ALU"], device_write_enable=DEVICE_TO_BITSTRING["T"]))


# Add with carry, T = A + B + carry
add_wc = Instruction()
add_wc.add_u_instruction(MicroInstruction(enable_carry_in="1", status_reg_load_select="0", inv_A="0",
                                          device_onto_db=DEVICE_TO_BITSTRING["ALU"], device_write_enable=DEVICE_TO_BITSTRING["T"]))

# Subtract, T = B - A
sub = Instruction()
sub.add_u_instruction(MicroInstruction(enable_carry_in="0", status_reg_load_select="0", inv_A="1",
                                       device_onto_db=DEVICE_TO_BITSTRING["ALU"], device_write_enable=DEVICE_TO_BITSTRING["T"]))

# inv_A will be OR'ed with carry in of ALU, thus giving us two's compliment representation of the contents in A register

# And, T = A bitwise AND B
and_ = Instruction()
and_.add_u_instruction(MicroInstruction(ALU_f0_f1=ALU_OP_TO_BITSTRING["AND"], status_reg_load_select="0", inv_A="0",
                                          device_onto_db=DEVICE_TO_BITSTRING["ALU"], device_write_enable=DEVICE_TO_BITSTRING["T"]))

# Or, T = A bitwise OR B
or_ = Instruction()

# Xor, T = A bitwise OR B
xor_ = Instruction()




asm_to_instruction = {
    "RESET" :
}
