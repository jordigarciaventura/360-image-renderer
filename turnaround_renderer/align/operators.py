import bpy


class TURNAROUND_RENDERER_OT_align_rotation(bpy.types.Operator):
    """Align objects rotation"""

    bl_label = "Orientate"
    bl_idname = "turnaround_renderer.align_rotation"

    @classmethod
    def poll(self, context):
        scene = context.scene
        properties = scene.align_properties

        if properties.from_obj not in set(scene.objects):
            return False
        if properties.to_obj not in set(scene.objects):
            return False

        return True

    def execute(self, context):
        scene = context.scene
        props = scene.align_properties
        # Align rotation
        props.from_obj.rotation_euler = props.to_obj.matrix_world.to_euler()

        return {"FINISHED"}


class TURNAROUND_RENDERER_OT_align_location(bpy.types.Operator):
    """Align objects location"""

    bl_label = "Align"
    bl_idname = "turnaround_renderer.align_location"

    @classmethod
    def poll(self, context):
        scene = context.scene
        props = scene.align_properties

        if props.from_obj not in set(scene.objects):
            return False
        if props.to_obj not in set(scene.objects):
            return False

        return True

    def execute(self, context):
        scene = context.scene
        props = scene.align_properties
        # Align location
        props.from_obj.location = props.to_obj.matrix_world.to_translation()

        return {"FINISHED"}


class TURNAROUND_RENDERER_OT_swap_align(bpy.types.Operator):
    """Swap align objects"""

    bl_label = "Swap"
    bl_idname = "turnaround_renderer.swap_align"

    @classmethod
    def poll(self, context):
        scene = context.scene
        props = scene.align_properties

        if props.from_obj not in set(scene.objects):
            return False
        if props.to_obj not in set(scene.objects):
            return False

        return True

    def execute(self, context):
        scene = context.scene
        props = scene.align_properties
        # Swap objects
        props.from_obj, props.to_obj = props.to_obj, props.from_obj

        return {"FINISHED"}


classes = (
    TURNAROUND_RENDERER_OT_swap_align,
    TURNAROUND_RENDERER_OT_align_rotation,
    TURNAROUND_RENDERER_OT_align_location
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
