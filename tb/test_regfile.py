import cocotb
import random
from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, NextTimeStep, Timer
from cocotb.clock import Clock


async def test_reset(dut):
    dut.reset.value = 1

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    dut.reset.value =0
    await RisingEdge(dut.clk)

    assert(dut.read_data1==0)
    assert(dut.read_data2==0)
    for i in range(32):
        assert(dut.registers[i]==0)


