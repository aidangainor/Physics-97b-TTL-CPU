# T register acts as a temporary register for all memory transfers
asm_insts = ["RESET", "HALT", "LOAD_BYTE", "LOAD_IND", "STORE_IND", "ADD", "ADD_WC", "SUB", "AND", "OR", "XOR",
             "MOV A,T", "MOV B,T", "MOV C,T", "MOV I,T", "MOV J,T", "MOV FLAGS,T", "MOV T,FLAGS", "MOV T,J", "MOV T,I", "MOV T,C", "MOV T,B", "MOV T,A",
             "JMP_UN", "JMP_Z", "JMP_NZ", "JMP_C", "JMP_NC", "JMP_N", "JMP_NN", "CALL", "RETURN"]


# Map assembly mnemonic to integer opcode
asm_to_opcode = {}
opcode = 0
for inst in asm_insts:
    asm_to_opcode[inst] = opcode
    opcode += 1
