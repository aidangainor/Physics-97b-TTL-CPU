import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Opcodes import asm_to_opcode, asm_insts
from HexWriter import HexWriter

class Assembler:
    def __init__(self, src_file):
        self.src_file = src_file
        with open(src_file) as f:
            self.lines = f.readlines()

    def assemble(self):
        output_array = self.parse_and_map()
        self.write_hex(output_array)

    def convert_to_int(self, string):
        base_string = string[-1]
        value_string = string[0:-1]
        base = None
        if base_string == "H":
            base = 16
        elif base_string == "D":
            base = 10
        elif base_string == "B":
            base = 2
        else:
            raise Exception("Number must end with H, D, or B to signify base")
        value = int(value_string, base)
        return value

    def convert_to_int8(self, string):
        value = self.convert_to_int(string)
        if value > 255 or value < 0:
            raise Exception("Operand must be in range 0 to 255 inclusive")
        return value

    def convert_to_int16(self, string):
        value = self.convert_to_int(string)
        if value > 65535 or value < 0:
            raise Exception("Operand must be in range 0 to 65535 inclusive")
        low_byte = value & 255
        high_byte = value >> 8
        return [low_byte, high_byte]

    def parse_and_map(self):
        parsed_lines = []
        for src_line in self.lines:
            src_line = src_line.split(";")[0] # Remove comments
            stripped_line = src_line.strip().upper()
            # Deal with where byte / 2 byte operand appear
            if "LOAD_BYTE" in stripped_line or "JMP" in stripped_line:
                split_line = stripped_line.split(" ")
                if len(split_line) != 2:
                    raise Exception("Opcode and operand must be on same line")
                parsed_lines.append(asm_to_opcode[split_line[0]])
                if "JMP" in stripped_line:
                    operand_addr = self.convert_to_int16(split_line[1])
                    # Little endian byte order
                    parsed_lines.append(operand_addr[0])
                    parsed_lines.append(operand_addr[1])
                else:
                    parsed_lines.append(self.convert_to_int8(split_line[1]))
            # We just ignore blank lines
            elif stripped_line != "":
                # If not opcode, lets just assume its data or fail miserably
                parsed_lines.append(asm_to_opcode[stripped_line])
        return parsed_lines

    def write_hex(self, parsed_lines):
        dest_location = self.src_file
        # Test if input file has extention
        split_location = dest_location.split(".")
        if len(split_location) > 1:
            dest_location = split_location[0]
        # Check for path sep and remove if found
        dest_location = dest_location.split(os.path.sep)[-1]
        dest_location = "programs" + os.path.sep + dest_location
        hr = HexWriter(dest_location + ".hex")
        for line in parsed_lines:
            hr.write_byte(line)
        hr.fill_file()


if __name__ == '__main__':
    source_file = sys.argv[1]

    asmblr = Assembler(source_file)
    asmblr.assemble()
