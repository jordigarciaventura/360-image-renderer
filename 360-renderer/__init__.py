# Copyright (C) 2020 Jordi García Ventura
# contact.garven@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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

if "bpy" in locals():
    import importlib

    importlib.reload(properties)
    importlib.reload(create_preset)
    importlib.reload(align_location)
    importlib.reload(align_rotation)
    importlib.reload(insert_keyframes)
    importlib.reload(export_marker_names)
    importlib.reload(ui_panels)

else:
    from . import (
        properties,
        create_preset,
        align_location,
        align_rotation,
        insert_keyframes,
        export_marker_names,
        ui_panels,
    )

import bpy

classes = (
    properties.classes
    + create_preset.classes
    + align_location.classes
    + align_rotation.classes
    + insert_keyframes.classes
    + export_marker_names.classes
    + ui_panels.classes
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=properties.MyProperties)
    properties.register_icons()


def unregister():
    properties.unregister_icons()
    del bpy.types.Scene.my_tool
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
