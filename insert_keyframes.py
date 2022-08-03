import bpy

import properties as prop


def rotate_and_add_markers(context, obj,
                           x_angle, x_axis, x_min, x_max,
                           y_angle, y_axis, y_min, y_max,
                           add_markers, format, x_show_sign, y_show_sign):
    """
    Views: 0,0 is the initial view

           y_min        y_max
           ----- -----  -----
    x_min |-1,-1  0,-1   1,-1
          |-1, 0  0, 0   1, 0
    x_max |-1, 1  0, 1   1, 1
    """

    scene = context.scene

    # Start at top left
    x = x_min
    y = y_min
    rotation = obj.rotation_euler.copy()
    rotate_axis(rotation, x_axis, x_angle * x_min)
    rotate_axis(rotation, y_axis, y_angle * y_min)
    obj.rotation_euler = rotation.copy()

    # Iterate through the matrix
    while x <= x_max:
        while y <= y_max:
            # Insert keyframe
            obj.keyframe_insert("rotation_euler", frame=scene.frame_current)
            # Insert marker
            if add_markers:
                marker_name = format_marker_name(
                    format, x, y, x_show_sign, y_show_sign)
                add_marker(context, marker_name)
            # Rotate object
            scene.frame_current += 1
            rotate_axis(obj.rotation_euler, y_axis, y_angle)
            y += 1

        # Set object rotation to the first column of the next row
        rotate_axis(rotation, x_axis, x_angle)
        obj.rotation_euler = rotation.copy()
        y = y_min  # Reset y
        x += 1


def rotate_axis(rotation_euler, axis, value):
    if axis.startswith("-"):
        rotation_euler.rotate_axis(axis[1:], value * -1)
    else:
        rotation_euler.rotate_axis(axis, value)


def format_marker_name(format, x, y, x_show_sign, y_show_sign):
    if x_show_sign and x > 0:
        x = f"+{x}"
    if y_show_sign and y > 0:
        y = f"+{y}"
    marker_name = format
    marker_name = marker_name.replace("{H}", str(x))
    marker_name = marker_name.replace("{V}", str(y))
    return marker_name


def add_marker(context, name):
    scene = context.scene
    frame = scene.frame_current

    # One marker per frame, so remove if existing
    for marker in scene.timeline_markers:
        if marker.frame == frame:
            scene.timeline_markers.remove(marker)

    scene.timeline_markers.new(name, frame=frame)


class RADIALRENDERER_OT_insert_keyframes(bpy.types.Operator):
    """Insert rotation keyframes and add, if enabled, a marker to each
    showing the axis steps count"""

    bl_label = "Create Keyframes"
    bl_idname = "radialrenderer.insert_keyframes"

    @classmethod
    def poll(self, context):
        scene = context.scene
        mytool = scene.my_tool

        if mytool.key_obj is None:
            return False

        if mytool.key_obj not in set(bpy.context.scene.objects):
            return False

        return True

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        if not prop.validate_file_name(mytool.marker_name):
            self.report({"ERROR"}, prop.marker_name_error)
            return {"FINISHED"}

        # Necessary parameters
        obj = mytool.key_obj
        x_turnaround = mytool.x_mode == 'TURNAROUND'
        x_angle = mytool.x_clamped_angle if x_turnaround else mytool.x_angle
        x_axis = mytool.x_rotation_axis
        x_min = 0 if x_turnaround else -mytool.left_steps
        x_max = mytool.x_steps - 1 if x_turnaround else mytool.right_steps
        if not mytool.x_axis:
            x_min = x_max = 0
        y_turnaround = mytool.y_mode == 'TURNAROUND'
        y_angle = mytool.y_clamped_angle if y_turnaround else mytool.y_angle
        y_axis = mytool.y_rotation_axis
        y_min = 0 if y_turnaround else -mytool.down_steps
        y_max = mytool.y_steps - 1 if y_turnaround else mytool.up_steps
        if not mytool.y_axis:
            y_min = y_max = 0
        add_markers = mytool.add_markers
        format = mytool.marker_name
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

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_insert_keyframes,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
