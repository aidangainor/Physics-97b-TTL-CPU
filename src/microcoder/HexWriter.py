import intelhex

class HexWriter:
    write_ptr = 0
    default_byte = 255

    def __init__(self, fname):
        self.write_ptr = 0
        self.hex_writer = intelhex.IntelHex()
        self.fname = fname

    def fill_file(self):
        for i in range(self.write_ptr, 8192):
            self.hex_writer[i] = self.default_byte
        self.commit()

    def write_byte(self, bitstring):
        if len(bitstring) != 8:
            raise Exception("Bitstring must be length 8")
        else:
            # Convert string of 1s and 0s to integer
            # "11111111" --> 255
            self.hex_writer[self.write_ptr] = int(bitstring, 2)
            self.write_ptr += 1


    def write_default_byte(self):
        self.hex_writer[self.write_ptr] = self.default_byte
        self.write_ptr += 1


    def commit(self):
        self.hex_writer.write_hex_file(self.fname)


h = HexWriter("test.hex")
h.fill_file()
h.commit()
