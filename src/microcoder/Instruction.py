from MicroInstruction import MicroInstruction
from Encoders import *

class Instruction:
    """Corresponds to an instruction from the ISA level.
    It stores a sequence of up to 16 micro instructions needed to execute a programmer specified instruction.
    Default micro instructions are specified as class varialbes to deal with instruction fetch, reset, and interrupt routines.
    Micro instructions with "NoneType" in Python are unused, and will be written as 0xFF by EEPROM programmer.
    """

    inst_micro_instructions = [None] * 16 # An instruction consits of 16 micro instructions
                                          # Note that only a subset of these 16 micro instructions will actually be used

    # Rest program counter and MAR, then do instruction fetch
    rst_micro_instructions = [MicroInstruction(clear_PC="0", clear_MAR="0", reset="1")]
    # Output ROM/RAM and clock in instruction register
    rst_micro_instructions.append(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                                   device_onto_ab=AB_DEVICE_TO_BITSTRING["PC"],
                                                   device_write_enable=DB_DEVICE_TO_BITSTRING["IR"],
                                                   reset="1"))

    # It is quite common to fetch two bytes from memory that are pointed to by PC + 1 and PC + 2
    # These values are loading into PC in little endian format, so lets store this sequence of u-insts
    fetch_new_pc_instructions = [MicroInstruction(inc_PC="1")]
    # Although we specify "PC_LOW" as our write target, the control unit actually writes into the PC low buffer so we can keep the original PC for next u-inst
    fetch_new_pc_instructions.append(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                                      device_onto_ab=AB_DEVICE_TO_BITSTRING["PC"],
                                                      device_write_enable=DB_DEVICE_TO_BITSTRING["PC_LOW"],
                                                      inc_PC="1"))
    # Now when we specify "PC_HIGH" as write target, the control unit actually specifies PC_HIGH to clock in data bus contents while PC_LOW clocks in PC buffer contents
    # This is done in parallel
    fetch_new_pc_instructions.append(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                                      device_onto_ab=AB_DEVICE_TO_BITSTRING["PC"],
                                                      device_write_enable=DB_DEVICE_TO_BITSTRING["PC_HIGH"]))

    # Auto generate instruction fetch, instruction fetch is always last 2 possible micro instructions of an instruction
    # Increment program counter first
    ir_fetch_instructions = [MicroInstruction(inc_PC="1", device_onto_ab=AB_DEVICE_TO_BITSTRING["PC"])]
    # Output ROM/RAM and clock in instruction register
    ir_fetch_instructions.append(MicroInstruction(device_onto_db=DB_DEVICE_TO_BITSTRING["ROM/RAM"],
                                                  device_onto_ab=AB_DEVICE_TO_BITSTRING["PC"],
                                                  device_write_enable=DB_DEVICE_TO_BITSTRING["IR"]))

    def __init__(self):
        self.instructions_added = 0

    def add_u_instruction(self, u_inst, i=None):
        """Add a micro instruction to the instance of an instruction.
        If i = None, then internal counter is used to append u_inst.
        """
        if i is None:
            i = self.instructions_added
        self.inst_micro_instructions[i] = u_inst
        self.instructions_added += 1

    def add_u_instructions(self, u_insts, i=None):
        """Add N micro instructions to instance of an instruction.
        If i = None, then internal counter is used to append u_insts.
        """
        for u_inst in u_insts:
            self.add_u_instruction(u_inst, i)

    def add_fetch_ir_sequence(self, i=None, inc_pc=True):
        """Append a sequence of micro instructions that swap the PC with 16 bit address operand stored in memory.
        Optional i paramater for specifying specific location of where to append PC fetch
        """
        self.add_u_instructions(self.ir_fetch_instructions, i)

    def add_fetch_pc_sequence(self, i=None):
        """Append a sequence of micro instructions that swap the PC with 16 bit address operand stored in memory.
        Optional i paramater for specifying specific location of where to append PC fetch
        """

    def generate_interrupt_sequence(self):
        """Return a constant interrupt handling routine (in microcode, of course!).
        Interrupt only occurs on next instruction cycle, this can be accomplished by checking if feedback register contains 4 0's
        """
        pass

    def get_u_instructions(self):
        """Return all micro instructions that constitute an instruction
        """
        return self.inst_micro_instructions

    def get_reset_sequence(self):
        """Returns a sequnce of u-insts that reset the CPU
        """
        return self.rst_micro_instructions
