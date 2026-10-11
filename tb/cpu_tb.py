import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock

import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock

#helpers
async def reset_dut(dut):
    
    dut.reset.value = 1

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    dut.reset.value =0
    await RisingEdge(dut.clk)


async def get_current_address(dut):
    return dut.instruction_addr.value

# Program Counter
async def setup_dut(dut):
    Clock(dut.clk, 10, unit="ns").start()
    await reset_dut(dut)

# Instruction Decode
async def build_instruct(op, rd, funct3, rs1, rs2, funct7):
    instruction = 0
    instruction |= (op & 0x7F)
    instruction |= (rd     & 0x1F) << 7
    instruction |= (funct3 & 0x07) << 12
    instruction |= (rs1    & 0x1F) << 15
    instruction |= (rs2    & 0x1F) << 20
    instruction |= (funct7 & 0x7F) << 25

    return instruction


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


    
