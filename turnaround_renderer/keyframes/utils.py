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
