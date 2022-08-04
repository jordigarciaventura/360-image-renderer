import bpy


def shared_poll(context):
    # Objects are not None
    scene = context.scene
    props = scene.align_properties
    return props.from_obj and props.to_obj


def shared_preconditions_check(self, context):
    # Objects are in View Layer
    scene = context.scene
    props = scene.align_properties
    objects = [props.from_obj, props.to_obj]
    return check_are_in_view_layer(self, context, objects)


def check_are_in_view_layer(self, context, objects):
    msg = "%s does not exist in the View Layer"

    scene = context.scene
    scene_objects = set(scene.objects)

    for object in objects:
        if object not in scene_objects:
            self.report({'ERROR'}, msg % object.name)
            return False
    return True


class TURNAROUND_RENDERER_OT_align_rotation(bpy.types.Operator):
    """Align objects rotation"""

    bl_label = "Orientate"
    bl_idname = "turnaround_renderer.align_rotation"

    @classmethod
    def poll(self, context):
        return shared_poll(context)

    def execute(self, context):
        # Check preconditions
        if not shared_preconditions_check(self, context):
            return {'FINISHED'}

        scene = context.scene
        props = scene.align_properties

        # Align rotation
        props.from_obj.rotation_euler = props.to_obj.matrix_world.to_euler()

        return {'FINISHED'}


class TURNAROUND_RENDERER_OT_align_location(bpy.types.Operator):
    """Align objects location"""

    bl_label = "Align"
    bl_idname = "turnaround_renderer.align_location"

    @classmethod
    def poll(self, context):
        return shared_poll(context)

    def execute(self, context):
        # Check preconditions
        if not shared_preconditions_check(self, context):
            return {'FINISHED'}

        scene = context.scene
        props = scene.align_properties

        # Align location
        props.from_obj.location = props.to_obj.matrix_world.to_translation()

        return {'FINISHED'}


class TURNAROUND_RENDERER_OT_swap_align(bpy.types.Operator):
    """Swap align objects"""

    bl_label = "Swap"
    bl_idname = "turnaround_renderer.swap_align"

    @classmethod
    def poll(self, context):
        return shared_poll(context)

    def execute(self, context):
        # Check preconditions
        if not shared_preconditions_check(self, context):
            return {'FINISHED'}

        scene = context.scene
        props = scene.align_properties

        # Swap objects
        props.from_obj, props.to_obj = props.to_obj, props.from_obj

        return {'FINISHED'}


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
