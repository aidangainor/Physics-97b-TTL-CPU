"""This file stores constant hash maps for device decoding and decimal to binary ASCII string decoding"""

DECIMAL_TO_BITSTRING = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
                        "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]

DEVICE_TO_BITSTRING = { "ROM/RAM" : "0000" , "A" : "0000", "B" : "0000", "C" : "0000", "T" : "0000", "ALU" : "0000",
                        "IR" : "0000", "PC_LOW" : "0000", "PC_HIGH" : "0000", "I" : "0000", "J" : "0000"}
