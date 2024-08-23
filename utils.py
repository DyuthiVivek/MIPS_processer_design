# register numbers
register_numbers = {0: '$zero', 1: '$at', 2: '$v0', 3: '$v1', 4: '$a0', 5: '$a1', 6: '$a2', 7: '$a3', 8: '$t0', 9: '$t1', 10: '$t2', 11: '$t3', 12: '$t4', 13: '$t5', 14: '$t6', 15: '$t7', 16: '$s0', 17: '$s1', 18: '$s2', 19: '$s3', 20: '$s4', 21: '$s5', 22: '$s6', 23: '$s7', 24: '$t8', 25: '$t9', 26: '$k0', 27: '$k1', 28: '$gp', 29: '$sp', 30: '$fp', 31: '$ra'}

# r format function codes
r_funct = {'add': '100000', 'sub': '100010', 'sll': '000000', 'move':'100001', 'slt': '101010'}

# immediate format opcodes
imm_opcodes = {'addi': '001000', 'lw': '100011','sw': '101011', 'beq':'000100'}

# jump format opcodes
j_opcodes = {'j':'000010', 'jal': '000011'}

# control lines
keys = ['regDst', 'ALUSrc', 'memToReg', 'regWrite', 'memRead', 'memWrite', 'branch', 'ALUOp', 'JMP']
r_format_vals = [1, 0, 0, 1, 0, 0 , 0, '10', 0]
lw_vals = [0, 1, 1, 1, 1, 0, 0, '00', 0]
sw_vals = [0, 1, 0, 0, 0, 1, 0, '00', 0]
beq_vals = [0, 0, 0, 0, 0, 0, 1, '01', 0]
jmp_vals = [0, 0, 0, 0, 0, 0, 1, '00', 1]
addi = [0, 1, 0, 1, 0, 0, 0, '00', 0]

# fetch machine code
def instructions(inp = 0):

    if inp == 0:
        with open("factorial_machine_code.txt","r") as f:
            instruction_memory = [x.strip('\n') for x in f.readlines()]

        data_memory = {}

        register_file = {'$0': 0, '$zero': 0, '$at': 0, '$v0': 0, '$v1': 0, '$a0': 0, '$a1': 0, '$a2': 0,
                        '$a3': 0, '$t0': 5, '$t1': 0, '$t2': 0, '$t3': 0, '$t4': 0, '$t5': 0,
                        '$t6': 0, '$t7': 0, '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0, '$s4': 0,
                        '$s5': 0, '$s6': 0, '$s7': 0, '$t8': 0, '$t9': 0, '$k0': 0, '$k1': 0,
                        '$gp': 0, '$sp': 0, '$fp': 0, '$ra': 0
                    }

        return instruction_memory, data_memory, register_file
    
    data_memory = {'286444':'-9', '286448': '2', '286452': '32', '286456': '-1'}
    register_file = {'$0': 0, '$zero': 0, '$at': 0, '$v0': 0, '$v1': 0, '$a0': 0, '$a1': 0, '$a2': 0,
                    '$a3': 0, '$t0': 0, '$t1': 4, '$t2': 0, '$t3': 286444, '$t4': 0, '$t5': 0,
                    '$t6': 0, '$t7': 0, '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0, '$s4': 0,
                    '$s5': 0, '$s6': 0, '$s7': 0, '$t8': 0, '$t9': 0, '$k0': 0, '$k1': 0,
                    '$gp': 0, '$sp': 0, '$fp': 0, '$ra': 0
                }
    
    with open("sorting_machine_code.txt","r") as f:
        instruction_memory = [x.strip('\n') for x in f.readlines()]
    return instruction_memory, data_memory, register_file

# Instruction decode
def ID(inst_info):
    inst = inst_info['inst']
    op = inst[:6]

    # get control lines based on opcode of the instruction
    if op == '000000':
        controls = dict(zip(keys, r_format_vals))

    elif op in imm_opcodes.values():
        if op == imm_opcodes['lw']:
            controls = dict(zip(keys, lw_vals))
        elif op == imm_opcodes['sw']:
            controls = dict(zip(keys, sw_vals))
        elif op == imm_opcodes['beq']:
            controls = dict(zip(keys, beq_vals))
        elif op == imm_opcodes['addi']:
            controls = dict(zip(keys, addi))

    elif op in j_opcodes.values():
        controls = dict(zip(keys, jmp_vals))

    # get rs, rt, a3
    rs = int(inst[6:11], 2)
    rt = int(inst[11:16], 2)

    a3 = int(inst[16:21], 2) if controls['regDst'] else rt
    
    # handle negative immediate value
    if inst[16]=='1':
        sign_extend = (int(''.join(str(int(not(int(x)))) for x in inst[16:]), 2) + 1)*(-1)
    else:
        sign_extend = int(inst[16:], 2)

    inst_info['controls'] = controls
    inst_info['rs'] = rs
    inst_info['rt'] = rt
    inst_info['a3'] = a3
    inst_info['sign_extend'] = sign_extend

    return inst_info
 
