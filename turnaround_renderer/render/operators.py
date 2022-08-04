import bpy
import re

from .utils import export_marker_names

project_not_saved_error = "The project is not saved"
path_empty_error = "Select a path to save the frames"
no_active_camera_error = "There is no active camera"
markers_names_named_error = (
    "Not all frames within the render range \
    have a named marker"
)
marker_name_error = (
    """A marker name can't contain any of these characters:
    \\ / : * ? " < > |"""
)


def validate_file_name(name):
    invalid_chars = r"[\\\/\:\*\?\"\<\>\|]"
    return not re.search(invalid_chars, name)


class TURNAROUND_RENDERER_OT_export(bpy.types.Operator):
    """Render animation using markers as filename"""

    bl_label = "Export Keyframes"
    bl_idname = "turnaround_renderer.export"

    def execute(self, context):
        scene = context.scene

        # Check dependencies
        if not bpy.data.is_saved:
            self.report({"ERROR"}, project_not_saved_error)
            return {"FINISHED"}

        if not scene.render.filepath:
            self.report({"ERROR"}, path_empty_error)
            return {"FINISHED"}

        if not scene.camera:
            self.report({"ERROR"}, no_active_camera_error)
            return {"FINISHED"}

        markers_names = []

        # Get markers names inside render range
        for frame in range(scene.frame_start, scene.frame_end + 1):
            for marker in scene.timeline_markers:
                if marker.frame == frame and marker.name:
                    markers_names.append(marker.name)
                    print(marker.name)

        # Check if all frames have a marker
        if len(markers_names) < 1 + scene.frame_start - scene.frame_end:
            self.report({"ERROR"}, markers_names_named_error)
            return {"FINISHED"}

        # Check if all markers have a valid name
        for name in markers_names:
            if not validate_file_name(name):
                self.report({"ERROR"}, marker_name_error)
                return {"FINISHED"}

        export_marker_names(context)

        return {"FINISHED"}


classes = (TURNAROUND_RENDERER_OT_export,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
