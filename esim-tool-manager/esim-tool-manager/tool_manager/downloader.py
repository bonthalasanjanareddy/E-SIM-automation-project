import os
import subprocess
import urllib.request
import zipfile
from pathlib import Path

from tool_manager.checker import find_executable
from tool_manager.logger import get_logger

log = get_logger()

SEVEN_ZIP_PATHS = [
    r"C:\Program Files\7-Zip\7z.exe",
    r"C:\Program Files (x86)\7-Zip\7z.exe",
    r"%LOCALAPPDATA%\Programs\7-Zip\7z.exe",
]


def tools_dir():
    """Folder where our tool keeps the software it downloads."""
    local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    base = Path(local) / "eSimToolManager" / "tools"
    base.mkdir(parents=True, exist_ok=True)
    return base


def get_7zip():
    """Find 7-Zip. If it is missing, install it with winget, then look again."""
    exe = find_executable(["7z"], SEVEN_ZIP_PATHS)
    if exe:
        return exe

    log.info("7-Zip not found, installing with winget")
    subprocess.run(
        [
            "winget", "install", "--id", "7zip.7zip", "--exact", "--silent",
            "--accept-package-agreements", "--accept-source-agreements",
        ],
        capture_output=True,
        text=True,
        timeout=900,
    )
    return find_executable(["7z"], SEVEN_ZIP_PATHS)


def extract(archive, target):
    """Unpack a .zip or .7z file into the target folder."""
    if archive.suffix == ".zip":
        with zipfile.ZipFile(archive) as z:
            z.extractall(target)
    elif archive.suffix == ".7z":
        seven_zip = get_7zip()
        if not seven_zip:
            raise RuntimeError("7-Zip is needed to unpack .7z files but could not be installed")
        subprocess.run(
            [seven_zip, "x", str(archive), f"-o{target}", "-y"],
            check=True,
            capture_output=True,
        )
    else:
        raise RuntimeError(f"unsupported archive type {archive.suffix}")


def download_and_extract(tool):
    """Download a tool's archive and unpack it. Returns (success, message)."""
    name = tool["name"]
    url = tool.get("download_url")
    if not url:
        msg = f"{name}: no download link set in registry.py"
        log.error(msg)
        return False, msg

    target = tools_dir() / name.lower()
    target.mkdir(parents=True, exist_ok=True)
    archive = target / tool.get("download_name", "download.bin")

    try:
        log.info("Downloading %s from %s", name, url)
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=120) as response, open(archive, "wb") as f:
            f.write(response.read())

        log.info("Extracting %s", archive)
        extract(archive, target)
        archive.unlink()
    except Exception as e:
        msg = f"{name}: download failed ({e})"
        log.error(msg)
        return False, msg

    msg = f"{name}: downloaded and unpacked to {target}"
    log.info(msg)
    return True, msg
