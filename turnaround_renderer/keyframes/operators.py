import bpy
import re

from .utils import rotate_and_add_markers


def check_valid_marker_name(self, marker_name):
    msg = "A marker name can't contain any of these characters:\n \
        \\ / : * ? \" < > |"
    invalid_chars = r"[\\\/\:\*\?\"\<\>\|]"

    if re.search(invalid_chars, marker_name):
        self.report({'ERROR'}, msg)
        return False
    return True


class TURNAROUND_RENDERER_OT_insert_keyframes(bpy.types.Operator):
    """Insert rotation keyframes and add, if enabled, a marker to each
    showing the axis steps count"""

    bl_label = "Create Keyframes"
    bl_idname = "turnaround_renderer.insert_keyframes"

    @classmethod
    def poll(self, context):
        scene = context.scene
        props = scene.keyframes_properties

        return props.key_obj in set(scene.objects)

    def execute(self, context):
        scene = context.scene
        props = scene.keyframes_properties

        # Check preconditions
        if not check_valid_marker_name(self, props.marker_name):
            return {'FINISHED'}

        # Necessary parameters
        obj = props.key_obj
        x_turnaround = props.x_mode == 'TURNAROUND'
        x_angle = props.x_clamped_angle if x_turnaround else props.x_angle
        x_axis = props.x_rotation_axis
        x_min = 0 if x_turnaround else -props.left_steps
        x_max = props.x_steps - 1 if x_turnaround else props.right_steps
        if not props.x_axis:
            x_min = x_max = 0
        y_turnaround = props.y_mode == 'TURNAROUND'
        y_angle = props.y_clamped_angle if y_turnaround else props.y_angle
        y_axis = props.y_rotation_axis
        y_min = 0 if y_turnaround else -props.down_steps
        y_max = props.y_steps - 1 if y_turnaround else props.up_steps
        if not props.y_axis:
            y_min = y_max = 0
        add_markers = props.add_markers
        format = props.marker_name
        x_show_sign = not x_turnaround
        y_show_sign = not y_turnaround

        # Set start frame
        scene.frame_start = scene.frame_current

        # Rotate object
        rotate_and_add_markers(context, obj,
                               x_angle, x_axis, x_min, x_max,
                               y_angle, y_axis, y_min, y_max,
                               add_markers, format, x_show_sign, y_show_sign)

        # Set end frame
        scene.frame_end = scene.frame_current - 1

        # Move to start
        scene.frame_current = scene.frame_start

        # Select key object
        for obj in context.selected_objects:
            obj.select_set(False)
        context.view_layer.objects.active = obj
        obj.select_set(True)

        return {'FINISHED'}


classes = (TURNAROUND_RENDERER_OT_insert_keyframes,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
