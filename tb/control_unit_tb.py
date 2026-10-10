import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock
ALU_ADD = 0b000
ALU_SUB = 0b001
ALU_AND = 0b010
ALU_OR  = 0b011
ALU_XOR = 0b100
ALU_SLT = 0b101

IMM_I = 0b000


async def control_input(
    dut,
    opcode,
    funct3,
    funct7,
    expected_alu_op,
    expected_alu_src_imm,
    expected_reg_write,
    expected_valid,
):


    dut.opcode.value = opcode
    dut.funct3.value = funct3
    dut.funct7.value = funct7


    await Timer(1, unit="ns")

    assert int(dut.alu_op.value) == expected_alu_op
    assert int(dut.alu_src_imm.value) == expected_alu_src_imm
    assert int(dut.reg_write.value) == expected_reg_write
    assert int(dut.valid.value) == expected_valid


@cocotb.test()
async def test_r_type(dut):
    await control_input( #ADD
        dut,
        opcode=0b0110011,
        funct3=0b000,
        funct7=0b0000000,
        expected_alu_op=ALU_ADD,
        expected_alu_src_imm=0,
        expected_reg_write=1,
        expected_valid=1,
    )

    await control_input( #SUB
        dut,
        opcode=0b0110011,
        funct3=0b000,
        funct7=0b0100000,
        expected_alu_op=ALU_SUB,
        expected_alu_src_imm=0,
        expected_reg_write=1,
        expected_valid=1,
    )

    await control_input( #AND
        dut,
        opcode=0b0110011,
        funct3=0b111,
        funct7=0b0000000,
        expected_alu_op=ALU_AND,
        expected_alu_src_imm=0,
        expected_reg_write=1,
        expected_valid=1,
    )

    await control_input( #OR
        dut,
        opcode=0b0110011,
        funct3=0b110,
        funct7=0b0000000,
        expected_alu_op=ALU_OR,
        expected_alu_src_imm=0,
        expected_reg_write=1,
        expected_valid=1,
    )


    await control_input(    # XOR
        dut,
        opcode=0b0110011,
        funct3=0b100,
        funct7=0b0000000,
        expected_alu_op=ALU_XOR,
        expected_alu_src_imm=0,
        expected_reg_write=1,
        expected_valid=1,
    )


    await control_input(   # SLT
        dut,
        opcode=0b0110011,
        funct3=0b010,
        funct7=0b0000000,
        expected_alu_op=ALU_SLT,
        expected_alu_src_imm=0,
        expected_reg_write=1,
        expected_valid=1,
    )