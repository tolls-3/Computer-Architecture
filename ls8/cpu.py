"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        MDR = self.ram[MAR]
        return MDR

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:

        program = [
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b10000010,  # LDI R1,9
            0b00000001,
            0b00001001,
            0b10100010,  # MUL R0,R1
            0b00000000,
            0b00000001,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        # filename = sys.argv[1]
        # try:
        #     address = 0
        #     with open(filename) as f:
        #         for line in f:
        #             line = line.split('#')[0]
        #             command = line.strip()
        #             if command == '':
        #                 continue
        #             instruction = int(command, 2)
        #             self.ram_write(address, instruction)

        #             address += 1
        # except FileNotFoundError:
        #     print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
        #     sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def prn(self, operand_a):
        print(operand_a)

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        running = True

        while running:
            IR = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)

            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                self.ldi(operand_a, operand_b)
                self.pc += 3

            if IR == PRN:
                self.prn(self.reg[operand_a])
                self.pc += 2

            if IR == HLT:
                running = False

            if IR == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
