import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock

#helpers
async def reset_dut(dut):
    
    dut.reset.value = 1

    dut.pc_next.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    dut.reset.value =0
    await RisingEdge(dut.clk)

async def setup_dut(dut):
    Clock(dut.clk, 10, unit="ns").start()
    await reset_dut(dut)

async def send_pc_next(dut, value):
    dut.pc_next.value = value

async def get_current_pc(dut):
    return dut.pc.value

#tests
@cocotb.test()
async def test_reset(dut):
    Clock(dut.clk, 10, unit="ns").start()
    await reset_dut(dut)

    assert(dut.pc.value == 0)

@cocotb.test()
async def test_pc_next(dut):
    await setup_dut(dut)

    await send_pc_next(dut, 4)
    assert(await get_current_pc(dut) == 0)
    await RisingEdge(dut.clk)
    await ReadOnly()   
    await NextTimeStep() 
    await send_pc_next(dut, 8)
    assert(int(await get_current_pc(dut)) == 4)
    await RisingEdge(dut.clk)
    await ReadOnly()   
    await NextTimeStep() 
    await send_pc_next(dut, 12)
    assert(await get_current_pc(dut) == 8)

@cocotb.test()
async def test_boundaries(dut):
    await setup_dut(dut)

    await send_pc_next(dut, 0)
    await RisingEdge(dut.clk)
    await ReadOnly()   
    await NextTimeStep() 
    assert(await get_current_pc(dut) == 0)


    await send_pc_next(dut, 0xFFFFFFFF)
    await RisingEdge(dut.clk)
    await ReadOnly()   
    await NextTimeStep() 
    assert(await get_current_pc(dut) == 0xFFFFFFFF)

    await send_pc_next(dut, 0x00000001)
    await RisingEdge(dut.clk)
    await ReadOnly()   
    await NextTimeStep() 
    assert(await get_current_pc(dut) == 0x00000001)


@cocotb.test()
async def test_reset_priority(dut):
    await setup_dut(dut)

    await send_pc_next(dut, 4)
    assert(await get_current_pc(dut) == 0)
    await RisingEdge(dut.clk)
    await ReadOnly()   
    await NextTimeStep() 
    await send_pc_next(dut, 8)
    assert(await get_current_pc(dut) == 4)
    await RisingEdge(dut.clk)
    await ReadOnly()   
    await NextTimeStep() 
    await send_pc_next(dut, 8)
    assert(await get_current_pc(dut) == 8)

    dut.reset.value = 1
    assert(await get_current_pc(dut) == 8)
    await RisingEdge(dut.clk)
    await ReadOnly()   
    await NextTimeStep() 
    assert(await get_current_pc(dut) == 0)

@cocotb.test()
async def test_sequential(dut):
    await setup_dut(dut)
    for i in range(0, 100):
        await send_pc_next(dut, i)
        await RisingEdge(dut.clk)
        await ReadOnly()   
        await NextTimeStep() 
        assert(await get_current_pc(dut) == i)

