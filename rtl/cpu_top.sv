module cpu_top(
    input logic clk,
    input logic reset,

    output logic [31:0] instruction_addr,
    output logic [31:0] instruction,
    output logic instr_valid,
    output logic debug_wb_en,
    output logic [4:0] debug_wb_rd,
    output logic [31:0] debug_wb_data
);


    cpu u_cpu(
        .clk(clk),
        .reset(reset),
        .instruction(instruction),
        .instruction_addr(instruction_addr),

        .instr_valid(instr_valid),
        .debug_wb_en(debug_wb_en),
        .debug_wb_rd(debug_wb_rd),
        .debug_wb_data(debug_wb_data)
    );


    logic [31:0] imem [0:63];

    initial begin
        $readmemh("program.hex", imem);
    end


    always_comb begin
        if (instruction_addr[31:8] == 0 && instruction_addr[1:0] == 0) begin
            instruction = imem[instruction_addr[7:2]];
        end 
        else begin
            instruction = 32'h00000013; // NOP
        end
    end
endmodule