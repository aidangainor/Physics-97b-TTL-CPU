import intelhex
import os

class HexWriter:
    """Wrapper class for intelhex library that allows us to write to 8kb EEPROM"""

    write_ptr = 0
    default_byte = 255

    def __init__(self, fname):
        self.write_ptr = 0
        self.hex_writer = intelhex.IntelHex()
        self.fname = fname

    def fill_file(self):
        """Fill up file with 0xFFs
        """
        for i in range(self.write_ptr, 8192):
            self.hex_writer[i] = self.default_byte
        self.commit()

    def write_byte(self, a_byte):
        """Write a byte sequentially
        Input can be bitstring of 1s and 0s of length 8, an integer < 256, or hex value < 0xFF
        """
        value_to_write = a_byte
        if isinstance(a_byte, str):
            if len(a_byte) != 8:
                raise Exception("Bitstring must be length 8")
            # If we get string as input, convert string of 1s and 0s to integer
            # "11111111" --> 255
            value_to_write = int(a_byte, 2)
        self.hex_writer[self.write_ptr] = value_to_write
        self.write_ptr += 1


    def write_default_byte(self):
        """Write the default value, which is 0xFF
        """
        self.hex_writer[self.write_ptr] = self.default_byte
        self.write_ptr += 1

    def commit(self):
        """Write intel hex file to disk in the /hex/ output folder
        """
        self.hex_writer.write_hex_file(os.path.join("..", "..", "hex", self.fname))
