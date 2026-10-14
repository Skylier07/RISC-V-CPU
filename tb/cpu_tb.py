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
        await ReadOnly()    
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
        encode_r(
            3, 1, 2, 0b000, 0b0000000
        ),
        pc=8,
        rd=3,
        data=23
    )

    # ADDI x4, x2, -10
    await execute_instruction(
        dut,
        encode_i(4, 2, -10),
        pc=12,
        rd=4,
        data=-2
    )

    # SUB x5 x3, x2 
    await execute_instruction(
        dut,
        encode_r(
            5, 3, 2, 0b000, 0b0100000
        ),
        pc=16,
        rd=5,
        data=15
    )

    # SUB x6 x5, x4 
    await execute_instruction(
        dut,
        encode_r(
            6, 5, 4, 0b000, 0b0100000
        ),
        pc=20,
        rd=6,
        data=17
    )


@cocotb.test()
async def test_cpu_logic(dut):
    await setup_dut(dut)


    # ADDI x1, x0, 15
    await execute_instruction(
        dut,
        encode_i(1, 0, 0b0010),
        pc=0,
        rd=1,
        data=0b0010
    )

    # ADDI x2, x0, 8
    await execute_instruction(
        dut,
        encode_i(2, 0, 0b1110),
        pc=4,
        rd=2,
        data=0b1110
    )

    # AND x3, x1, x2
    await execute_instruction(
        dut,
        encode_r(
            3, 1, 2, 0b111, 0b0000000
        ),
        pc=8,
        rd=3,
        data=0b0010
    )

    # OR x4, x1, x2
    await execute_instruction(
        dut,
        encode_r(
            4, 1, 2, 0b110, 0b0000000
        ),
        pc=12,
        rd=4,
        data=0b1110
    )

    # XOR x5, x1, x2
    await execute_instruction(
        dut,
        encode_r(
            5, 1, 2, 0b100, 0b0000000
        ),
        pc=16,
        rd=5,
        data=0b1100
    )

    # ANDI x6, x2, b'1001
    await execute_instruction(
        dut,
        encode_i(
            6, 2, 0b1001, 0b111
        ),
        pc=20,
        rd=6,
        data=0b1000
    )

    # ORI x7, x2, b'1001
    await execute_instruction(
        dut,
        encode_i(
            7, 2, 0b1001, 0b110
        ),
        pc=24,
        rd=7,
        data=0b1111
    )

    # XORI x8, x2, b'1001
    await execute_instruction(
        dut,
        encode_i(
            8, 2, 0b1001, 0b100
        ),
        pc=28,
        rd=8,
        data=0b0111
    )

    # SLT x9, x2, x1
    await execute_instruction(
        dut,
        encode_r(
            9, 2, 1, 0b010, 0b0000000
        ),
        pc=32,
        rd=9,
        data=0b0
    )

    # SLT x10, x1, x2
    await execute_instruction(
        dut,
        encode_r(
            10, 1, 2, 0b010, 0b0000000
        ),
        pc=36,
        rd=10,
        data=0b1
    )


    # SLTI x11, x2, 0b1111
    await execute_instruction(
        dut,
        encode_i(
            11, 2, 0b1111, 0b010
        ),
        pc=40,
        rd=11,
        data=0b1
    )

    # SLT x12, x2, 0b0011
    await execute_instruction(
        dut,
        encode_i(
            12, 2, 0b0011, 0b010
        ),
        pc=44,
        rd=12,
        data=0b0
    )