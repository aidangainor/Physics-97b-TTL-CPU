class MicroInstruction:
    """Each object of this class corresponds to a single "instruction" in the microprogram.
    In other words, it represents the 32 control signals active for a single clock cycle that dictate a CPU state transition from microarchitecture level.
    Class variables represent each control signal in default / inactive state, and programmer can generate
    """
    # The bit 0 is used for currently *unused* EEPROM I/O pins output
    NOT_USED = "1"

    # EEPROM 1 flags here
    enable_carry_in = "0"
    ALU_f0_f1 = "11"
    status_reg_load_select = "0" # 0 = load flags from ALU, 1 = load flags from DB
    device_onto_db = "1111" # 4 bit code for what devide (register, RAM, ...) is outputting onto DB? DB output is mutually exclusive
                            # PC low buffer CAN'T drive databus

    # EEPROM 2 flags here
    inc_PC = "0"
    inc_MAR = "0"
    device_onto_ab = "00" # What 16 bit register is active on address bus? 0 = PC, 1 = MAR
    device_write_enable = "1111" # 4 bit code for what device is enabled to clock in data bus value next clock cycle
                                 # PC low + high are always clocked in at once
                                 # Status register is special case write, as it can be written in tandem with other registers

    # EEPROM 3 flags here
    condition_code = "111" # Fed to 3 -> 8 decoder on what condition to check
    write_status_reg = "0"
    inv_A = "0" # Inverse values of A input

    # EEPROM 4 flags here
    clear_PC = "1"
    clear_MAR = "1"
    halt = "0" # This is NAND'ed with clock signal, so when halt = 1 the system clock will stop
    reset = "1" # This is OR'ed with reset pin signal, so we can't "escape" a reset once pin is unpressed
                # Harware reset is accomplished by setting 4 bit FB register reset pin low and EEPROM address 12 high
    next_micro_inst = "0000" # 4 bits of feedback of what micro instruction to execute next

    def __init__(self, **control_flags):
        for flag in control_flags:
            for char in control_flags[flag]:
                if char not in ["0", "1"]:
                    raise Exception("Control flag must be either an ASCII 0 or 1")
            setattr(self, flag, control_flags[flag])

    def pretty_print(self):
        return [self.generate_EEPROM_bitstring(x) for x in self.get_all_EEPROM_flags()]

    def generate_EEPROM_bitstring(self, flag_layout):
        """Create a byte string from a given "flag layout", like from EEPROM1 layout for example
        """
        bitstring = ""
        for flag in flag_layout:
            bitstring += flag
        if len(bitstring) != 8:
            raise Exception("Bit string must be length = 8")
        return bitstring

    def get_all_EEPROM_flags(self):
        # Flag layout for each EEPROM
        # This directly maps to hardware, for example ALU_f0 will emanate from the 1st EEPROM's 2nd I/O pin
        # Clear_PC will emanate from the 3rd EEPROM's 1st I/O pin
        # Order is like:     [7th bit, 6th bit, ..., 1st bit, 0th bit] for these arrays below
        EEPROM1_layout = [self.device_onto_db, self.status_reg_load_select, self.NOT_USED, self.NOT_USED, self.NOT_USED]
        EEPROM2_layout = [self.device_write_enable, self.device_onto_ab, self.inc_MAR, self.inc_PC]
        EEPROM3_layout = [self.enable_carry_in, self.ALU_f0_f1, self.write_status_reg, self.inv_A, self.condition_code]
        EEPROM4_layout = [self.next_micro_inst, self.halt, self.reset, self.clear_MAR, self.clear_PC]
        return [EEPROM1_layout, EEPROM2_layout, EEPROM3_layout, EEPROM4_layout]

    def get_EEPROM_flag_layout(self, EEPROM_num):
        """Grab a specific bit layout of control signals for an EEPROM.
        EEPROM's are indexed starting at 1.
        """
        if EEPROM_num > 4 or EEPROM_num < 1:
            raise Exception("EEPROM number must be between 1 and 4 inclusive")
        else:
            return self.get_all_EEPROM_flags()[EEPROM_num-1]

    def set_next_u_inst_addr(self, addr):
        """Set the 4 bit address to load into feedback register next clock cycle.
        """
        self.next_micro_inst = addr
