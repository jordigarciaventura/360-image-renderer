import bpy

from .utils import isolate_selection, setup_transparent_background


class Properties(bpy.types.PropertyGroup):
    only_selected: bpy.props.BoolProperty(
        name="",
        description="Hide/Show non-selected renderable objects \
            in viewport and in render",
        default=False,
        update=lambda self, context: isolate_selection(
            context, self.only_selected),
    )

    transparent_background: bpy.props.BoolProperty(
        name="",
        description="Change/Restore render and output properties \
            for transparent background",
        default=False,
        update=lambda self, context: setup_transparent_background(
            context, self.transparent_background),
    )


def register():
    bpy.utils.register_class(Properties)
    bpy.types.Scene.render_properties = bpy.props.PointerProperty(
        type=Properties)


def unregister():
    del bpy.types.Scene.render_properties
    bpy.utils.unregister_class(Properties)
