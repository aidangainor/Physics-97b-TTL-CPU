from MicroInstruction import MicroInstruction
from Decoders import *

class Instruction:
    """Corresponds to an instruction from the ISA level.
    It stores a sequence of up to 16 micro instructions needed to execute a programmer specified instruction.
    Default micro instructions are specified as class varialbes to deal with instruction fetch, reset, and interrupt routines.
    Micro instructions with "NoneType" in Python are unused, and will be written as 0xFF by EEPROM programmer.
    """

    inst_micro_instructions = [None] * 16 # An instruction consits of 16 micro instructions
                                          # Note that only a subset of these 16 micro instructions will actually be used

    rst_micro_instructions = [None] * 16
    # Rest program counter and MAR, then do instruction fetch
    rst_micro_instructions[0] = MicroInstruction(clear_PC="0", clear_MAR="0", reset="1", next_micro_inst=DECIMAL_TO_BITSTRING[1])
    # Output ROM/RAM and clock in instruction register
    rst_micro_instructions[1] = MicroInstruction(device_onto_db=DEVICE_TO_BITSTRING["ROM/RAM"],
                                                 device_write_enable=DEVICE_TO_BITSTRING["IR"],
                                                 next_micro_inst=DECIMAL_TO_BITSTRING[0],
                                                 reset="1")

    

    def __init__(self):
        # Auto generate instruction fetch, instruction fetch is always last 2 possible micro instructions of an instruction
        # Increment program counter first
        self.inst_micro_instructions[14] = MicroInstruction(inc_PC="1", next_micro_inst=DECIMAL_TO_BITSTRING[15])
        # Output ROM/RAM and clock in instruction register
        self.inst_micro_instructions[15] = MicroInstruction(device_onto_db=DEVICE_TO_BITSTRING["ROM/RAM"],
                                                            device_write_enable=DEVICE_TO_BITSTRING["IR"],
                                                            next_micro_inst=DECIMAL_TO_BITSTRING[0])
        self.instructions_added = 0

    def add_micro_instruction(self, u_inst, i=None):
        """Add a micro instruction to the instance of an instruction.
        If i = None, then internal counter is used to append u_inst.
        """
        if i is None:
            i = self.instructions_added
        self.inst_micro_instructions[i] = u_inst
        self.instructions_added += 1

    def on_condition_met(self):
        pass

    def on_interrupt(self):
        # Interrupt only occurs on next instruction cycle, this can be accomplished by checking if feedback register contains 4 0's
        pass

    def on_reset(self):
        return self.rst_micro_instructions
