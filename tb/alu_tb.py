import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock

ALU_ADD = 0
ALU_SUB =1
ALU_AND = 2
ALU_OR=3
ALU_XOR = 4
ALU_SLT = 5

@cocotb.test()
async def test_ADD(dut):
    dut.operand_a.value = 5
    dut.operand_b.value = 10
    dut.alu_op.value = ALU_ADD 

    await ReadOnly()
    assert(dut.result.value == 15)
    assert(dut.zero.value == 0)


@cocotb.test()
async def test_SUB(dut):
    dut.operand_a.value = 5
    dut.operand_b.value = 10
    dut.alu_op.value = ALU_SUB

    await ReadOnly()
    assert(dut.result.value == -5)
    assert(dut.zero.value == 0)

@cocotb.test()
async def test_AND(dut):
    dut.operand_a.value = 1
    dut.operand_b.value = 1
    dut.alu_op.value = ALU_AND

    await ReadOnly()
    assert(dut.result.value == 1)
    # assert(dut.zero.value == 0)

    await Timer(1, unit="ns")

    dut.operand_a.value = 1
    dut.operand_b.value = 0
    dut.alu_op.value = ALU_AND

    await ReadOnly()
    assert(dut.result.value == 0)
    # assert(dut.zero.value == 0)


@cocotb.test()
async def test_OR(dut):
    dut.operand_a.value = 1
    dut.operand_b.value = 1
    dut.alu_op.value = ALU_OR

    await ReadOnly()
    assert(dut.result.value == 1)
    # assert(dut.zero.value == 0)

    await Timer(1, unit="ns")

    dut.operand_a.value = 1
    dut.operand_b.value = 0
    dut.alu_op.value = ALU_OR

    await ReadOnly()
    assert(dut.result.value == 1)
    # assert(dut.zero.value == 0)

@cocotb.test()
async def test_XOR(dut):
    dut.operand_a.value = 1
    dut.operand_b.value = 1
    dut.alu_op.value = ALU_XOR

    await ReadOnly()
    assert(dut.result.value == 0)
    # assert(dut.zero.value == 0)
    await Timer(1, unit="ns")

    dut.operand_a.value = 0
    dut.operand_b.value = 0
    dut.alu_op.value = ALU_XOR

    await ReadOnly()
    assert(dut.result.value == 0)
    # assert(dut.zero.value == 0)
    await Timer(1, unit="ns")

    dut.operand_a.value = 1
    dut.operand_b.value = 0
    dut.alu_op.value = ALU_XOR

    await ReadOnly()
    assert(dut.result.value == 1)
    # assert(dut.zero.value == 0)

@cocotb.test()
async def test_SLT(dut):
    dut.operand_a.value = 5
    dut.operand_b.value = 10
    dut.alu_op.value = ALU_SLT

    await ReadOnly()
    assert(dut.result.value == 1)

    await Timer(1, unit="ns")

    dut.operand_a.value = 5
    dut.operand_b.value = -10
    dut.alu_op.value = ALU_SLT

    await ReadOnly()
    assert(dut.result.value == 0)

    await Timer(1, unit="ns")


    dut.operand_a.value = -5
    dut.operand_b.value = -10
    dut.alu_op.value = ALU_SLT

    await ReadOnly()
    assert(dut.result.value == 0)

    await Timer(1, unit="ns")


    dut.operand_a.value = 100
    dut.operand_b.value = 7
    dut.alu_op.value = ALU_SLT

    await ReadOnly()
    assert(dut.result.value == 0)

    await Timer(1, unit="ns")
