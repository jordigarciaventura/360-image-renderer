import bpy


class RADIALRENDERER_PT_render(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "360 Renderer"
    bl_label = "Render"
    bl_idname = "RADIALRENDERER_PT_render"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.render_properties

        col = layout.column()

        # Path
        split = col.split(factor=0.2)
        split.alignment = 'RIGHT'
        split.label(text="Output")
        split.prop(scene.render, "filepath", text="")

        # Only selected
        col.separator(factor=1)
        split = col.split(factor=0.2)
        split.label(text="")
        split.prop(props, "only_selected", text="Only selected")
        split = col.split(factor=0.2)
        split.label(text="")
        split.prop(props, "transparent_background",
                   text="Transparent background")
        col.separator(factor=2)

        # Range
        row = col.row(align=True)
        row.use_property_split = False
        row.prop(scene, "frame_start", text="Start")
        row.prop(scene, "frame_end", text="End")

        col.separator()

        # Render frames
        row = col.row()
        row.scale_y = 1.5

        frame_count = 1 + scene.frame_end - scene.frame_start

        row.operator(
            "radialrenderer.export",
            text="Render {} frame{}".format(
                frame_count, 's' if frame_count != 1 else ''),
            icon='RENDER_ANIMATION'
        )


classes = (
    RADIALRENDERER_PT_render,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
