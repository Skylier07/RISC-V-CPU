`timescale 1ns/1ps

module control_unit (
    input  logic [6:0] opcode,
    input  logic [2:0] funct3,
    input  logic [6:0] funct7,

    output logic [2:0] alu_op,
    output logic       alu_src_imm,
    output logic       reg_write,
    output logic [2:0] imm_type,
    output logic       valid
);


localparam logic [2:0] ALU_ADD = 3'b000;
localparam logic [2:0] ALU_SUB = 3'b001;
localparam logic [2:0] ALU_AND = 3'b010;
localparam logic [2:0] ALU_OR  = 3'b011;
localparam logic [2:0] ALU_XOR = 3'b100;
localparam logic [2:0] ALU_SLT = 3'b101;
localparam logic [2:0] IMM_I = 0'b000;



always_comb begin
    alu_op      = ALU_ADD;
    alu_src_imm = 1'b0;
    reg_write   = 1'b0;
    imm_type    = IMM_I;
    valid       = 1'b0;

    case(opcode)
        7'b0110011: //R-Type
            case(funct3)
                3'b000: 
                    case(funct7)
                        7'b0000000:
                            alu_op = ALU_ADD;
                            alu_src_imm = 1'b0;
                            reg_write = 1'b1;
                            imm_type = IMM_I; 
                            valid = 1'b1;
                        7'b0100000:
                            alu_op = ALU_SUB;
                            alu_src_imm = 1'b0;
                            reg_write = 1'b1;
                            imm_type = IMM_I; 
                            valid = 1'b1;
                    endcase
                3'b111:                                                  
                    alu_op = ALU_AND;
                    alu_src_imm = 1'b0;
                    reg_write = 1'b1;
                    imm_type = IMM_I; 
                    valid = 1'b1;    
                3'b110:                                                  
                    alu_op = ALU_OR;
                    alu_src_imm = 1'b0;
                    reg_write = 1'b1;
                    imm_type = IMM_I; 
                    valid = 1'b1;  
                3'b110:                                                  
                    alu_op = ALU_XOR;
                    alu_src_imm = 1'b0;
                    reg_write = 1'b1;
                    imm_type = IMM_I; 
                    valid = 1'b1;   
                3'b010:                                                  
                    alu_op = ALU_SLT;
                    alu_src_imm = 1'b0;
                    reg_write = 1'b1;
                    imm_type = IMM_I; 
                    valid = 1'b1;   
                3'b011:                                                  
                    alu_op = ALU_SLT;
                    alu_src_imm = 1'b0;
                    reg_write = 1'b1;
                    imm_type = IMM_I; 
                    valid = 1'b1;    
            endcase   
        7'b0010011: //I-Type
            case(funct3)
                3'b000: 
                    case(funct7)
                        7'b0000000:
                            alu_op = ALU_ADDI;
                            alu_src_imm = 1'b1;
                            reg_write = 1'b1;
                            imm_type = IMM_I; 
                            valid = 1'b1;
                        7'b0100000:
                            alu_op = ALU_SUBI;
                            alu_src_imm = 1'b1;
                            reg_write = 1'b1;
                            imm_type = IMM_I; 
                            valid = 1'b1;
                    endcase
                3'b111:                                                  
                    alu_op = ALU_ANDI;
                    alu_src_imm = 1'b1;
                    reg_write = 1'b1;
                    imm_type = IMM_I; 
                    valid = 1'b1;    
                3'b110:                                                  
                    alu_op = ALU_ORI;
                    alu_src_imm = 1'b1;
                    reg_write = 1'b1;
                    imm_type = IMM_I; 
                    valid = 1'b1;  
                3'b110:                                                  
                    alu_op = ALU_XORI;
                    alu_src_imm = 1'b1;
                    reg_write = 1'b1;
                    imm_type = IMM_I; 
                    valid = 1'b1;   
                3'b010:                                                  
                    alu_op = ALU_SLTI;
                    alu_src_imm = 1'b1;
                    reg_write = 1'b1;
                    imm_type = IMM_I; 
                    valid = 1'b1;   
                3'b011:                                                  
                    alu_op = ALU_SLTI;
                    alu_src_imm = 1'b1;
                    reg_write = 1'b1;
                    imm_type = IMM_I; 
                    valid = 1'b1;    
            endcase                                                                                  
    endcase
end
endmodule
