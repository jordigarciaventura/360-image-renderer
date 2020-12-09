import bpy

from . import properties as prop

from math import (
    radians,
    degrees,
)

import re

initial_rotation = None
views = set()

# Rotate object
def rotate_and_add_marker(
    obj, x_axis, x_steps, x_angle, y_axis, y_steps, y_angle, marker_namerule
):

    scene = bpy.context.scene

    # Get orient axis
    x_orient_axis = x_axis.replace("-", "")
    y_orient_axis = y_axis.replace("-", "")

    # Get dir
    x_dir = int(re.sub("[XYZ]", "1", x_axis))
    y_dir = int(re.sub("[XYZ]", "1", y_axis))

    for y in range(0, abs(y_steps) + 1):
        for x in range(0, abs(x_steps) + 1):

            # Get x and y signed (ID)
            signed_x = -x if x_steps < 0 else x
            signed_y = -y if y_steps < 0 else y

            # Check to avoid repetitions
            if (signed_x, signed_y) in views:
                continue
            else:
                views.add((signed_x, signed_y))

            # Calculate absolute angles
            x_angle_abs = radians(degrees(x_angle * x))
            y_angle_abs = radians(degrees(y_angle * y))

            # Set rotation to initial
            global initial_rotation
            obj.rotation_euler = initial_rotation

            # Rotate

            # Right
            if x_steps > 0:
                obj.rotation_euler.rotate_axis(x_orient_axis, x_angle_abs * x_dir)
            # Left
            else:
                obj.rotation_euler.rotate_axis(x_orient_axis, -x_angle_abs * x_dir)
            # Up
            if y_steps > 0:
                obj.rotation_euler.rotate_axis(y_orient_axis, -y_angle_abs * y_dir)
            # Down
            else:
                obj.rotation_euler.rotate_axis(y_orient_axis, y_angle_abs * y_dir)

            # Set keyframe
            obj.keyframe_insert("rotation_euler", frame=scene.frame_current)

            # Add marker
            if marker_namerule != "No marker name":

                # Remove markers
                for marker in scene.timeline_markers:
                    if marker.frame == scene.frame_current:
                        scene.timeline_markers.remove(marker)

                # Add marker namerule
                marker_name = marker_namerule
                marker_name = marker_name.replace("%V%", str(signed_y))
                marker_name = marker_name.replace("%H%", str(signed_x))

                scene.timeline_markers.new(marker_name, frame=scene.frame_current)

            # Move next keyframe
            scene.frame_current += 1


