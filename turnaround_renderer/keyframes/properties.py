import bpy

from math import degrees, radians


class Properties(bpy.types.PropertyGroup):

    # GETTER/SETTER
    # Horizontal Axis
    def set_x_mode(self, value):
        self["x_mode"] = value

    def get_x_mode(self):
        return self.get("x_mode", 0)

    # Turn Around
    def get_x_steps(self):
        return self.get("x_steps", 360)

    def set_x_steps(self, value):
        self["x_steps"] = value
        self["x_clamped_angle"] = radians(360 / value)

    def get_x_clamped_angle(self):
        return self.get("x_clamped_angle", radians(1))

    def set_x_clamped_angle(self, value):
        self["x_steps"] = round(360 / degrees(value))
        self["x_clamped_angle"] = radians(360 / self["x_steps"])

    # Custom
    def get_x_angle(self):
        return self.get("x_angle", radians(1))

    def set_x_angle(self, value):

        # Change angle
        self["x_angle"] = value

        # Change max steps
        angle = round(degrees(self["x_angle"]), 4)
        self["x_steps_max"] = 360 // angle
        if 360 % angle == 0:
            self["x_steps_max"] -= 1

        # Change right/left steps
        x_steps_total = self["right_steps"] + self["left_steps"]

        if x_steps_total > self["x_steps_max"]:

            # Distribute the max steps proportionally
            factor = self["x_steps_max"] / x_steps_total

            left_steps_new = int(self["left_steps"] * factor)
            right_steps_new = int(self["right_steps"] * factor)

            # Distribute the unit
            x_steps_total = left_steps_new + right_steps_new

            if x_steps_total < self["x_steps_max"]:

                if self["right_steps"] >= self["left_steps"]:
                    right_steps_new += 1
                else:
                    left_steps_new += 1

            self["left_steps"] = left_steps_new
            self["right_steps"] = right_steps_new

    def get_right_steps(self):
        return int(self.get("right_steps", 0))

    def set_right_steps(self, value):

        x_steps_max = self.get("x_steps_max", 259)

        # Clamp value to max steps
        value = max(0, min(value, x_steps_max))

        # Change right steps
        self["right_steps"] = value

        # Clamp left steps with the rest
        self["left_steps"] = max(
            0, min(self.left_steps, x_steps_max - self.right_steps)
        )

    def get_left_steps(self):
        return self.get("left_steps", 0)

    def set_left_steps(self, value):

        x_steps_max = self.get("x_steps_max", 259)

        # Clamp value to max steps
        value = max(0, min(value, x_steps_max))

        # Change left steps
        self["left_steps"] = value

        # Clamp right steps with the rest
        self["right_steps"] = max(
            0, min(self.right_steps, x_steps_max - self.left_steps)
        )

    # Vertical Axis
    def set_y_mode(self, value):
        self["y_mode"] = value

    def get_y_mode(self):
        return self.get("y_mode", 'TURNAROUND')

    # Turn Around
    def get_y_steps(self):
        return self.get("y_steps", 360)

    def set_y_steps(self, value):
        self["y_steps"] = value
        self["y_clamped_angle"] = radians(360 / value)

    def get_y_clamped_angle(self):
        return self.get("y_clamped_angle", radians(1))

    def set_y_clamped_angle(self, value):
        self["y_steps"] = round(360 / degrees(value))
        self["y_clamped_angle"] = radians(360 / self["y_steps"])

    # Custom
    def get_y_angle(self):
        return self.get("y_angle", radians(1))

    def set_y_angle(self, value):
        # Change angle
        self["y_angle"] = value

        # Change max steps
        angle = round(degrees(self["y_angle"]), 4)
        self["y_steps_max"] = 360 // angle
        if 360 % angle == 0:
            self["y_steps_max"] -= 1

        # Change up/down steps
        y_steps_total = self["up_steps"] + self["down_steps"]

        if y_steps_total > self["y_steps_max"]:

            # Distribute the max steps proportionally
            factor = self["y_steps_max"] / y_steps_total

            down_steps_new = int(self["down_steps"] * factor)
            up_steps_new = int(self["up_steps"] * factor)

            # Distribute the unit
            y_steps_total = down_steps_new + up_steps_new

            if y_steps_total < self["y_steps_max"]:

                if self["up_steps"] >= self["down_steps"]:
                    up_steps_new += 1
                else:
                    down_steps_new += 1

            self["down_steps"] = down_steps_new
            self["up_steps"] = up_steps_new

    def get_up_steps(self):
        return self.get("up_steps", 0)

    def set_up_steps(self, value):

        y_steps_max = self.get("y_steps_max", 259)

        # Clamp value to max steps
        value = max(0, min(value, y_steps_max))

        # Change up steps
        self["up_steps"] = value

        # Clamp down steps with the rest
        self["down_steps"] = max(
            0, min(self["down_steps"], y_steps_max - self["up_steps"])
        )

    def get_down_steps(self):
        return self.get("down_steps", 0)

    def set_down_steps(self, value):

        y_steps_max = self.get("y_steps_max", 259)

        # Clamp value to max steps
        value = max(0, min(value, y_steps_max))

        # Change down steps
        self["down_steps"] = value

        # Clamp up   steps with the rest
        self["up_steps"] = max(
            0, min(self["up_steps"], y_steps_max - self["down_steps"])
        )

    # Create keyframes

    def get_marker_name(self):
        return self.get("marker_name", "V{V}H{H}")

    def set_marker_name(self, value):
        self["marker_name"] = value
        self["marker_name_preview"] = value.replace(
            "{H}", "0", 1).replace("{V}", "1", 1)

    def get_marker_name_preview(self):
        return self.get("marker_name_preview", "V1H0")

    def get_views_count(self):
        x = 1
        y = 1

        if self.x_axis:
            if self.x_mode == 'TURNAROUND':
                x = self.x_steps
            else:
                x += self.right_steps + self.left_steps

        if self.y_axis:
            if self.y_mode == 'TURNAROUND':
                y = self.y_steps
            else:
                y += self.up_steps + self.down_steps

        return x * y

    def get_frame_end(self):
        scene = bpy.context.scene
        return scene.frame_current + self.views_count - 1

    # Keyframe Assistant
    key_obj: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="",
        description="Object to insert rotation keyframes",
    )

    # X Turnaround
    x_axis: bpy.props.BoolProperty(
        name="",
        default=False,
    )

    x_rotation_axis: bpy.props.EnumProperty(
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("-X", "-X", ""),
            ("-Y", "-Y", ""),
            ("-Z", "-Z", ""),
        ],
        name="Axis",
        description="Rotation Axis (default: Z)",
        default="Z",
    )

    x_mode: bpy.props.EnumProperty(
        name="Rotation mode",
        items={
            ('TURNAROUND', "Turnaround", "Turnaround mode", 0),
            ('MANUAL', "Manual", "Manual mode", 1)},
        default='TURNAROUND',
        get=get_x_mode,
        set=set_x_mode
    )

    x_steps: bpy.props.IntProperty(
        name="",
        min=1,
        max=360,
        default=1,
        get=get_x_steps,
        set=set_x_steps,
    )

    x_steps_max: bpy.props.IntProperty()

    # Y Turnaround
    y_axis: bpy.props.BoolProperty(
        name="",
        default=False,
    )

    y_rotation_axis: bpy.props.EnumProperty(
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("-X", "-X", ""),
            ("-Y", "-Y", ""),
            ("-Z", "-Z", ""),
        ],
        name="Axis",
        description="Rotation Axis (default: X)",
        default="X",
    )

    y_mode: bpy.props.EnumProperty(
        name="Rotation mode",
        items={
            ('TURNAROUND', "Turnaround", "Turnaround mode", 0),
            ('MANUAL', "Manual", "Manual mode", 1)},
        default='MANUAL',
        get=get_y_mode,
        set=set_y_mode
    )

    y_steps: bpy.props.IntProperty(
        name="",
        default=1,
        min=1,
        max=360,
        get=get_y_steps,
        set=set_y_steps,
    )

    y_steps_max: bpy.props.IntProperty()

    # X Custom
    x_angle: bpy.props.FloatProperty(
        name="",
        description="Angle of each step in Z",
        default=radians(1),
        min=radians(1),
        max=radians(359.99),
        precision=3,
        subtype="ANGLE",
        unit="ROTATION",
        get=get_x_angle,
        set=set_x_angle,
    )

    x_clamped_angle: bpy.props.FloatProperty(
        name="",
        description="Angle of each part in Z",
        default=radians(1),
        min=radians(1),
        max=radians(360),
        precision=3,
        subtype="ANGLE",
        unit="ROTATION",
        get=get_x_clamped_angle,
        set=set_x_clamped_angle,
    )

    right_steps: bpy.props.IntProperty(
        name="",
        description="Steps to rotate in +Z",
        default=0,
        min=0,
        max=359,
        get=get_right_steps,
        set=set_right_steps,
    )

    left_steps: bpy.props.IntProperty(
        name="",
        description="Steps to rotate in -Z",
        default=0,
        min=0,
        max=359,
        get=get_left_steps,
        set=set_left_steps,
    )

    # Y Custom
    y_angle: bpy.props.FloatProperty(
        name="",
        description="Angle of each step in X",
        default=radians(1),
        min=radians(1),
        max=radians(359.99),
        precision=3,
        subtype="ANGLE",
        unit="ROTATION",
        get=get_y_angle,
        set=set_y_angle,
    )

    y_clamped_angle: bpy.props.FloatProperty(
        name="",
        description="Angle of each part in X",
        default=radians(1),
        min=radians(1),
        max=radians(360),
        precision=3,
        subtype="ANGLE",
        unit="ROTATION",
        get=get_y_clamped_angle,
        set=set_y_clamped_angle,
    )

    up_steps: bpy.props.IntProperty(
        name="",
        description="Steps to rotate in +X",
        default=0,
        min=0,
        max=359,
        get=get_up_steps,
        set=set_up_steps,
    )

    down_steps: bpy.props.IntProperty(
        name="",
        description="Steps to rotate in -X",
        default=0,
        min=0,
        max=359,
        get=get_down_steps,
        set=set_down_steps,
    )

    # Insert keyframes
    views_count: bpy.props.IntProperty(
        default=1,
        get=get_views_count,
    )

    add_markers: bpy.props.BoolProperty(
        name="Add markers",
        default=True
    )

    marker_name: bpy.props.StringProperty(
        name="",
        description="Marker names (use {H} and {V} for horizontal and vertical values)",
        default="H{H}V{V}",
        maxlen=1024,
        subtype="FILE_NAME",
        get=get_marker_name,
        set=set_marker_name,
    )

    marker_name_preview: bpy.props.StringProperty(
        name="",
        description="Example marker name",
        default="V1H0",
        maxlen=1024,
        subtype="FILE_NAME",
        get=get_marker_name_preview,
    )

    frame_end: bpy.props.IntProperty(
        name="",
        description="End frame from last keyframe",
        get=get_frame_end,
    )


def register():
    bpy.utils.register_class(Properties)
    bpy.types.Scene.keyframes_properties = bpy.props.PointerProperty(type=Properties)


def unregister():
    del bpy.types.Scene.keyframes_properties
    bpy.utils.unregister_class(Properties)
