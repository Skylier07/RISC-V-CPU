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
# https://www.cs.cornell.edu/courses/cs3410/2026sp/rsrc/riscv-ref.html
def build_i_type(immediate):
    imm_12bit = immediate & 0xFFF 

    instruction = imm_12bit << 20

    return instruction


def build_s_type(immediate):
    imm_12bit = immediate & 0xFFF

    imm_11_5 = (imm_12bit >> 5) & 0x7F
    imm_4_0 = imm_12bit & 0x1F

    instruction = 0

    instruction|= imm_11_5 << 25
    instruction |= imm_4_0 << 7

    return instruction


def build_b_type(immediate):

    imm_13bit = immediate & 0x1FFF

    imm_12 = (imm_13bit >> 12) & 0x1
    imm_11 = (imm_13bit >> 11) & 0x1
    imm_10_5 = (imm_13bit >> 5) & 0x3F
    imm_4_1 = (imm_13bit>> 1) & 0xF

    instruction = 0
    instruction |= imm_12 << 31
    instruction |= imm_10_5 << 25
    instruction |= imm_4_1 << 8
    instruction |= imm_11 << 7

    return instruction


def extend_sign(value, bits=32):
    if value & (1 << (bits - 1)):
        value -= 1 << bits
    return value



@cocotb.test()
async def test_i_type_positive(dut):

    imm = 19

    instruction = build_i_type(imm)

    dut.instruction.value = instruction
    dut.imm_type.value = IMM_I

    await Timer(1, unit="ns")

    assert int(dut.immediate.value) == 19

    


@cocotb.test()
async def test_i_type_negative(dut):

    imm = -3

    instruction = build_i_type(imm)

    dut.instruction.value = instruction
    dut.imm_type.value = IMM_I

    await Timer(1, unit="ns")


    assert extend_sign(int(dut.immediate.value)) == -3

@cocotb.test()
async def test_s_type_positive(dut):

    imm = 21

    dut.instruction.value = build_s_type(imm)
    dut.imm_type.value = IMM_S

    await Timer(1, unit="ns")

    assert int(dut.immediate.value) == 21


@cocotb.test()
async def test_s_type_negative(dut):

    imm = -21

    dut.instruction.value = build_s_type(imm)
    dut.imm_type.value = IMM_S

    await Timer(1, unit="ns")

    assert extend_sign(int(dut.immediate.value)) == -21



@cocotb.test()
async def test_b_type_positive(dut):

    imm = 14

    dut.instruction.value = build_b_type(imm)
    dut.imm_type.value = IMM_B

    await Timer(1, unit="ns")

    assert int(dut.immediate.value) == 14


@cocotb.test()
async def test_b_type_negative(dut):

    imm = -8

    dut.instruction.value = build_b_type(imm)
    dut.imm_type.value = IMM_B

    await Timer(1, unit="ns")

    assert extend_sign(int(dut.immediate.value)) == -8

