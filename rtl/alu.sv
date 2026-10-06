module alu (
    input  logic [31:0] operand_a,
    input  logic [31:0] operand_b,
    input  logic [2:0]  alu_op,

    output logic [31:0] result,
    output logic        zero
);

localparam logic [2:0] ALU_ADD = 3'b000;
localparam logic [2:0] ALU_SUB = 3'b001;
localparam logic [2:0] ALU_AND = 3'b010;
localparam logic [2:0] ALU_OR  = 3'b011;
localparam logic [2:0] ALU_XOR = 3'b100;
localparam logic [2:0] ALU_SLT = 3'b101;

always_comb begin
    result = '0;

    case(alu_op)
        ALU_ADD: 
            result = operand_a + operand_b;
        ALU_SUB:
            result = operand_a - operand_b;
        ALU_AND:
            result = operand_a & operand_b;
        ALU_OR:
            result = operand_a | operand_b;
        ALU_XOR:
            result = operand_a ^ operand_b;
        ALU_SLT: begin
            if ($signed(operand_a) < $signed(operand_b))
                result = 1;
            else
                result = 0;
        end

    endcase
end
always_comb begin
    zero = (result==32'b0);
end
endmodule