import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock


IMM_I = 0
IMM_S = 1
IMM_B = 2


#helpers function 
async def build_instruct(op, rd, funct3, rs1, rs2, funct7):
    instruction = 0
    instruction |= (op & 0x7F)
    instruction |= (rd     & 0x1F) << 7
    instruction |= (funct3 & 0x07) << 12
    instruction |= (rs1    & 0x1F) << 15
    instruction |= (rs2    & 0x1F) << 20
    instruction |= (funct7 & 0x7F) << 25

    return instruction

async def build_i_type(immediate):
    imm_12bit = immediate & 0xFFF 

    instruction = imm_12bit << 20

    return instruction


def extend_sign(value, bits):
    signed = 1 << (bits-1)

    if value & signed:
        value -= 1 << bits

    return value & 0xFFFFFFFF



@cocotb.test()
async def test_i_type_positive(dut):

    imm = 5

    instruction = build_i_type(imm)

    dut.instruction.value = instruction
    dut.imm_type.value = IMM_I

    await Timer(1, unit="ns")

    assert int(dut.immediate.value) == 5


@cocotb.test()
async def test_i_type_negative(dut):

    imm = -4

    instruction = build_i_type(imm)

    dut.instruction.value = instruction
    dut.imm_type.value = IMM_I

    await Timer(1, unit="ns")

    expected = 0xFFFFFFFC

    assert int(dut.immediate.value) == expected

