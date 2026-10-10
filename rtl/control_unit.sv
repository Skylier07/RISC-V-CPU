
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

localparam logic [2:0] IMM_I = 3'b000;

always_comb begin
    alu_op      = ALU_ADD;
    alu_src_imm = 1'b0;
    reg_write   = 1'b0;
    imm_type    = IMM_I;
    valid       = 1'b0;

    case (opcode)

        // R-Type
        7'b0110011: begin
            case (funct3)
                3'b000: begin
                    case (funct7)
                        7'b0000000: begin
                            alu_op = ALU_ADD;
                            valid = 1'b1;
                        end
                        7'b0100000: begin
                            alu_op = ALU_SUB;
                            valid = 1'b1;
                        end
                    endcase
                end
                3'b111: begin
                    if (funct7 == 7'b0000000) begin
                        alu_op = ALU_AND;
                        valid = 1'b1;
                    end
                end

                3'b110: begin
                    if (funct7 == 7'b0000000) begin
                        alu_op = ALU_OR;
                        valid = 1'b1;
                    end
                end

                3'b100: begin
                    if (funct7 == 7'b0000000) begin
                        alu_op = ALU_XOR;
                        valid = 1'b1;
                    end
                end

                3'b010: begin
                    if (funct7 == 7'b0000000) begin
                        alu_op = ALU_SLT;
                        valid = 1'b1;
                    end
                end
            endcase
        end

        // I-Type
        7'b0010011: begin
            case (funct3)
                3'b000: begin
                    alu_op = ALU_ADD;
                    valid = 1'b1;
                end
                3'b111: begin
                    alu_op = ALU_AND;
                    valid = 1'b1;
                end
                3'b110: begin
                    alu_op = ALU_OR;
                    valid = 1'b1;
                end
                3'b100: begin
                    alu_op = ALU_XOR;
                    valid = 1'b1;
                end
                3'b010: begin
                    alu_op = ALU_SLT;
                    valid = 1'b1;
                end
            endcase
            alu_src_imm = 1'b1; 
        end
        default: ;
    endcase
    reg_write = valid;
end
endmodule
