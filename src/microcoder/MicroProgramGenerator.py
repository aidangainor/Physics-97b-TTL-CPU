from MicroInstruction import MicroInstruction
from Instruction import Instruction
import InstructionMapper as IM
from HexWriter import HexWriter

file_writer = HexWriter()

# Go through all possible EEPROM addresses
# Pin 0 to 3 = Feedback Resgister
# Pin 4 to 9 = Instruction register
# Pin 10 = Condition Met
# Pin 11 = Interrupt
# Pin 12 = Reset

# There are 512 instructions, in that there exist 64 possible opcodes with
for addr in range(512):
    if addr < 64: # For all vanilla instructions (no reset/interrupt/condition)
        pass
    elif addr < 128: # For condition met
        pass
    elif addr < 256: # For interrupt
        pass
    else: # For reset
        pass
