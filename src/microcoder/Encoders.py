"""This file stores constant hash maps for device encoding and decimal to binary ASCII string encoding"""

ALU_OP_TO_BITSTRING = {"ADD" : "11", "OR" : "10", "XOR" : "01", "AND" : "00"}

CONDITION_TO_BITSTRING = {"UN" : "000", "Z" : "001", "NZ" : "010", "N" : "011", "NN" : "100", "C" : "101", "NC" : "110"}

DECIMAL_TO_BITSTRING = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
                        "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]

DB_DEVICE_TO_BITSTRING = { "A" : "0000", "B" : "0001", "C" : "0010", "T" : "0011", "ROM/RAM" : "0100" , "IR" : "0101",
                           "PC_LOW" : "0110", "PC_HIGH" : "0111", "I" : "1000", "J" : "1001", "ALU" : "1010", "FLAGS" : "1011", 
                           "OUTPUT" : "1100"}

AB_DEVICE_TO_BITSTRING = {"PC" : "00", "IJ" : "00", "SP" : "00", "EXT" : "00"}
