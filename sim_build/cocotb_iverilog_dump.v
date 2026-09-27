module cocotb_iverilog_dump();
initial begin
    string dumpfile_path;    if ($value$plusargs("dumpfile_path=%s", dumpfile_path)) begin
        $dumpfile(dumpfile_path);
    end else begin
        $dumpfile("/mnt/c/Users/eason/OneDrive/Documents/Code/verilog-practice/RISC-V/RISC-V-CPU/sim_build/regfile.fst");
    end
    $dumpvars(0, regfile);
end
endmodule
