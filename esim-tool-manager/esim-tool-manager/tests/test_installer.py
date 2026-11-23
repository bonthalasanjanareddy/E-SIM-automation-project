import subprocess

from tool_manager import installer


class Result:
    def __init__(self, code):
        self.returncode, self.stdout, self.stderr = code, "", ""


def fake_winget(monkeypatch, code):
    monkeypatch.setattr(installer, "winget_available", lambda: True)
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: Result(code))


def test_success(monkeypatch):
    fake_winget(monkeypatch, 0)
    assert installer.install_tool({"name": "X", "winget_id": "X.X"})[0] is True


def test_already_installed_counts_as_success(monkeypatch):
    fake_winget(monkeypatch, 2316632107)
    assert installer.install_tool({"name": "X", "winget_id": "X.X"})[0] is True


def test_real_failure_returns_message_not_crash(monkeypatch):
    fake_winget(monkeypatch, 1)
    ok, msg = installer.install_tool({"name": "X", "winget_id": "X.X"})
    assert ok is False and "exit code 1" in msg


def test_no_winget_id_falls_back_to_download(monkeypatch):
    monkeypatch.setattr(installer, "download_and_extract", lambda t: (True, "downloaded"))
    tool = {"name": "Ngspice", "winget_id": None, "download_url": "https://example.com/x.7z"}
    assert installer.install_tool(tool) == (True, "downloaded")


def test_nothing_defined_asks_for_manual_install():
    ok, msg = installer.install_tool({"name": "Y", "winget_id": None})
    assert ok is False and "manually" in msg
