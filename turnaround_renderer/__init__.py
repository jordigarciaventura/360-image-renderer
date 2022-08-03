import bpy
import importlib
import sys

bl_info = {
    "name": "360 Renderer",
    "description": "Render your models up to 360 degrees as image sequence",
    "author": "jordigarciaventura",
    "version": (1, 0),
    "blender": (3, 2, 1),
    "location": "View3d > Tool",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render",
}

ordered_module_names = [
    "setup.utils",
    "setup.properties",
    "setup.panels",
    "setup.operators",
    "align.properties",
    "align.panels",
    "align.operators",
    "keyframes.utils",
    "keyframes.properties",
    "keyframes.panels",
    "keyframes.operators",
    "render.utils",
    "render.properties",
    "render.panels",
    "render.operators"
]

if __name__ != "__main__":
    ordered_module_names = [f"{__name__}.{name}" for name in ordered_module_names]

# IMPORT
for module_name in ordered_module_names:
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    else:
        importlib.import_module(module_name)


# REGISTER
def register():
    modules_attribute_caller(ordered_module_names, "register")


# UNREGISTER
def unregister():
    modules_attribute_caller(reversed(ordered_module_names), "unregister")


def modules_attribute_caller(module_names, attribute):
    for module_name in module_names:
        if module_name in sys.modules:
            module = sys.modules[module_name]
            if hasattr(module, attribute):
                getattr(module, attribute)()


if __name__ == "__main__":
    register()