def ALUControl(funct, ALUOp):

    # generate alu control based on ALUOp
    funct_dic = {'100000' : '010', '100010' : '011', '100100' : '000', '100101' : '001', '101010' : '100','100001' : '010','000000':'111'}
    if ALUOp == '00':
        return '010'
    elif ALUOp == '01':
        return '011'
    elif ALUOp =='10':
        return funct_dic[funct]
    elif ALUOp =='11':
        return '111'

# get the next pc
def determine_next_pc(zero, controls, sign_extend, pc):

    # check branch condition
    branch = (zero == 0) and controls['branch']
    pc += 4

    # if branch, add immediate value * 4 to pc
    if branch:
        pc += sign_extend * 4
    return pc, branch 

# EX stage
def EX(inst_info, register_file, forwardA = '00', forwardB = '00'):

    # if no forwarding, take values from the registers
    if forwardA == '00':
        rs = register_file[register_numbers[inst_info['rs']]]
    else:
        rs = inst_info['rs']
    
    if forwardB == '00':
        rt = register_file[register_numbers[inst_info['rt']]]
    else:
        rt = inst_info['rt']

    sign_extend = inst_info['sign_extend']
    controls = inst_info['controls']
    pc = inst_info['pc']

    # ALU operands
    alu1 = int(rs)
    alu2 = int(sign_extend) if controls['ALUSrc'] else int(rt)

    aluc = ALUControl(inst_info['funct'], controls['ALUOp'])
    
    # perform operation based on ALU control
    if aluc == '010':
        alu_result = alu1 + alu2
    elif aluc == '011':
        alu_result = alu1 - alu2
    elif aluc == '000':
        alu_result = alu1 & alu2
    elif aluc == '001':
        alu_result = alu1 | alu2
    elif aluc == '100':
        alu_result = int(alu1 < alu2)
    elif aluc == '111':
        alu_result = alu2*(int(inst_info['inst'][21:26],2))*2

    inst_info['alu_result'] = alu_result
    inst_info['pc'], branch = determine_next_pc(int(alu1) - int(alu2), controls, sign_extend, pc)
    return inst_info, branch

# MEM stage
def MEM(inst_info, register_file, data_memory, forwardA = '00', forwardB = '00'):
    controls = inst_info['controls']
    alu_result = inst_info['alu_result']

    rt = inst_info['rt']

    # if no forwarding, take value from register
    if forwardA == '00' and forwardB == '00':
        rt = register_file[register_numbers[rt]]

    write_data = rt
    read_data = ''

    # read/write data according to control signals
    if controls['memWrite']:
        data_memory[str(alu_result)] = write_data
    elif controls['memRead']:
        read_data = data_memory[str(alu_result)]

    inst_info['read_data'] = read_data
    return inst_info

    
# WB stage
def WB(inst_info, register_file): 
    controls = inst_info['controls']
    a3 = inst_info['a3']
    alu_result = inst_info['alu_result']

    read_data = inst_info['read_data']

    # get the correct write based on memToReg
    write_data = read_data if controls['memToReg'] else alu_result 
    if controls['regWrite']:
        # write to reg
        register_file[register_numbers[a3]] = write_data


# convert to binary
def convert_to_bin(instruction_memory):
    for i in range(len(instruction_memory)):
        instruction_memory[i] = (bin(int(instruction_memory[i][2:], 16))[2:]).zfill(32)
    return instruction_memory

def get_pc(inst_info, instruction_memory):
    if inst_info['inst'][16]=='1':
        sign_extend = (int(''.join(str(int(not(int(x)))) for x in inst_info['inst'][16:]), 2) + 1)*(-1)
    else:
        sign_extend = int(inst_info['inst'][16:], 2)

    return instruction_memory.index(inst_info['inst']) + sign_extend + 1

def IF_pipeline(if_pipe_reg):
    if len(if_pipe_reg) and if_pipe_reg[0] != 'NOP':

        # fetch the instruction
        inst_info = {'inst': 0, 'controls': 0, 'rs': 0, 'rt': 0, 'a3': 0, 'sign_extend': 0, 'funct': 0, 'alu_result': 0, 'pc': 0, 'read_data':0, 'forwardA': '00', 'forwardB': '00', 'hazard_num_A' : 0, 'hazard_num_B' : 0}
        inst_info['inst'] = if_pipe_reg.pop(0)
        inst_info['funct'] = inst_info['inst'][26:]
    
    elif len(if_pipe_reg) and 'NOP' == if_pipe_reg[0]:
        if_pipe_reg.pop(0)
        inst_info = 'NOP'
    else:
        inst_info = None
    
    # return output of IF stage
    return inst_info

