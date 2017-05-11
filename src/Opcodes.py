# T register acts as a temporary register for all memory transfers
# Order dictates opcode = eg asm_inst[op_code] = instruction
# For example, RESET is opcode 0 in decimal and MOV T,FLAGS is opcode 17 in decimal


asm_insts = ["RESET", "HALT", "LOAD_BYTE", "LOAD_IND", "STORE_IND", "ADD", "ADD_WC", "SUB", "AND", "OR", "XOR",
             "MOV A,T", "MOV B,T", "MOV C,T", "MOV I,T", "MOV J,T", "MOV FLAGS,T", "MOV T,FLAGS", "MOV T,J", "MOV T,I", "MOV T,C", "MOV T,B", "MOV T,A",
             "JMP_UN", "JMP_Z", "JMP_NZ", "JMP_C", "JMP_NC", "JMP_N", "JMP_NN", "CALL", "RETURN", "NOP", "OUTPUT"]

"""
RESET : reset program counter and memory address register (I and J) and fetch very first instruction in ROM

HALT : freeze CPU by not incrementing program counter and causing feedback register to loop to itself

LOAD_BYTE a_byte : load a_byte immediately to the T register

LOAD_IND : load a byte indirectly to the T register pointed by memory address register (I and J)

STORE_IND : store the value in T register to memory address pointed by I and J

ADD : add values A and B and store in T register ; affects the C, Z, and N flags

ADD_WC : same as ADD except we also input carry bit ; affects the C, Z, and N flags

SUB : subtract A from B and store in T, in other words T = B - A ; affects the C, Z, and N flags

AND : bitwise AND registers A and B, store in T ; affects the C, Z, and N flags

OR : bitwise OR registers A and B, store in T ; affects the C, Z, and N flags

XOR : bitwise XOR registers A and B, store in T ; affects the C, Z, and N flags

MOV reg1, reg2 : copy reg2 to reg1, in other words reg1 = reg2

JMP memory_addr : jump to the instruction located at some 16 bit memory address, JMP_UN is an unconditional jump and JMP_NC is jump if carry bit not set
                  JMP_N is jump if negative bit is set and JMP_NZ is jump if zero bit is not set, meaning the result of ALU operation was not zero

CALL memory_addr : to be implemented w/ stack pointer

RETURN : to be implemented w/ stack pointer

NOP : do nothing for 5 clock cycles
"""

# Map assembly mnemonic to integer opcode
asm_to_opcode = {}
opcode = 0
for inst in asm_insts:
    asm_to_opcode[inst] = opcode
    opcode += 1
