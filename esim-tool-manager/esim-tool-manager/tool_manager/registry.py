"""List of tools the manager checks for and knows how to install."""

TOOLS = [
    {
        "name": "Python",
        "executables": ["python", "python3"],
        "search_paths": [
            r"%LOCALAPPDATA%\Programs\Python\Python3*\python.exe",
            r"C:\Program Files\Python3*\python.exe",
        ],
        "version_args": ["--version"],
        "winget_id": "Python.Python.3.12",
    },
    {
        "name": "Git",
        "executables": ["git"],
        "search_paths": [
            r"C:\Program Files\Git\cmd\git.exe",
            r"%LOCALAPPDATA%\Programs\Git\cmd\git.exe",
        ],
        "version_args": ["--version"],
        "winget_id": "Git.Git",
    },
    {
        "name": "KiCad",
        "executables": ["kicad-cli"],
        "search_paths": [
            r"%LOCALAPPDATA%\Programs\KiCad\*\bin\kicad-cli.exe",
            r"C:\Program Files\KiCad\*\bin\kicad-cli.exe",
        ],
        "version_args": ["--version"],
        "winget_id": "KiCad.KiCad",
    },
    {
        "name": "Ngspice",
        # ngspice_con is the console build; plain "ngspice" is the GUI build
        # and can hang when started from a script.
        "executables": ["ngspice_con", "ngspice"],
        "search_paths": [
            r"%LOCALAPPDATA%\eSimToolManager\tools\ngspice\**\ngspice_con.exe",
            r"C:\Spice64\bin\ngspice_con.exe",
        ],
        "version_args": ["--version"],
        "version_regex": r"ngspice-(\d+(?:\.\d+)*)",
        "winget_id": None,  # not on winget, so we download it instead
        "download_url": "https://sourceforge.net/projects/ngspice/files/ng-spice-rework/47/ngspice-47_64.7z/download",
        "download_name": "ngspice.7z",
    },
]
