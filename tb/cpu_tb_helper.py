import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock

import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock


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

# Legacy
async def build_instruct(op, rd, funct3, rs1, rs2, funct7):
    instruction = 0
    instruction |= (op & 0x7F)
    instruction |= (rd & 0x1F) << 7
    instruction |= (funct3 & 0x07) << 12
    instruction |= (rs1 & 0x1F) << 15
    instruction |= (rs2 & 0x1F) << 20
    instruction |= (funct7 & 0x7F) << 25

    return instruction

def encode_r(rd, rs1, rs2, funct3, funct7):
    opcode = 0b0110011
    return ((funct7 << 25)
        | (rs2 << 20)
        | (rs1 << 15)
        |(funct3 << 12)
        | (rd << 7)
        | opcode
    )


def encode_i(rd, rs1, imm, funct3=0):
    opcode = 0b0010011

    return (((imm& 0xFFF) << 20)
        | (rs1 << 15)
        |(funct3 << 12)
        | (rd << 7)
        | opcode
    )

async def execute_instruction(dut, instruction, pc, rd, data):
    dut.instruction.value = instruction

    await Timer(1, unit="ns")

    dut._log.info(
        f"Expected PC: {pc}, "
        f"Actual PC: {int(dut.instruction_addr.value)}"
    )

    assert int(dut.instruction_addr.value) == pc

    assert int(dut.instr_valid.value) == 1

    assert int(dut.debug_wb_en.value) == 1
    assert int(dut.debug_wb_rd.value) == rd
    assert int(dut.debug_wb_data.value) == data

    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.instruction_addr.value) == pc + 4

    await FallingEdge(dut.clk)