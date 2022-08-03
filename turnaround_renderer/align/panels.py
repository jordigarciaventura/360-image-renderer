import bpy


class RADIALRENDERER_PT_align(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "360 Renderer"
    bl_label = "Align"
    bl_idname = "RADIALRENDERER_PT_align"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.align_properties

        col = layout.column()

        box = col.box()

        sub = box.column(align=True)

        split = sub.split(factor=0.2)
        split.alignment = 'RIGHT'
        split.label(text="From")
        split.prop(props, "from_obj")
        sub.separator()
        split = sub.split(factor=0.2)
        split.alignment = 'RIGHT'
        split.label(text="To")
        split.prop(props, "to_obj")
        sub.separator(factor=2)
        sub.operator("radialrenderer.swap_align", text="Swap")

        col.separator(factor=1)
        sub = col.column()
        sub.scale_y = 1.5
        sub.operator("radialrenderer.align_location",
                     text="Align Location", icon="EMPTY_AXIS")
        sub.operator("radialrenderer.align_rotation",
                     text="Align Rotation", icon="ORIENTATION_GIMBAL")


classes = (
    RADIALRENDERER_PT_align,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
