import imp


import bpy


class RADIALRENDERER_PT_keyframe_assistant(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "360 Renderer"
    bl_label = "Keyframe Assistant"
    bl_idname = "RADIALRENDERER_PT_keyframe_assistant"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.keyframes_properties

        col = layout.column()

        # Object
        split = col.split(factor=0.2)
        split.alignment = 'RIGHT'
        split.label(text="Object")
        split.prop(props, "key_obj")
        col.separator()

        # Markers name
        box = col.box()
        row = box.row(align=True)
        row.prop(props, "add_markers", text="")
        row.label(text="Marker name")
        sub = box.column(align=True)
        sub.enabled = props.add_markers
        sub.prop(props, "marker_name")
        sub.prop(props, "marker_name_preview")

        col.separator()

        # Horizontal Axis
        box = col.box()

        split = box.split(factor=0.7, align=True)
        row = split.row(align=True)
        row.prop(props, "x_axis")
        row.label(text="Horizontal Axis")
        split.prop(props, "x_rotation_axis", text="")

        if props.x_axis:
            box.row().prop(props, "x_mode", expand=True)
            subcol = box.column(align=True)
            # Parts/Angle
            if props.x_mode == 'TURNAROUND':
                subcol.prop(props, "x_clamped_angle", text="Angle")
                subcol.prop(props, "x_steps", text="Parts")
            # Angle/LeftSteps/RightSteps
            else:
                subcol.prop(props, "x_angle", text="Angle")
                subcol.prop(props, "left_steps", text="Left Steps")
                subcol.prop(props, "right_steps", text="Right Steps")

        # Vertical Axis
        box = col.box()

        split = box.split(factor=0.7, align=True)
        row = split.row(align=True)
        row.prop(props, "y_axis")
        row.label(text="Vertical Axis")
        split.prop(props, "y_rotation_axis", text="")

        if props.y_axis:

            box.row().prop(props, "y_mode", expand=True)

            subcol = box.column(align=True)

            # Parts/Angle
            if props.y_mode == 'TURNAROUND':
                subcol.prop(props, "y_clamped_angle", text="Angle")
                subcol.prop(props, "y_steps", text="Parts")

            # Angle/UpSteps/DownSteps
            else:
                subcol.prop(props, "y_angle", text="Angle")
                subcol.prop(props, "up_steps", text="Up Steps")
                subcol.prop(props, "down_steps", text="Down Steps")

        col.separator(factor=2)

        row = col.row(align=True)
        row.prop(scene, "frame_current", text="Start")
        row.prop(props, "frame_end", text="End")

        # Insert keyframes
        col.separator()

        row = col.row()
        row.scale_y = 1.5
        row.operator(
            "radialrenderer.insert_keyframes",
            text="Insert {} keyframe{}".format(
                props.views_count, 's' if props.views_count != 1 else ''),
            icon='DECORATE_KEYFRAME',
        )


classes = (
    RADIALRENDERER_PT_keyframe_assistant,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
