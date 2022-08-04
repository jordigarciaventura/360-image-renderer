import bpy


class Properties(bpy.types.PropertyGroup):
    from_obj: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="",
        description="Object to align from"
    )

    to_obj: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="",
        description="Object to align to"
    )


def register():
    bpy.utils.register_class(Properties)
    bpy.types.Scene.align_properties = bpy.props.PointerProperty(
        type=Properties)


def unregister():
    del bpy.types.Scene.align_properties
    bpy.utils.unregister_class(Properties)
