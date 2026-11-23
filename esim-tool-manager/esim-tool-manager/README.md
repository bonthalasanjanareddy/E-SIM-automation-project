# eSim Tool Manager

A small Windows command-line tool that checks whether the software needed for
eSim-style circuit design (Python, Git, KiCad, Ngspice) is installed, shows the
version of each, and installs whatever is missing.

## Features
- Detects tools on `PATH` and in common install folders (newest version wins)
- Shows a status table: name, status, version, path
- Installs missing tools with **winget**; Ngspice (not on winget) is downloaded
  and unpacked automatically (7-Zip is installed if needed)
- `--verify` runs a real ngspice simulation to prove the install works
- Treats winget's "already installed" exit code as success
- Logs everything to `logs/tool_manager.log`

## Requirements
Windows 10/11, Python 3.10+, winget (App Installer).

## Usage
```powershell
python main.py              # check, then offer to install missing tools
python main.py --check      # status table only, exit code 1 if anything is missing
python main.py --verify     # also run the ngspice smoke test
```

Example output:
```
Software    Status      Version     Path
----------------------------------------------------------------------
Python      Installed   3.12.4      C:\...\python.exe
Git         Installed   2.45.1      C:\Program Files\Git\cmd\git.exe
KiCad       Installed   9.0.1       C:\Program Files\KiCad\9.0\bin\kicad-cli.exe
Ngspice     Installed   47          C:\Spice64\bin\ngspice_con.exe

Verify: OK - ngspice simulated the test circuit: v(out) = 5.000000e+00
```
(Replace with your own screenshot.)

## Project layout
```
main.py                  command-line entry point
tool_manager/registry.py list of tools, how to find and install each
tool_manager/checker.py  detection and version parsing
tool_manager/installer.py winget install, with download fallback
tool_manager/downloader.py download + unpack (.zip / .7z)
tool_manager/verify.py   ngspice smoke test
samples/rc_test.cir      example netlist
tests/                   pytest tests
```

## Windows notes (lessons learned)
- Use **`ngspice_con.exe`** (console build) in scripts. Plain `ngspice.exe` is
  the GUI build and can hang.
- ngspice finds its code models via `..\lib\ngspice`, relative to the exe. It must
  be launched with its own `bin` folder as the working directory, otherwise you get
  `Error opening code model "../lib/ngspice/xtraevt.cm"`. The tool does this.
- winget exit code `2316632107` means "already installed, no upgrade", not a failure.
- Newly installed programs are not on `PATH` until a new terminal is opened, so the
  tool also searches the standard install folders.

## Tests
```powershell
pip install -r requirements.txt
python -m pytest
```

## Known limitations
- Windows only. Ngspice download URL is pinned to version 47.
- Installing with winget may show a UAC prompt.
