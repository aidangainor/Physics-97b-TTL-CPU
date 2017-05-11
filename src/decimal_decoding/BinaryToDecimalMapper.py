"""Generate 3 hex files to be stored in EEPROMs for binary to decimal decoding
Each EEPROM stores 7 segment display encoding for digits 0 to 9 for each possible number from 0 to 255
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from HexWriter import HexWriter

# I/O pin 0 = A, pin 1 = B, pin 2 = C, pin 3 = D, pin 4 = E, pin 5 = F, pin 6 = G, pin 7 = no connection
# We are using 3 LTS-312AHR 7 seg displays which are common anode, meaning we light LED outputting 0 volts
seven_seg_encoding = {
        # gfedcba
    0 : "11000000",
    1 : "11111001",
    2 : "10100100",
    3 : "10110000",
    4 : "10011001",
    5 : "10010010",
    6 : "10000010",
    7 : "11111000",
    8 : "10000000",
    9 : "10011000"
}

# We need to generate 3 HEX files for each EEPROM connected in parallel to decode binary input into 7 segment display signals
prefix = "display" + os.path.sep + "bin_to_dec_"
file_writer_1s = HexWriter(prefix + "1s_place.hex")
file_writer_10s = HexWriter(prefix + "10s_place.hex")
file_writer_100s = HexWriter(prefix + "100s_place.hex")
all_file_writers = [file_writer_1s, file_writer_10s, file_writer_100s]

for i in range(256):
    ones_place_digit = i%10
    tens_place_digit = int((i%100)/10.0)
    hundreds_place_digit = int(i/100.0)

    file_writer_1s.write_byte(seven_seg_encoding[ones_place_digit])
    file_writer_10s.write_byte(seven_seg_encoding[tens_place_digit])
    file_writer_100s.write_byte(seven_seg_encoding[hundreds_place_digit])

# Write all hex files to disk
for file_writer in all_file_writers:
    file_writer.fill_file()
