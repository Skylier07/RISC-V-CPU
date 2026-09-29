module imm_gen(
    input logic [31:0] instruction,
    input logic [2:0] type,
    output logic [31:0] imemediate
);

endmodule

typedef enum logic[1:0] {
    IDLE, 
    START,
    DATA,
    STOP
} state_t;

state_t state;