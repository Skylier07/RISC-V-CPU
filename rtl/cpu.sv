module cpu(
    input logic clk,
    input logic reset,
    input logic [31:0] instruction, 
    
    output logic [31:0] instruction_addr,
    output logic instr_valid, 
    output logic debug_wb_en,
    output logic [4:0] debug_wb_rd,
    output logic [31:0] debug_wb_data
);



    logic [31:0] current_pc;
    logic [31:0] pc_next;

    assign pc_next = current_pc + 32'd4;

    program_counter u_pc (
        .clk(clk),
        .reset(reset),
        .pc_next(pc_next),
        .pc(current_pc)
    );

    assign instruction_addr = current_pc;

    logic[4:0] rs1;
    logic[4:0] rs2;
    logic[4:0] rd;
    logic[6:0] opcode;
    logic[2:0] funct3;
    logic[6:0] funct7;

    instr_decode u_instr_decdode(
        .instruction(instruction),
        .rs1(rs1),
        .rs2(rs2),
        .rd(rd),
        .opcode(opcode),
        .funct3(funct3),
        .funct7(funct7)
    );

endmodule
