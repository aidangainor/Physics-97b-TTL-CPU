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
        self.label_addrs = {}

    def assemble(self):
        first_pass = self.assemble_first_pass()
        second_pass = self.resolve_label_addrs(first_pass)
        self.write_hex(second_pass)

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

    def assemble_multiline_inst(self, stripped_line, parsed_lines):
        split_line = stripped_line.split(" ")
        if len(split_line) != 2:
            raise Exception("Opcode and operand must be on same line")
        parsed_lines.append(asm_to_opcode[split_line[0]])

        if stripped_line.startswith("JMP") or stripped_line.startswith("CALL"):
            operand_string = split_line[1]
            # Means label was provided as operand instead of number
            if operand_string.startswith("&"):
                label = operand_string[1:].strip()
                parsed_lines.append("&") # Append the & symbol to indicate this is label and will be resolved on 2nd pass
                parsed_lines.append(label) # Also append the label to be looked up later, this also adds two lines for operand which keeps us in order
            # Means we are dealing with literal number address
            else:
                operand_addr = self.convert_to_int16(operand_string)
                # Little endian byte order
                parsed_lines.append(operand_addr[0])
                parsed_lines.append(operand_addr[1])
        else:
            parsed_lines.append(self.convert_to_int8(split_line[1]))

    def resolve_label_addrs(self, parsed_lines):
        for i in range(len(parsed_lines)):
            if parsed_lines[i] == "&":
                resolved_addr = self.label_addrs[parsed_lines[i+1]]
                low_byte = resolved_addr & 255
                high_byte = resolved_addr >> 8
                parsed_lines[i] = low_byte
                parsed_lines[i+1] = high_byte
        return parsed_lines

    def assemble_first_pass(self):
        parsed_lines = []
        for src_line in self.lines:
            src_line = src_line.split(";")[0] # Remove comments
            stripped_line = src_line.strip().upper()

            # Check if this is label definition
            if stripped_line.endswith(":"):
                stripped_line = stripped_line.split(":")[0]
                label = stripped_line.strip()
                # On "first pass" we also store a table of all label addresses
                self.label_addrs[label] = len(parsed_lines)

            # Deal with where byte / 2 byte operand appear
            elif stripped_line.startswith("LOAD_BYTE") or stripped_line.startswith("JMP") or stripped_line.startswith("CALL"):
                self.assemble_multiline_inst(stripped_line, parsed_lines)

            elif "NOP" in stripped_line and len(stripped_line) > 3:
                num_nops = 1
                # We allow user to input a number after nop operation to indicate how many nops occur
                try:
                    num_ops = int(stripped_line[4:])
                except ValueError:
                    raise Exception("Multi-NOP must end with an integer")
                for i in range(num_ops):
                    parsed_lines.append(asm_to_opcode["NOP"])
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
