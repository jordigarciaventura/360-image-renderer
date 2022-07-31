from cgitb import text
import bpy

import properties as prop


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

        col = layout.column()

        # Add camera controller

        sub = col.row()
        sub.scale_y = 1.2
        sub.operator("radialrenderer.add_camera_controller", text="Add camera controller")

        col.separator()

        # Controller

        box = col.box()

        split = box.split(align=True, factor=0.4)
        split.alignment = "RIGHT"

        split.label(text="Camera controller")
        split.prop(mytool, "controller", icon='SPHERE')
        
        # Add light controller
                
        box.operator("radialrenderer.add_light_controller", text="Add light controller")


class RADIALRENDERER_PT_align(bpy.types.Panel, RADIALRENDERER_panel):
    bl_label = "Align"
    bl_idname = "RADIALRENDERER_PT_align"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        col = layout.column()
        
        box = col.box()

        sub = box.column(align=True)

        split = sub.split(factor=0.2)
        split.alignment='RIGHT'
        split.label(text="From")
        split.prop(mytool, "from_obj")
        sub.separator()
        split = sub.split(factor=0.2)
        split.alignment='RIGHT'
        split.label(text="To")
        split.prop(mytool, "to_obj")
        sub.separator(factor=2)
        sub.operator("radialrenderer.swap_align", text="Swap")
                
        col.separator(factor=1)
        col.operator("radialrenderer.align_location", text="Align Location")
        col.operator("radialrenderer.align_rotation", text="Align Rotation")
 

class RADIALRENDERER_PT_keyframe_assistant(bpy.types.Panel, RADIALRENDERER_panel):
    bl_label = "Keyframe Assistant"
    bl_idname = "RADIALRENDERER_PT_keyframe_assistant"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        col = layout.column()

        # Object
        split = col.split(factor=0.2)
        split.alignment = 'RIGHT'
        split.label(text="Object")
        split.prop(mytool, "key_obj")

        col.separator()
        
        col.label(text="Keyframes")
        # Horizontal Axis
        box = col.box()
        
        split = box.split(factor=0.7, align=True)
        row = split.row(align=True)
        row.prop(mytool, "x_axis") 
        row.label(text="Horizontal Axis")
        split.prop(mytool, "x_rotation_axis", text="")
        
        if mytool.x_axis:
          box.row().prop(mytool, "x_mode", expand=True)
          subcol = box.column(align=True)
          # Parts/Angle
          if mytool.x_mode == 'TURNAROUND':
              subcol.prop(mytool, "x_clamped_angle", text="Angle")
              subcol.prop(mytool, "x_steps", text="Parts")
          # Angle/LeftSteps/RightSteps
          else:
              subcol.prop(mytool, "x_angle", text="Angle")
              subcol.prop(mytool, "left_steps", text="Left Steps")
              subcol.prop(mytool, "right_steps", text="Right Steps")

        # Vertical Axis     
        box = col.box()
                
        split = box.split(factor=0.7, align=True)
        row = split.row(align=True)
        row.prop(mytool, "y_axis") 
        row.label(text="Vertical Axis")
        split.prop(mytool, "y_rotation_axis", text="")
                                      
        if mytool.y_axis:
                
          box.row().prop(mytool, "y_mode", expand=True)

          subcol = box.column(align=True)

          # Parts/Angle
          if mytool.y_mode == 'TURNAROUND':
              subcol.prop(mytool, "y_clamped_angle", text="Angle")
              subcol.prop(mytool, "y_steps", text="Parts")

          # Angle/UpSteps/DownSteps
          else:
              subcol.prop(mytool, "y_angle", text="Angle")
              subcol.prop(mytool, "up_steps", text="Up Steps")
              subcol.prop(mytool, "down_steps", text="Down Steps")        
        
        # Markers name
        col.separator()

        sub = col.column(align=True)
        sub.label(text="Marker names")
        split = sub.split(factor=0.2)
        split.alignment = 'RIGHT'
        split.label(text="Format")
        split.prop(mytool, "marker_name")
        split = sub.split(factor=0.2)
        split.alignment = 'RIGHT'
        split.label(text="Preview")
        split.prop(mytool, "marker_name_preview")

        col.separator(factor=2)

        row = col.row(align=True)
        row.prop(scene, "frame_current", text="Start")
        row.prop(mytool, "frame_end", text="End")

        # Insert keyframes
        col.separator()

        row = col.row()
        row.scale_y = 1.5
        row.operator(
            "radialrenderer.insert_keyframes",
            text="Insert {} {}".format(str(mytool.views_count), "keyframes" if mytool.views_count > 1 else "keyframe"),
            icon='DECORATE_KEYFRAME',
        )


class RADIALRENDERER_PT_render(bpy.types.Panel, RADIALRENDERER_panel):
    bl_label = "Render"
    bl_idname = "RADIALRENDERER_PT_render"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        col = layout.column()

        # Path
        split = col.split(factor=0.2)
        split.alignment = 'RIGHT'
        split.label(text="Output")
        split.prop(scene.render, "filepath", text="")

        # Only selected
        col.separator(factor=1)
        row = col.row()
        row.alignment = 'RIGHT'
        row.prop(mytool, "only_selected", text="Only selected")

        col.separator(factor=2)

        # Range
        row = col.row(align=True)
        row.prop(scene, "frame_start", text="Start")
        row.prop(scene, "frame_end", text="End")

        col.separator()

        # Render frames
        row = col.row()
        row.scale_y = 1.5

        frame_count = scene.frame_end - scene.frame_start

        row.operator(
            "radialrenderer.export",
            text="Render {} frame{}".format(frame_count, "s" if frame_count != 1 else ""),
            icon_value=prop.icons["frames"].icon_id,
        )


classes = (
    RADIALRENDERER_PT_setup,
    RADIALRENDERER_PT_align,
    RADIALRENDERER_PT_keyframe_assistant,
    RADIALRENDERER_PT_render,
)

def register():
  for cls in classes:
    bpy.utils.register_class(cls)

def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)