from IMT2022523_IMT2022572_utils import *

# To run factorial, give input to instructions() as 0
# To run sorting, give input to instructions() as 1
instruction_memory, data_memory, register_file = instructions(1)

pc = 0
instruction_memory = convert_to_bin(instruction_memory)
if_pipe_reg = instruction_memory.copy()    
id_pipe_reg = []
ex_pipe_reg = []
mem_pipe_reg = []
wb_pipe_reg = []

clock_cycles = 1

hazard_detect = []
load_check = []
flush = False
stalled = False

while len(if_pipe_reg) or len(id_pipe_reg) or len(ex_pipe_reg) or len(mem_pipe_reg) or len(wb_pipe_reg):
    #if
    inst_info = IF_pipeline(if_pipe_reg)

    #wb
    WB_pipeline(wb_pipe_reg, register_file)

    #id
    id_info, hazard_detect, load_check, stalled = ID_pipeline(id_pipe_reg, hazard_detect, load_check, stalled)

    #ex
    ex_info, flush = EX_pipeline(ex_pipe_reg, wb_pipe_reg, mem_pipe_reg, register_file, flush)

    #mem
    mem_info = MEM_pipeline(mem_pipe_reg, register_file, data_memory)

    if len(wb_pipe_reg):
        wb_pipe_reg.pop(0)
    
    # insert NOP
    if stalled:
        if_pipe_reg.insert(0, 'NOP')

    # if not flush, each intruction progress to next clock cycle
    if not(flush):
        if inst_info != None:
            id_pipe_reg.append(inst_info) 

        if id_info != None and not(stalled):
            ex_pipe_reg.append(id_info) 

        if ex_info != None:
            mem_pipe_reg.append(ex_info) 
        
        if mem_info != None:
            wb_pipe_reg.append(mem_info) 
    else:

        # clear IF, ID, EX
        if_pipe_reg.clear()
        id_pipe_reg.clear()
        ex_pipe_reg.clear()
        hazard_detect = []        
        load_check = []

        if mem_info:
            wb_pipe_reg.append(mem_info)

        # get next PC in case of branch
        if_pipe_reg = instruction_memory[get_pc(ex_info, instruction_memory):]

        flush = False
        
    
    clock_cycles += 1

print('Time taken:', clock_cycles - 1, 'Clock cycles:', clock_cycles - 1)
print()

print('Register file:')
print(register_file)
print()

print('Data memory:')
print(data_memory)
