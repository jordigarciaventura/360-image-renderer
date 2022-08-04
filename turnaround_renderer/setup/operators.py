import bpy

from .utils import (create_camera_controller, create_light_controller,
                    get_selection_center, get_selection_diameter)

not_in_view_layer_error = "The %s is not in the View Layer"


class TURNAROUND_RENDERER_OT_add_light_controller(bpy.types.Operator):
    """Add a pre-built light controller"""

    bl_label = "Create Light Controller"
    bl_idname = "turnaround_renderer.add_light_controller"

    @classmethod
    def poll(self, context):
        scene = context.scene
        props = scene.setup_properties
        return props.camera_pivot

    def execute(self, context):
        scene = context.scene
        props = scene.setup_properties
        camera_pivot = props.camera_pivot

        if camera_pivot not in set(scene.objects):
            self.report({'ERROR'}, not_in_view_layer_error % camera_pivot.name)
            return {'FINISHED'}

        # Create light controller
        coll, _, light_pivot = create_light_controller(camera_pivot)
        # Add inside camera controller
        camera_pivot.users_collection[0].children.link(coll)

        # Select controller
        for obj in context.selected_objects:
            obj.select_set(False)
        context.view_layer.objects.active = light_pivot
        light_pivot.select_set(True)

        return {'FINISHED'}


class TURNAROUND_RENDERER_OT_add_camera_controller(bpy.types.Operator):
    """Add a pre-built camera controller"""

    bl_label = "Create Camera Controller"
    bl_idname = "turnaround_renderer.add_camera_controller"

    def execute(self, context):
        scene = context.scene
        props = scene.setup_properties

        # Calculate spawn location
        spawn_location = get_selection_center(context)
        # Calculate diamater
        radius = get_selection_diameter(context, spawn_location)

        # Add camera controller
        coll, _, camera_pivot = create_camera_controller(
            spawn_location, radius)
        scene.collection.children.link(coll)  # Add to scene

        # Select camera pivot
        for obj in context.selected_objects:
            obj.select_set(False)
        context.view_layer.objects.active = camera_pivot
        camera_pivot.select_set(True)

        # Prefill camera pivot input
        props.camera_pivot = camera_pivot

        return {'FINISHED'}


classes = (
    TURNAROUND_RENDERER_OT_add_light_controller,
    TURNAROUND_RENDERER_OT_add_camera_controller
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
