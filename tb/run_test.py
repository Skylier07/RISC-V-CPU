from pathlib import Path
from cocotb_tools.runner import get_runner
tb_dir = Path(__file__).resolve().parent
project_dir = tb_dir.parent
rtl_dir = project_dir/"rtl"
runner = get_runner("icarus")

runner.build(
    sources=[rtl_dir/"regfile.sv"],
    hdl_toplevel="regfile",
    always=True,
    waves=True,
)

runner.test(
    hdl_toplevel="regfile",
    test_module="regfile_tb",
    test_dir=tb_dir,
    waves=True,
    gui=True,
)