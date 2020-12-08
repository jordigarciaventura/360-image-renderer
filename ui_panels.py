import bpy

from . import properties as prop


class RADIALRENDERER_panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "360 Renderer"


class RADIALRENDERER_PT_setup(bpy.types.Panel, RADIALRENDERER_panel):
    bl_label = "Setup"
    bl_idname = "RADIALRENDERER_PT_setup"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        # Add controller

        row = layout.row()
        row.operator("radialrenderer.create_preset", text="Add controller")

        # Controller

        row = layout.split(factor=0.4, align=True)
        row.alignment = "RIGHT"

        row.label(text="Controller", icon_value=prop.icons["controller"].icon_id)
        row.prop(mytool, "controller", icon_value=prop.icons["none"].icon_id)


class RADIALRENDERER_PT_align(bpy.types.Panel, RADIALRENDERER_panel):
    bl_label = "Align"
    bl_idname = "RADIALRENDERER_PT_align"
    bl_parent_id = "RADIALRENDERER_PT_setup"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        # Object

        row = layout.split(factor=0.4, align=True)
        row.alignment = "RIGHT"
        row.label(text="Object", icon_value=prop.icons["object"].icon_id)

        row.prop(mytool, "obj", icon_value=prop.icons["none"].icon_id)

        # Controller --> Object

        layout.separator(factor=1)

        box = layout.box()

        if mytool.controller is None or mytool.obj is None:
            box.enabled = False
        else:
            box.enabled = True

        row = box.row(align=True)
        row.alignment = "CENTER"

        row.label(text="Controller")

        if mytool.controller_to_obj:
            row.prop(
                mytool,
                "controller_to_obj",
                text="",
                icon_value=prop.icons["right"].icon_id,
            )
        else:
            row.prop(
                mytool,
                "controller_to_obj",
                text="",
                icon_value=prop.icons["left"].icon_id,
            )

        row.label(text="    Object")

        # Location/Rotation

        row = box.row(align=True)

        row.operator("radialrenderer.align_location", text="Location")
        row.operator("radialrenderer.align_rotation", text="Rotation")


class RADIALRENDERER_PT_keyframe_assistant(bpy.types.Panel, RADIALRENDERER_panel):
    bl_label = "Keyframe Assistant"
    bl_idname = "RADIALRENDERER_PT_keyframe_assistant"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        # Horizontal Axis

        row = layout.split(factor=0.7, align=True)
        row.alignment = "LEFT"

        row.prop(mytool, "x_axis", text="Horizontal Axis")
        row.prop(mytool, "x_rotation_axis", text="")

        # Turn Around
        if mytool.x_axis:

            box = layout.box()

            row = box.row(align=True)
            row.alignment = "RIGHT"

            row.label(icon_value=prop.icons["turnaround"].icon_id, text="Turn Around")
            row.prop(mytool, "x_turnaround")

            # Parts/Angle
            if mytool.x_turnaround:

                box.separator(factor=2.25)
                row = box.row(align=True)

                row1 = row.row()
                row1.alignment = "CENTER"
                row1.label(icon_value=prop.icons["parts"].icon_id, text="Parts")

                row2 = row.row()
                row2.alignment = "CENTER"
                row2.label(icon_value=prop.icons["angle"].icon_id, text="Angle")

                row = box.row(align=True)
                row.prop(mytool, "x_steps")
                row.prop(mytool, "x_clamped_angle")

            # Angle/RightSteps/LeftSteps
            else:
                box = layout.box()
                col = box.column(align=True)

                row = col.split(factor=0.5, align=True)
                row.alignment = "RIGHT"
                row.label(icon_value=prop.icons["angle"].icon_id, text="Angle")
                row.prop(mytool, "x_angle")

                row = col.split(factor=0.5, align=True)
                row.alignment = "RIGHT"
                row.label(icon_value=prop.icons["right"].icon_id, text="Right Steps")
                row.prop(mytool, "right_steps")

                row = col.split(factor=0.5, align=True)
                row.alignment = "RIGHT"
                row.label(icon_value=prop.icons["left"].icon_id, text="Left Steps")
                row.prop(mytool, "left_steps")

            layout.separator(factor=1)

        # Vertical Axis
        row = layout.split(factor=0.7, align=True)
        row.alignment = "LEFT"

        row.prop(mytool, "y_axis", text="Vertical Axis")
        row.prop(mytool, "y_rotation_axis", text="")

        # Turn Around
        if mytool.y_axis:

            box = layout.box()

            row = box.row(align=True)
            row.alignment = "RIGHT"

            row.label(icon_value=prop.icons["turnaround"].icon_id, text="Turn Around")
            row.prop(mytool, "y_turnaround")

            # Parts/Angle
            if mytool.y_turnaround:

                box.separator(factor=2.25)
                row = box.row(align=True)

                row1 = row.row()
                row1.alignment = "CENTER"
                row1.label(icon_value=prop.icons["parts"].icon_id, text="Parts")

                row2 = row.row()
                row2.alignment = "CENTER"
                row2.label(icon_value=prop.icons["angle"].icon_id, text="Angle")

                row = box.row(align=True)
                row.prop(mytool, "y_steps")
                row.prop(mytool, "y_clamped_angle")

            # Angle/UpSteps/DownSteps
            else:
                box = layout.box()
                col = box.column(align=True)

                row = col.split(factor=0.5, align=True)
                row.alignment = "RIGHT"
                row.label(icon_value=prop.icons["angle"].icon_id, text="Angle")
                row.prop(mytool, "y_angle")

                row = col.split(factor=0.5, align=True)
                row.alignment = "RIGHT"
                row.label(icon_value=prop.icons["up"].icon_id, text="Up Steps")
                row.prop(mytool, "up_steps")

                row = col.split(factor=0.5, align=True)
                row.alignment = "RIGHT"
                row.label(icon_value=prop.icons["down"].icon_id, text="Down Steps")
                row.prop(mytool, "down_steps")

        # Markers name

        layout.separator(factor=4)

        row = layout.split(factor=0.6, align=True)
        row.prop(mytool, "marker_name")
        row.prop(mytool, "marker_name_preview")

        # Views count

        layout.separator(factor=1)

        row = layout.row(align=True)
        row.alignment = "RIGHT"
        row.label(text="Views count: " + str(mytool.views_count))

        # Insert keyframes

        row = layout.row()
        row.scale_y = 1.5
        row.operator(
            "radialrenderer.insert_keyframes",
            text="Insert keyframes",
            icon_value=prop.icons["keyframe"].icon_id,
        )


class RADIALRENDERER_PT_render(bpy.types.Panel, RADIALRENDERER_panel):
    bl_label = "Render"
    bl_idname = "RADIALRENDERER_PT_render"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        # Path

        layout.scale_y = 1

        row = layout.row()
        row.prop(mytool, "path")

        # Only selected

        row = layout.row()
        row.prop(mytool, "only_selected", text="Only selected")

        layout.separator(factor=2)

        # Frames count

        row = layout.row(align=True)
        row.alignment = "RIGHT"
        row.label(text="Frames count: " + str(mytool.frames_count))

        # Export frames

        row = layout.row()
        row.scale_y = 1.5

        row.operator(
            "radialrenderer.export",
            text="Render frames",
            icon_value=prop.icons["frames"].icon_id,
        )


# ----------------------------------------------------------------------------------------------------------
#    Registration
# ----------------------------------------------------------------------------------------------------------


classes = (
    RADIALRENDERER_PT_setup,
    RADIALRENDERER_PT_align,
    RADIALRENDERER_PT_keyframe_assistant,
    RADIALRENDERER_PT_render,
)
