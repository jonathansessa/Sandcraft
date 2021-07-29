import sys
from cx_Freeze import *

build_exe_opts = {  
                    "packages": ["pygame","sandcraft"],
                }

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "sandcraft",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]sandcraft.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Sandcraft",
    version = "1.0",
    author = "jsessa@ufl.edu",
    description = "Particle physics sandbox game",
    options = { "build_exe" : build_exe_opts,
                "bdist_msi" : bdist_msi_options
                },
    executables = [Executable("sandcraft/main.py", base = base, target_name = "sandcraft.exe")]
)