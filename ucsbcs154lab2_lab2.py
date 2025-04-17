import pyrtl

# === Inputs and Outputs ===
instr = pyrtl.Input(bitwidth=32, name='instr')

# === Register File ===
rf = pyrtl.MemBlock(bitwidth=32, addrwidth=5, name='rf')

# === Decoding Fields ===
opcode = instr[26:32]
rs = instr[21:26]
rt = instr[16:21]
rd = instr[11:16]
shamt = instr[6:11]
funct = instr[0:6]

# === Reading from Register File ===
read_data1 = rf[rs]
read_data2 = rf[rt]

# === ALU Operations ===
alu_out = pyrtl.WireVector(bitwidth=32, name='alu_out') 

with pyrtl.conditional_assignment:
    with funct == 0b100000:   # ADD
        alu_out |= read_data1 + read_data2
    with funct == 0b100010:   # SUB
        alu_out |= read_data1 - read_data2
    with funct == 0b100100:   # AND
        alu_out |= read_data1 & read_data2
    with funct == 0b100101:   # OR
        alu_out |= read_data1 | read_data2
    with funct == 0b100110:   # XOR
        alu_out |= read_data1 ^ read_data2
    with funct == 0b000000:   # SLL
        alu_out |= pyrtl.shift_left_logical(read_data2, shamt)
    with funct == 0b000010:   # SRL
        alu_out |= pyrtl.shift_right_logical(read_data2, shamt)
    with funct == 0b000011:   # SRA
        alu_out |= pyrtl.shift_right_arithmetic(read_data2, shamt)
    with funct == 0b101010:   # SLT
        alu_out |= pyrtl.signed_lt(read_data1, read_data2)

# === Write Back ===
rf[rd] <<= alu_out  

