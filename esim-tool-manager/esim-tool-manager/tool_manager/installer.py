import shutil
import subprocess

from tool_manager.downloader import download_and_extract
from tool_manager.logger import get_logger

log = get_logger()

# winget exit codes that mean "already installed, nothing to do".
# 0x8A15002B = no applicable upgrade, 0x8A150061 = package already installed.
WINGET_ALREADY_INSTALLED = {2316632107, 2316632161}


def winget_available():
    return shutil.which("winget") is not None


def install_tool(tool):
    """Install one tool: winget if it has a package id, else download it.

    Returns (success, message).
    """
    name = tool["name"]
    winget_id = tool.get("winget_id")

    if not winget_id:
        if tool.get("download_url"):
            return download_and_extract(tool)
        msg = f"{name}: no winget package or download link defined, install manually"
        log.warning(msg)
        return False, msg

    if not winget_available():
        msg = "winget not found on this system"
        log.error(msg)
        return False, msg

    cmd = [
        "winget", "install",
        "--id", winget_id,
        "--exact",
        "--silent",
        "--accept-package-agreements",
        "--accept-source-agreements",
    ]
    log.info("Running: %s", " ".join(cmd))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    except (subprocess.TimeoutExpired, OSError) as e:
        msg = f"{name}: install failed ({e})"
        log.error(msg)
        return False, msg

    if result.returncode == 0:
        msg = f"{name}: installed successfully"
        log.info(msg)
        return True, msg

    if result.returncode in WINGET_ALREADY_INSTALLED:
        msg = f"{name}: already installed (no upgrade needed)"
        log.info(msg)
        return True, msg

    msg = f"{name}: install failed (exit code {result.returncode})"
    log.error("%s\n%s", msg, result.stdout + result.stderr)
    return False, msg
