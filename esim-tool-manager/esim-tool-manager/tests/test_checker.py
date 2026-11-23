import sys

from tool_manager.checker import check_tool, find_executable, get_version


def test_missing_tool_is_reported():
    fake = {"name": "FakeTool", "executables": ["this-tool-does-not-exist"], "version_args": ["--version"]}
    result = check_tool(fake)
    assert result["status"] == "Missing"
    assert result["version"] == "-"


def test_python_is_found():
    python = {"name": "Python", "executables": ["python", "python3"], "version_args": ["--version"]}
    assert check_tool(python)["status"] == "Installed"


def test_newest_version_folder_wins(tmp_path):
    for v in ("9.0", "10.0"):
        d = tmp_path / "KiCad" / v / "bin"
        d.mkdir(parents=True)
        (d / "tool.exe").write_text("")
    found = find_executable(["nope-not-on-path"], [str(tmp_path / "KiCad" / "*" / "bin" / "tool.exe")])
    assert "10.0" in found  # 10 beats 9 numerically, not alphabetically


def test_version_regex_picks_named_group():
    out = get_version(sys.executable, ["--version"], r"Python (\d+\.\d+)")
    assert out == f"{sys.version_info.major}.{sys.version_info.minor}"
