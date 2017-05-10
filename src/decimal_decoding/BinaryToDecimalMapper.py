"""Generate 3 hex files to be stored in EEPROMs for binary to decimal decoding
Each EEPROM stores 7 segment display encoding for digits 0 to 9 for each possible number from 0 to 255
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from HexWriter import HexWriter

seven_seg_encoding = {
    0 : "",
    1 : "",
    2 : "",
    3 : "",
    4 : "",
    5 : "",
    6 : "",
    7 : "",
    8 : "",
    9 : ""
}

# We need to generate 3 HEX files for each EEPROM connected in parallel to decode binary input into 7 segment display signals
prefix = "display" + os.path.sep + "bin_to_dec_"
file_writer_1s = HexWriter(prefix + "1s_place.hex")
file_writer_10s = HexWriter(prefix + "10s_place.hex")
file_writer_100s = HexWriter(prefix + "100s_place.hex")

for i in range(256):
    ones_place_digit = i%10
    tens_place_digit = int((i%100)/10.0)
    hundreds_place_digit = int(i/100.0)

    file_writer_1s.write_byte(seven_seg_encoding[ones_place_digit])
    file_writer_10s.write_byte(seven_seg_encoding[tens_place_digit])
    file_writer_100s.write_byte(seven_seg_encoding[hundreds_place_digit])

# Write all hex files to disk
for file_writer in all_file_writers:
    file_writer.commit()
