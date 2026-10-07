from pathlib import Path
from cocotb_tools.runner import get_runner
import sys

tb_dir = Path(__file__).resolve().parent
project_dir = tb_dir.parent
rtl_dir = project_dir / "rtl"


TESTS = {
    "regfile": {
        "sources": [
            rtl_dir / "regfile.sv",
        ],
        "top": "regfile",
        "test_module": "regfile_tb",
    },

    "pc": {
        "sources": [
            rtl_dir / "pc.sv",
        ],
        "top": "program_counter",
        "test_module": "pc_tb",
    },

    "instruction_decode": {
        "sources": [
            rtl_dir / "instruction_decode.sv",
        ],
        "top": "instr_decode",
        "test_module": "instruction_decode_tb",
    },
    "imm_gen": {
        "sources": [
            rtl_dir / "imm_generator.sv",
        ],
        "top": "imm_gen",
        "test_module": "imm_generator_tb",
    },

    "alu": {
        "sources": [
            rtl_dir / "alu.sv",
        ],
        "top": "alu",
        "test_module": "alu_tb",
    },



}


def run_test(component):

    config = TESTS[component]

    runner = get_runner("icarus")

    runner.build(
        sources=config["sources"],
        hdl_toplevel=config["top"],
        build_dir=project_dir / "sim_build" / component,
        always=True,
        waves=True,
    )

    runner.test(
        hdl_toplevel=config["top"],
        test_module=config["test_module"],
        test_dir=tb_dir,
        build_dir=project_dir / "sim_build" / component,
        waves=True,
        gui=True,
    )


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("  python tb/run_test.py regfile")
        print("  python tb/run_test.py pc")
        sys.exit(1)

    component = sys.argv[1]

    if component not in TESTS:
        print(f"Unknown component: {component}")
        print(f"Available tests: {', '.join(TESTS.keys())}")
        sys.exit(1)

    run_test(component)