class RADIALRENDERER_OT_insert_keyframes(bpy.types.Operator):
    """Insert rotation keyframes and add, if enabled, a marker to each showing the axis steps count"""

    bl_label = "Create Keyframes"
    bl_idname = "radialrenderer.insert_keyframes"

    def execute(self, context):

        scene = context.scene
        mytool = scene.my_tool

        global views
        views.clear()

        # Check dependencies

        if mytool.controller is None:
            self.report({"ERROR"}, prop.no_selected_error % "Controller")
            return {"FINISHED"}

        if mytool.controller not in set(bpy.context.scene.objects):
            self.report({"ERROR"}, prop.not_in_view_layer_error % "Controller")
            return {"FINISHED"}

        # Validation

        name = mytool.marker_name

        if name != "No marker name":

            if not prop.validate_file_name(name):
                self.report({"ERROR"}, prop.marker_name_error)
                return {"FINISHED"}

            if mytool.x_axis:
                if "%H%" not in name:

                    self.report({"ERROR"}, prop.marker_name_h_missing_error)
                    return {"FINISHED"}

            if mytool.y_axis:
                if "%V%" not in name:

                    self.report({"ERROR"}, prop.marker_name_v_missing_error)
                    return {"FINISHED"}

        obj = mytool.controller

        # Set start frame
        scene.frame_start = scene.frame_current

        # Rotate objects

        global initial_rotation
        initial_rotation = obj.rotation_euler.copy()

        if mytool.x_axis and mytool.y_axis:

            if mytool.x_turnaround and mytool.y_turnaround:

                # Use y_steps and x_steps
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    mytool.x_steps - 1,
                    mytool.x_clamped_angle,
                    mytool.y_rotation_axis,
                    mytool.y_steps - 1,
                    mytool.y_clamped_angle,
                    mytool.marker_name,
                )

            elif mytool.x_turnaround:

                # Use x_steps and up/down steps
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    mytool.x_steps - 1,
                    mytool.x_clamped_angle,
                    mytool.y_rotation_axis,
                    mytool.up_steps,
                    mytool.y_angle,
                    mytool.marker_name,
                )
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    mytool.x_steps - 1,
                    mytool.x_clamped_angle,
                    mytool.y_rotation_axis,
                    -mytool.down_steps,
                    mytool.y_angle,
                    mytool.marker_name,
                )

            elif mytool.y_turnaround:

                # Use y_steps and right/left steps
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    mytool.right_steps,
                    mytool.x_angle,
                    mytool.y_rotation_axis,
                    mytool.y_steps - 1,
                    mytool.y_clamped_angle,
                    mytool.marker_name,
                )
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    -mytool.left_steps,
                    mytool.x_angle,
                    mytool.y_rotation_axis,
                    mytool.y_steps - 1,
                    mytool.y_clamped_angle,
                    mytool.marker_name,
                )

            else:

                # Use right/left and up/down steps
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    mytool.right_steps,
                    mytool.x_angle,
                    mytool.y_rotation_axis,
                    mytool.up_steps,
                    mytool.y_angle,
                    mytool.marker_name,
                )
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    mytool.right_steps,
                    mytool.x_angle,
                    mytool.y_rotation_axis,
                    -mytool.down_steps,
                    mytool.y_angle,
                    mytool.marker_name,
                )
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    -mytool.left_steps,
                    mytool.x_angle,
                    mytool.y_rotation_axis,
                    mytool.up_steps,
                    mytool.y_angle,
                    mytool.marker_name,
                )
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    -mytool.left_steps,
                    mytool.x_angle,
                    mytool.y_rotation_axis,
                    -mytool.down_steps,
                    mytool.y_angle,
                    mytool.marker_name,
                )

        elif mytool.x_axis:

            if mytool.x_turnaround:

                # Use x_steps
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    mytool.x_steps - 1,
                    mytool.x_clamped_angle,
                    mytool.y_rotation_axis,
                    0,
                    0,
                    mytool.marker_name,
                )

            else:

                # Use right/left steps
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    mytool.right_steps,
                    mytool.x_angle,
                    mytool.y_rotation_axis,
                    0,
                    0,
                    mytool.marker_name,
                )
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    -mytool.left_steps,
                    mytool.x_angle,
                    mytool.y_rotation_axis,
                    0,
                    0,
                    mytool.marker_name,
                )

        elif mytool.y_axis:

            if mytool.y_turnaround:

                # Use y_steps
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    0,
                    0,
                    mytool.y_rotation_axis,
                    mytool.y_steps - 1,
                    mytool.y_clamped_angle,
                    mytool.marker_name,
                )

            else:

                # Use up/down steps
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    0,
                    0,
                    mytool.y_rotation_axis,
                    mytool.up_steps,
                    mytool.y_angle,
                    mytool.marker_name,
                )
                rotate_and_add_marker(
                    obj,
                    mytool.x_rotation_axis,
                    0,
                    0,
                    mytool.y_rotation_axis,
                    -mytool.down_steps,
                    mytool.y_angle,
                    mytool.marker_name,
                )
        else:

            # Export one frame
            rotate_and_add_marker(
                obj,
                mytool.x_rotation_axis,
                0,
                0,
                mytool.y_rotation_axis,
                0,
                0,
                mytool.marker_name,
            )

        # Set end frame
        scene.frame_end = scene.frame_current - 1

        # Move to start
        scene.frame_current = scene.frame_start

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_insert_keyframes,)
