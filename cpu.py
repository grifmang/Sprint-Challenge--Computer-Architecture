import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.halted = False
        self.sp = 7
        self.reg[self.sp] = 0xF4
        self.E = None


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val

    def add(self):
        return self.alu("ADD", self.ram_read(self.pc+1), self.ram_read(self.pc+2))

    def halt(self):
        self.halted = True

    def print_stuff(self):
        print(f'Value: {self.reg[self.ram_read(self.pc+1)]}')

    def mult(self):
        return self.alu("MUL", self.ram_read(self.pc+1), self.ram_read(self.pc+2))

    def comp(self):
        return self.alu("CMP", self.ram_read(self.pc+1), self.ram_read(self.pc+2))

    def reg_write(self):
        self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)

    def jump(self):
        self.pc = self.reg[self.ram_read(self.pc + 1)]

    def jne(self):
        if self.E == 0:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else:
            self.pc += 2

    def jeq(self):
        if self.E == 1:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else:
            self.pc += 2

    def push(self):
        self.reg[self.sp] -= 1
        reg_a = self.ram_read(self.pc+1)
        self.ram[self.reg[self.sp]] = self.reg[reg_a]

    def pop(self):
        if self.reg[self.sp] == 0xF4:
            return 'Stack is empty'
        reg_a = self.ram_read(self.pc+1)
        self.reg[reg_a] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def load(self, file):
        """Load a program into memory."""

        address = 0

        with open(file) as program:
            for instruction in program:
                try:
                    instruction = int(instruction.split('#')[0][:-1], 2)
                    self.ram[address] = instruction
                    address += 1
                except:
                    continue

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
            else:
                self.E = 0
        #elif op == "SUB": etc
        elif op == 'MUL':
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
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            instruction = self.ram[self.pc]
            # print(instruction)
            # print(self.ram)
            # print(self.reg)
            # print(self.trace())

            function_lookup = {
                1: {'func': self.halt, 'move': 0},
                162: {'func': self.mult, 'move': 3},
                130: {'func': self.reg_write, 'move': 3},
                69: {'func': self.push, 'move': 2},
                70: {'func': self.pop, 'move': 2},
                71: {'func': self.print_stuff, 'move': 2},
                167: {'func': self.comp, 'move': 3},
                84: {'func': self.jump, 'move': 0},
                85: {'func': self.jeq, 'move': 0},
                86: {'func': self.jne, 'move': 0}

            }

            if instruction in function_lookup:
                function_lookup[instruction]['func']()
                self.pc += function_lookup[instruction]['move']
            else:
                print(f'unknown instruction {instruction} at address {self.pc}')
                break