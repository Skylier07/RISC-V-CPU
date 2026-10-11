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
    logic[31:0] write_data;
    logic write_en;
    logic[31:0] read_data1;
    logic[31:0] read_data2;
    regfile u_regfile(
        .clk(clk),
        .reset(reset),
        .rs1(rs1),
        .rs2(rs2),
        .rd(rd),
        .write_data(write_data),
        .write_en(write_en),
        .read_data1(read_data1),
        .read_data2(read_data2)
    );
    
//     typedef enum logic[1:0] {
//     IMM_I =2'b00,
//     IMM_S = 2'b01,
//     IMM_B =2'b10
// } imm_type_enum;
//     imm_type_enum imm_type;
    logic[1:0] imm_type;

    logic [31:0] immediate;
    imm_gen u_imm_gen(
        .instruction(instruction),
        .imm_type(imm_type),
        .immediate(immediate)
    );

    logic [2:0] alu_op,
    logic alu_src_imm,
    logic reg_write,
    logic [2:0] imm_type,
    logic valid

    control_unit u_control_unit(
        .opcode(opcode),
        .funct3(funct3),
        .funct7(funct7),
        .alu_op(alu_op),
        .alu_src_imm(alu_src_imm),
        .reg_write(reg_write),
        .imm_type(imm_type),
        .valid(valid)
    );

    logic passed_data[31:0];
    assign passed_data = alu_src_imm ? immediate : read_data2;

    logic [31:0] result; 
    logic zero;
    alu u_alu(
        .operand_a(read_data1),
        .operand_b(passed_data),
        .alu_op(alu_op),
        .result(result),
        .zero(zero)
    )
endmodule
