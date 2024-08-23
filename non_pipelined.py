from IMT2022523_IMT2022572_utils import *

# To run factorial, give input to instructions() as 0
# To run sorting, give input to instructions() as 1
instruction_memory, data_memory, register_file = instructions(1)

pc = 0
instruction_memory = convert_to_bin(instruction_memory)
clock_cycles = 0

while pc//4 < len(instruction_memory):
    inst_info = {'inst': 0, 'controls': 0, 'rs': 0, 'rt': 0, 'a3': 0, 'sign_extend': 0, 'funct': 0, 'alu_result': 0, 'pc': pc, 'read_data':0}

    #if
    inst_info['inst'] = instruction_memory[pc//4]
    inst_info['funct'] = inst_info['inst'][26:]

    #id
    inst_info = ID(inst_info)

    #ex
    inst_info, branch = EX(inst_info, register_file)

    #mem
    inst_info = MEM(inst_info, register_file, data_memory)

    #wb
    WB(inst_info, register_file)

    pc = inst_info['pc']
    clock_cycles += 1

print('Time taken:', clock_cycles * 5, 'Clock cycles:', clock_cycles)
print()

print('Register file:')
print(register_file)
print()

print('Data memory:')
print(data_memory)
