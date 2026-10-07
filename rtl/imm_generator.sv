`timescale 1ns/1ps


typedef enum logic[1:0] {
    IMM_I =2'b00,
    IMM_S = 2'b01,
    IMM_B =2'b10
} imm_type_enum;


module imm_gen(
    input logic [31:0] instruction,
    input imm_type_enum imm_type,
    output logic [31:0] immediate
);






always_comb begin
    case(imm_type)
        IMM_I: begin
            immediate = {{20{instruction[31]}}, instruction[31:20]};
        end
        IMM_S: begin
            immediate =  {{20{instruction[31]}},instruction[31:25], instruction[11:7]};
        end

        IMM_B: begin
            immediate = {
                {19{instruction[31]}},
                instruction[31],
                instruction[7],
                instruction[30:25],
                instruction[11:8],
                1'b0
            };
        end

        default: begin
            immediate = 32'b0;
        end
    endcase
end

endmodule