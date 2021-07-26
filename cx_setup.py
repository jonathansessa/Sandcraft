import sys
from cx_Freeze import setup, Executable

build_exe_opts = {  
                    "packages": ["pygame","sandcraft"],
                    "excludes": ["tkinter"]
                }

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Sandcraft",
    version = "1.0",
    author = "jsessa@ufl.edu",
    description = "Particle physics sandbox game",
    options = {"build_exe": build_exe_opts},
    executables = [Executable("sandcraft/main.py", base = base, target_name = "sandcraft.exe")]
)