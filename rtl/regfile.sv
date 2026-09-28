`timescale 1ns/1ps
module regfile(
    input logic clk,
    input logic reset,
    input logic[4:0] rs1,
    input logic[4:0] rs2,
    input logic[4:0] rd,
    input logic[31:0] write_data,
    input logic write_en,
    output logic[31:0] read_data1,
    output logic[31:0] read_data2

);
    logic[31:0] registers[0:31];
    int i;
always_comb begin
    if(rs1 ==0)
        read_data1 = 0;
    else
        read_data1 = registers[rs1];
    if(rs2==0)
        read_data2=0;
    else
        read_data2 = registers[rs2];
end

always_ff @(posedge clk) begin
    if(reset) begin
        for(i = 0; i<=31; i= i+1) begin
            registers[i] <= '0;
        end
    end

    else if(write_en && (rd!=0)) begin
        registers[rd] <= write_data;
    end


    
end

endmodule   