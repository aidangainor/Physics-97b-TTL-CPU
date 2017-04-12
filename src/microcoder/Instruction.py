from MicroInstruction import MicroInstruction
from Decoders import *

class Instruction:
    """Corresponds to an instruction from the ISA level.
    It stores a sequence of up to 16 micro instructions needed to execute a programmer specified instruction.
    Default micro instructions are specified as class varialbes to deal with instruction fetch routine.
    """

    micro_instructions = [None] * 16 # An instruction consits of 16 micro instructions
                                     # Note that only a subset of these 16 micro instructions will actually be used

    def __init__(self):
        # Auto generate instruction fetch
        # Increment program counter first
        self.micro_instructions[14] = MicroInstruction(inc_PC="1", next_micro_inst=DECIMAL_TO_BITSTRING[15])
        # Output ROM/RAM and clock in instruction register
        self.micro_instructions[15] = MicroInstruction(device_onto_db=DEVICE_TO_BITSTRING["ROM/RAM"],
                                                       device_write_enable=DEVICE_TO_BITSTRING["IR"],
                                                       next_micro_inst=DECIMAL_TO_BITSTRING[0])

    def on_condition_met(self):
        pass

    def on_interrupt(self):
        # Interrupt logic works as
        pass

    def on_reset(self):
        pass
