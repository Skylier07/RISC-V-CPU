`timescale 1ns/1ps

module program_counter (
    input logic clk,
    input logic reset,
    input logic[31:0] pc_next,
    output logic[31:0] pc
);

always_ff @(posedge clk) begin
    if(reset) begin
        pc <= 0;
    end
    else
        pc <= pc_next;
end

endmodule