import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock

import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock

from cpu_tb_helper import *


@cocotb.test()
async def test_reset(dut):
    Clock(dut.clk, 10, unit="ns").start()
    await reset_dut(dut)

    assert(await get_current_address(dut) == 0)
    


# Program Counter Test
@cocotb.test()
async def test_program_counter(dut):
    await setup_dut(dut)
    assert(await get_current_address(dut) == 0)
    for i in range(1, 100):
        await RisingEdge(dut.clk)
        assert(await get_current_address(dut)== i*4)


# Instruction decode Test
@cocotb.test()
async def test_instruction_decode(dut):
    for _ in range(1000):
        opcode = random.randint(0, 127)
        rd = random.randint(0, 31)
        funct3 = random.randint(0, 7)
        rs1 = random.randint(0, 31)
        rs2 = random.randint(0, 31)
        funct7 = random.randint(0, 127)

        instruction = await build_instruct(
            opcode, rd, funct3, rs1, rs2, funct7
        )

        dut.instruction.value = instruction
        await Timer(1, unit="ns")
    
        assert int(dut.opcode.value) == opcode
        assert int(dut.rd.value) == rd
        assert int(dut.funct3.value) == funct3
        assert int(dut.rs1.value) == rs1
        assert int(dut.rs2.value) == rs2
        assert int(dut.funct7.value) == funct7





@cocotb.test()
async def test_cpu_arithmetic(dut):
    await setup_dut(dut)

    # ADDI x1, x0, 15
    await execute_instruction(
        dut,
        encode_i(1, 0, 15),
        pc=0,
        rd=1,
        data=15
    )

    # ADDI x2, x0, 8
    await execute_instruction(
        dut,
        encode_i(2, 0, 8),
        pc=4,
        rd=2,
        data=8
    )

    # ADD x3, x1, x2
    await execute_instruction(
        dut,
        await encode_r(
            3, 1, 2, 0b000, 0b0000000
        ),
        pc=8,
        rd=3,
        data=23
    )