# MIPS_processer_design

In this project, a Python-based simulation of a MIPS (Microprocessor without Interlocked Pipeline Stages) processor is developed to understand and analyze the differences between non-pipelined and pipelined processor architectures. The MIPS architecture is a popular RISC (Reduced Instruction Set Computing) design, known for its simplicity and efficiency, making it an ideal candidate for educational and research purposes.


## Non-pipelined MIPS processor

This model executes each instruction sequentially, completing one instruction fully before starting the next. It follows a five-stage instruction cycle—which are processed one at a time. 

1. Instruction Fetch (IF) - Read in the machine code of instructions one after the oher
2. Instruction Decode (ID) - Decode the instruction
3. Execute (EX) - Execute it in an ALU
4. Memory Access (MEM) - Perform memory access 
5. Writeback (WB) - Writeback to register file 

This is repeated for all instructions in a non-pipelined fashion. This design, while straightforward, can lead to inefficiencies due to idle stages waiting for the completion of previous instructions.

## Pipelined MIPS processor design 

In pipelining, in each clock cycle, all the stages perform simultaneously (but for different instructions). Once one stage for an instruction is completed, it is added to the respective pipeline register. In the next clock cycle, the instruction reaches the next stage.

1. The inputs and outputs remain same as in the non-pipelined scenario.
2. The IF, ID, EX, MEM and WB will occur in a pipelined fashion, that is an instruction is fetched every cycle, and does not wait until the previous instruction is completed.
4. Hazards are handled in the program.
5. RAW and Load hazards are resolved using forwarding and stalls. Forwarding is done in case of dependencies. For stalling, a bubble is introduced in the pipeline by pushing a ‘NOP’ instruction.
6. Control hazards are resolved using pipeline flushes. 

The pipelined design improves performance by filling the pipeline with instructions, ensuring that each stage of the processor is actively working on different instructions during each clock cycle. 

## Conclusion

By comparing these two architectures, the simulation aims to demonstrate the efficiency gains of pipelining in processor design and explore the complexities involved in handling different types of hazards. The project also includes performance metrics, such as the number of clock cycles required to execute a program, to quantitatively analyze the benefits of pipelining.

Observed that the pipelined processor executed the programs faster than the non-pipelined processor.