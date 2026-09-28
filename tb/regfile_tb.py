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

async def setup_dut(dut):
    Clock(dut.clk, 10, unit="ns").start()
    await reset_dut(dut)

async def write_reg(dut, rd, value):
    dut.write_en.value = 1
    dut.rd.value=rd
    dut.write_data.value = value
    await RisingEdge(dut.clk)
    await ReadOnly()
    await NextTimeStep()
    dut.write_en.value=0

async def read_rs1(dut, register):
    dut.rs1.value = register
    await ReadOnly()
    await NextTimeStep()
    return dut.read_data1.value

async def read_rs2(dut, register):
    dut.rs2.value = register
    await ReadOnly()
    await NextTimeStep()
    return dut.read_data2.value




#tests
@cocotb.test()
async def test_reset(dut):
    Clock(dut.clk, 10, unit="ns").start()
    await reset_dut(dut)

    for i in range(32):
        assert(dut.registers[i].value==0)

@cocotb.test()
async def test_read_write(dut):
    await setup_dut(dut)
    await write_reg(dut, 5, 100)
    assert(dut.registers[5].value == 100) 
    assert(await read_rs1(dut, 5) == 100)
    
@cocotb.test()
async def test_multi_read_write(dut):
    await setup_dut(dut)

    r_value = 10
    await write_reg(dut, r_value, 10)

    r_value = 15
    await write_reg(dut, r_value, 11)

    r_value = 31
    await write_reg(dut, r_value, 12)

    r_value = 2
    await write_reg(dut, r_value, 13)

    r_value = 9
    await write_reg(dut, r_value, 14)


    assert(await read_rs1(dut, 10) == 10)
    assert(await read_rs1(dut, 15) == 11)
    assert(await read_rs1(dut, 31) == 12)
    assert(await read_rs1(dut, 2) == 13)
    assert(await read_rs1(dut, 9) == 14)

@cocotb.test()
async def test_read_simultaneous(dut):
    await setup_dut(dut)


    r_value = 10
    await write_reg(dut, r_value, 10)

    r_value = 15
    await write_reg(dut, r_value, 11)
    assert((await read_rs1(dut, 10) == 10) and await read_rs2(dut, 15) == 11)

@cocotb.test()
async def test_read_same_register(dut):
    await setup_dut(dut)
    r_value = 10
    await write_reg(dut, r_value, 10)


    assert((await read_rs1(dut, 10) == 10) and await read_rs2(dut, 10) == 10)

    
@cocotb.test()
async def test_modify_x0(dut):
    await setup_dut(dut)

    for i in range(0, 100):
        await write_reg(dut, 0, i)

    assert(await read_rs1(dut, 0) ==0)
    assert(dut.registers[0].value == 0)
    
@cocotb.test()
async def write_disabled(dut):
    await setup_dut(dut)
    r_value = 10
    await write_reg(dut, r_value, 10)

    dut.write_en.value = 0
    dut.rd.value=10
    dut.write_data.value = 28
    await RisingEdge(dut.clk)
    await ReadOnly()
    await NextTimeStep()

    assert(await read_rs1(dut, 10) == 10)


    
@cocotb.test()
async def test_boundaries(dut):
    await setup_dut(dut)

    r_value = 1
    await write_reg(dut, r_value, 0)

    r_value = 30
    await write_reg(dut, r_value, 0xFFFFFFFF)

    r_value = 31
    await write_reg(dut, r_value, 0x00000001)

    assert(await read_rs1(dut, 1) == 0)
    assert(await read_rs1(dut, 30) == 0xFFFFFFFF)
    assert(await read_rs1(dut, 31) == 0x00000001)

