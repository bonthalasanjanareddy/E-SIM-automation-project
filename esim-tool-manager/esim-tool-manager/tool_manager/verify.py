"""Smoke test: run a tiny circuit through ngspice to prove it really works."""
import os
import re
import subprocess
import tempfile
from pathlib import Path

SAMPLE_NETLIST = """RC smoke test
V1 in 0 DC 5
R1 in out 1k
C1 out 0 1u
.control
op
print v(out)
.endc
.end
"""


def run_smoke_test(ngspice_path, timeout=60):
    """Simulate a 5V source into an RC circuit. Returns (success, message)."""
    exe = os.path.abspath(ngspice_path)
    with tempfile.TemporaryDirectory() as tmp:
        cir = Path(tmp) / "smoke.cir"
        log = Path(tmp) / "smoke.log"
        cir.write_text(SAMPLE_NETLIST)
        try:
            # cwd = the exe's folder so ../lib/ngspice (code models) resolves
            subprocess.run(
                [exe, "-b", "-o", str(log), str(cir)],
                cwd=os.path.dirname(exe),
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            return False, f"could not run ngspice ({e})"

        output = log.read_text(errors="replace") if log.exists() else ""

    match = re.search(r"v\(out\)\s*=\s*([-+0-9.eE]+)", output)
    if match and abs(float(match.group(1)) - 5.0) < 1e-6:
        return True, f"ngspice simulated the test circuit: v(out) = {match.group(1)}"
    return False, "ngspice ran but gave unexpected output:\n" + output[-500:]
