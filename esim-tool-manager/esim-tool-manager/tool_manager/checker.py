import glob
import os
import re
import shutil
import subprocess

DEFAULT_VERSION_REGEX = r"\d+(?:\.\d+)*"


def find_executable(candidates, search_paths=None):
    """Look on PATH first, then in known install folders."""
    for name in candidates:
        path = shutil.which(name)
        if path:
            return path
    for pattern in search_paths or []:
        matches = glob.glob(os.path.expandvars(pattern), recursive=True)
        if matches:
            # newest version folder wins (compare numbers, not text)
            return max(matches, key=lambda p: [int(n) for n in re.findall(r"\d+", p)])
    return None


def get_version(path, version_args, version_regex=None):
    """Run '<tool> --version' and pull out the version number.

    The tool runs from its own folder: ngspice finds its code models
    through a path relative to its bin folder and fails otherwise.
    """
    try:
        result = subprocess.run(
            [path, *version_args],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=os.path.dirname(path) or None,
        )
        output = result.stdout + result.stderr
        match = re.search(version_regex or DEFAULT_VERSION_REGEX, output)
        if not match:
            return "unknown"
        return match.group(1) if match.groups() else match.group(0)
    except (subprocess.TimeoutExpired, OSError):
        return "unknown"


def check_tool(tool):
    """Return a dict with the tool's name, status, version and path."""
    path = find_executable(tool["executables"], tool.get("search_paths"))
    if path is None:
        return {"name": tool["name"], "status": "Missing", "version": "-", "path": "-"}
    return {
        "name": tool["name"],
        "status": "Installed",
        "version": get_version(path, tool["version_args"], tool.get("version_regex")),
        "path": path,
    }


def check_all(tools):
    return [check_tool(t) for t in tools]