def WB_pipeline(wb_pipe_reg, register_file):

    # if the queue to writeback is not empty, call WB
    if len(wb_pipe_reg) and wb_pipe_reg[0] != 'NOP':
        WB(wb_pipe_reg[0], register_file)

def ID_pipeline(id_pipe_reg, hazard_detect, load_check, stalled):
    if len(id_pipe_reg) and id_pipe_reg[0] != 'NOP':
        id_info = ID(id_pipe_reg.pop(0))

        # if not stalled
        if not(stalled):

            # if rs is hazard, control signals = forwardA
            if id_info['rs'] in hazard_detect:

                # load hazard, implement stalling
                if load_check[hazard_detect.index(id_info['rs'])]:
                    id_info['forwardA'] = '01'
                    stalled = True
                    id_pipe_reg.insert(0, id_info)

                # RAW hazard
                else:
                    id_info['forwardA'] = '10'
                id_info['hazard_num_A'] = hazard_detect.index(id_info['rs']) + 1

            # if rt is hazard, control signals = forwardB
            if id_info['rt'] in hazard_detect:

                # load hazard
                if load_check[hazard_detect.index(id_info['rt'])]:
                        id_info['forwardB'] = '01'
                        stalled = True
                        id_pipe_reg.insert(0, id_info)
                
                # RAW hazard
                else:
                    id_info['forwardB'] = '10'
                id_info['hazard_num_B'] = hazard_detect.index(id_info['rt']) + 1
            
            # the instruction is branch, the reg will not cause a hazard
            if id_info['controls']['branch']:
                hazard_detect.append('')
            else:
                # append the register that will cause a hazard
                hazard_detect.append(id_info['a3'])

            # check if it is a load
            load_check.append(id_info['controls']['memRead'])

            # remove instructions that do not cause a hazard anymore
            if len(hazard_detect) > 2:
                hazard_detect.pop(0)
                load_check.pop(0)
            
            if len(load_check) == 2 and load_check[1] and load_check[0]:
                hazard_detect.pop(0)
                load_check.pop(0)

        # if intruction stalled in the same stage, do nothing
        else:
            stalled = False
    
    elif len(id_pipe_reg) and 'NOP' == id_pipe_reg[0]:
        id_pipe_reg.pop(0)
        id_info = 'NOP'
    else:
        id_info = None

    
    return id_info, hazard_detect, load_check, stalled


def EX_pipeline(ex_pipe_reg, wb_pipe_reg, mem_pipe_reg, register_file, flush):
    if len(ex_pipe_reg) and ex_pipe_reg[0] != 'NOP':
        ex_inps = ex_pipe_reg.pop(0)

        # forward from mem or wb pipeline regs 
        # based on which stage the hazard instruction has reached
        # rs if forwardA
        if ex_inps['forwardA'] == '10':
            if ex_inps['hazard_num_A'] == 1:
                ex_inps['rs'] = wb_pipe_reg[0]['alu_result']
            else:
                ex_inps['rs'] = mem_pipe_reg[0]['alu_result']

        # rt if forwardB
        if ex_inps['forwardB'] == '10':
            if ex_inps['hazard_num_B'] == 1:
                ex_inps['rt'] = wb_pipe_reg[0]['alu_result']
            else:
                ex_inps['rt'] = mem_pipe_reg[0]['alu_result']
        
        # load hazard, forward read data from mem here
        if ex_inps['forwardA'] == '01':
            ex_inps['rs'] = int(wb_pipe_reg[0]['read_data'])
        if ex_inps['forwardB'] == '01':
            ex_inps['rt'] = int(wb_pipe_reg[0]['read_data'])

        
        ex_info, branch = EX(ex_inps, register_file, forwardA = ex_inps['forwardA'], forwardB = ex_inps['forwardB'])

        # flush
        if branch:
            flush = True

    elif len(ex_pipe_reg) and 'NOP' == ex_pipe_reg[0]:
        ex_pipe_reg.pop(0)
        ex_info = 'NOP'
    else:
        ex_info = None
    
    return ex_info, flush

def MEM_pipeline(mem_pipe_reg, register_file, data_memory):

    # if the queue to MEM stage is not empty, call MEM
    if len(mem_pipe_reg) and mem_pipe_reg[0] != 'NOP':
        mem_inps = mem_pipe_reg.pop(0)
        mem_info = MEM(mem_inps, register_file, data_memory, mem_inps['forwardA'], mem_inps['forwardB'])
    elif len(mem_pipe_reg) and 'NOP' == mem_pipe_reg[0]:
        mem_pipe_reg.pop(0)
        mem_info = 'NOP'
    else:
        mem_info = None
    return mem_info

