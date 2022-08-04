"""
Boot script for support debugging multi-file add-ons inside
Blender 'Scripting' tab.

Attributes
----------
project_dir : str
    path of the add-on project folder
init_file_name : str
    name of the init file (should not change)
"""

import os
import sys

addon_dir = r"C:\Users\jordi\Documents\GitHub\360-renderer\turnaround_renderer"
init_file_name = "__init__.py"

if addon_dir not in sys.path:
    sys.path.append(addon_dir)

file_path = os.path.join(addon_dir, init_file_name)

exec(compile(open(file_path).read(), init_file_name, 'exec'))
