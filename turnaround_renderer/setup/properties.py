import bpy


class Properties(bpy.types.PropertyGroup):
    controller: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="",
        description="Controller to rotate",
    )


def register():
    bpy.utils.register_class(Properties)
    bpy.types.Scene.setup_properties = bpy.props.PointerProperty(type=Properties)


def unregister():
    del bpy.types.Scene.setup_properties
    bpy.utils.unregister_class(Properties)
