import bpy


class RADIALRENDERER_PT_setup(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "360 Renderer"
    bl_label = "Setup"
    bl_idname = "RADIALRENDERER_PT_setup"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.setup_properties

        col = layout.column()

        # Add camera controller
        sub = col.row()
        sub.scale_y = 1.5
        sub.operator("radialrenderer.add_camera_controller",
                     text="Add camera controller", icon='OUTLINER_OB_CAMERA')

        col.separator()

        # Controller
        box = col.box()

        split = box.split(align=True, factor=0.4)
        split.alignment = "RIGHT"

        split.label(text="Camera pivot")
        split.prop(props, "controller", icon='CON_CAMERASOLVER')

        # Add light controller
        box.operator("radialrenderer.add_light_controller",
                     text="Add light controller")


classes = (
    RADIALRENDERER_PT_setup,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
