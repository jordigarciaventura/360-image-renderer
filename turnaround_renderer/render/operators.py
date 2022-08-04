import bpy
import re

from .utils import render_by_marker_names


def check_render_path(self, context):
    msg = "Select a path to save the frames"
    scene = context.scene

    if not scene.render.filepath:
        self.report({'ERROR'}, msg)
        return False
    return True


def check_project_saved(self):
    msg = "The project is not saved"

    if not bpy.data.is_saved:
        self.report({'ERROR'}, msg)
        return False
    return True


def check_named_markers(self, context):
    msg = "Not all frames within the render range have a named marker"
    scene = context.scene

    named_markers_count = 0

    # Get markers names inside render range
    for frame in range(scene.frame_start, scene.frame_end + 1):
        for marker in scene.timeline_markers:
            if marker.frame == frame and marker.name:
                named_markers_count += 1

    frames_count = 1 + scene.frame_end - scene.frame_start
    if named_markers_count != frames_count:
        self.report({'ERROR'}, msg)
        return False
    return True


def check_marker_names(self, context):
    msg = "A marker name can't contain any of these characters:\n \
    \\ / : * ? \" < > |"
    invalid_chars = r"[\\\/\:\*\?\"\<\>\|]"
    scene = context.scene

    for marker in scene.timeline_markers:
        if re.search(invalid_chars, marker.name):
            self.report({'ERROR'}, msg)
            return False
    return True


def check_active_camera(self, context):
    msg = "There is no active camera"
    scene = context.scene

    if not scene.camera:
        self.report({'ERROR'}, msg)
        return False
    return True


class TURNAROUND_RENDERER_OT_export(bpy.types.Operator):
    """Render animation using markers as filename"""

    bl_label = "Export Keyframes"
    bl_idname = "turnaround_renderer.export"

    def execute(self, context):
        # Check preconditions
        if not check_project_saved(self):
            return {'FINISHED'}

        if not check_render_path(self, context):
            return {'FINISHED'}

        if not check_active_camera(self, context):
            return {'FINISHED'}

        if not check_named_markers(self, context):
            return {'FINISHED'}

        if not check_marker_names(self, context):
            return {'FINISHED'}

        # Save project
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

        render_by_marker_names(context)

        return {'FINISHED'}


classes = (TURNAROUND_RENDERER_OT_export,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
