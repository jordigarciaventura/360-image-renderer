import importlib
import os
import sys

import bpy

bl_info = {
    "name": "360 Renderer",
    "description": "Render your models up to 360 degrees as image sequence",
    "author": "Garven",
    "version": (1, 0),
    "blender": (2, 81, 16),
    "location": "View3d > Tool",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render",
}

# Add path to use absolute imports
file_path = os.path.realpath(__file__)
dir_path = os.path.dirname(file_path)
sys.path.append(dir_path)

module_names = ["properties",
                "add_camera_controller",
                "add_light_controller",
                "align_location",
                "align_rotation",
                "swap_align",
                "insert_keyframes",
                "export_marker_names",
                "ui_panels"]

for module_name in module_names:
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    else:
        importlib.import_module(module_name)


def register():
    for module_name in module_names:
        if module_name in sys.modules:
            module = sys.modules[module_name]
            if hasattr(module, 'register'):
                module.register()

        bpy.types.Scene.my_tool = bpy.props.PointerProperty(
            type=sys.modules["properties"].MyProperties)


def unregister():
    del bpy.types.Scene.my_tool

    for module_name in reversed(module_names):
        module = sys.modules[module_name]
        if hasattr(module, 'unregister'):
            module.unregister()


if __name__ == "__main__":
    register()
