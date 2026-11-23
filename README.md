# eSim Automated Tool Manager

**FOSSEE eSim Semester Long Internship – Autumn 2026**  
**Screening Task 5: Automated Tool Manager (CSE and Related Fields)**

## 1. Project Overview

The **eSim Automated Tool Manager** is a Python-based command-line application developed to simplify the management of external tools required by the eSim Electronic Design Automation (EDA) environment.

eSim depends on external applications and utilities such as KiCad, Ngspice, Git, and Python. Installing and verifying these tools manually can be time-consuming.

This project provides a centralized solution to detect installed tools, check their versions, identify missing dependencies, and assist users with tool installation through a simple command-line interface.

## 2. Objectives

- Automate the detection of essential tools required by eSim.
- Check whether the required tools are installed.
- Retrieve and display installed tool versions.
- Assist users in installing missing tools.
- Provide a command-line interface for managing tools.
- Verify Ngspice functionality through a simulation test.
- Maintain logs of tool manager operations.

## 3. Features

### Tool Detection and Version Checking
- Detects whether supported tools are available on the system.
- Searches system paths for executable files.
- Retrieves installed tool versions.
- Displays the installation status of each tool.

### Tool Installation Management
- Identifies missing tools.
- Supports installation through Windows Package Manager (winget) where configured.
- Provides installation assistance for required utilities.
- Handles installation errors and existing installations.

### Command-Line Interface
- Provides a simple interface for checking tool availability.
- Displays tool names, versions, and installation status.
- Allows users to run verification operations.

### Ngspice Verification
- Includes a sample circuit file.
- Runs a basic Ngspice simulation to verify that the simulator is functioning.
- Reports the verification result.

### Logging
- Records important operations and errors.
- Helps users understand the actions performed by the application.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Subprocess | Executing system commands and external tools |
| OS and Pathlib | File system and environment path management |
| Requests / Download utilities | Tool download support |
| Pytest | Unit testing |
| Colorama | Terminal output formatting |
| Git | Version control |

## 5. Project Architecture

The project follows a modular architecture in which each module is responsible for a specific task.

```text
esim-tool-manager/
│
├── main.py
│
├── tool_manager/
│   ├── __init__.py
│   ├── checker.py
│   ├── downloader.py
│   ├── installer.py
│   ├── logger.py
│   ├── registry.py
│   └── verify.py
│
├── tests/
│   ├── test_checker.py
│   └── test_installer.py
│
├── samples/
│   └── rc_test.cir
│
├── requirements.txt
├── pytest.ini
├── .gitignore
├── README.md
└── DESIGN_DOCUMENT.pdf
```

### Module Description

| Module | Responsibility |
|---|---|
| `main.py` | Main entry point and command-line interface |
| `checker.py` | Detects installed tools and checks versions |
| `downloader.py` | Handles tool downloads and extraction |
| `installer.py` | Manages tool installation |
| `logger.py` | Records application activities and errors |
| `registry.py` | Maintains tool information and installation details |
| `verify.py` | Verifies Ngspice functionality |
| `tests/` | Contains automated unit tests |
| `samples/` | Contains sample circuit files |

## 6. Requirements

Before running the application, ensure that the following are available:

- Windows 10 or Windows 11
- Python 3.10 or later
- Git (recommended)
- Windows Package Manager (winget)
- Required permissions for installing external tools

Some tools may need to be installed separately depending on the system configuration.

## 7. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd esim-tool-manager
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Then activate the environment again.

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## 8. How to Run

Run the following command to start the application:

```bash
python main.py
```

### Check Installed Tools

```bash
python main.py --check
```

This command checks the availability of supported tools and displays their installation status and detected versions.

### Verify Ngspice

```bash
python main.py --verify
```

This command runs the Ngspice verification procedure using the sample circuit file.

 9. Testing

The project uses Pytest for automated testing.

Run the following command from the project root:

```bash
python -m pytest -v
```

The tests cover important functionality, including tool detection and installation-related operations.

10. Sample Output

The command-line interface displays a status table similar to the following:

```text
========================================
       eSim AUTOMATED TOOL MANAGER
========================================

Tool       Status       Version
----------------------------------------
Python     Installed    Detected Version
Git        Installed    Detected Version
KiCad      Installed    Detected Version
Ngspice    Installed    Detected Version

----------------------------------------
Tool checking completed.
```

*Note: Actual results depend on the tools installed and detected on the user's system.*

11. Error Handling

The application includes basic error handling for:

- Missing tools.
- Unavailable executable paths.
- Installation failures.
- Download and extraction errors.
- Version detection failures.
- Ngspice verification failures.

Relevant operations and errors are recorded through the logging module.

 12. Current Scope and Limitations

- The current implementation is primarily designed for Windows environments.
- Tool installation depends on the availability of winget and the configured installation details.
- Ngspice download support uses a configured release source.
- Tool availability and version detection depend on executable paths and system configuration.
- Full Linux and macOS support is not currently implemented.
- A complete automatic update-management system is outside the current prototype scope.

 13. Future Enhancements

The project can be extended with the following features:

- Cross-platform support for Linux, Windows, and macOS.
- Automatic tool update and upgrade management.
- Configuration and environment-variable management.
- Advanced dependency compatibility checking.
- Graphical user interface (GUI).
- Automatic backup and restoration of tool configurations.
- Integration with additional package managers.

 14. Deliverables

This repository contains the following deliverables:

1. Python source code for the Automated Tool Manager.
2. Design document explaining the architecture and module interactions.
3. Execution instructions and dependency requirements.
4. Automated test cases.
5. Sample circuit file for Ngspice verification.

 
