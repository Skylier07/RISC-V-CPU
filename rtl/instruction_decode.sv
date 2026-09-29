module instr_decode(
    input logic [31:0] instruction, 
    output logic[4:0] rs1,
    output logic[4:0] rs2,
    output logic[4:0] rd,
    output logic[6:0] opcode,
    output logic[2:0] funct3,
    output logic[6:0] funct7
);
// 0-6: opcode
//7-11: rd
// 12-14: funct3
// 15-19: rs1
// 20:24: rs2
// 25-31: funct7

always_comb begin
    opcode = instruction[6:0];
    rd = instruction[11:7];
    funct3 = instruction[14:12];
    rs1 = instruction[19:15];
    rs2 = instruction[24:20];
    funct7 = instruction[31:25];


end
endmodule