import bpy

from math import radians

from mathutils import Vector

# Creates a Camera Controller and 3 Light Controllers. Returns the object


def create_camera_controller(location, radius):
    # Create camera pivot
    camera_pivot = bpy.data.objects.new("Camera Pivot", None)
    camera_pivot.empty_display_type = "SPHERE"
    camera_pivot.location = location
    camera_pivot.scale = Vector((radius, radius, radius))

    # Create camera
    camera_data = bpy.data.cameras.new(name="Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    camera.location = location
    camera.rotation_euler = (radians(90), 0, 0)

    # Add 'Transform' constraint
    light_transform = camera.constraints.new('TRANSFORM')
    light_transform.target = camera_pivot
    light_transform.target_space = 'LOCAL'
    light_transform.owner_space = 'LOCAL'
    light_transform.map_from = 'SCALE'
    light_transform.from_min_y_scale = 0
    light_transform.from_max_y_scale = 100000
    light_transform.map_to = 'LOCATION'
    light_transform.map_to_z_from = 'Y'
    light_transform.to_max_z = 100000

    # Add 'Child of' constraint
    cam_child_of = camera.constraints.new('CHILD_OF')
    cam_child_of.target = camera_pivot
    cam_child_of.use_scale_x = False
    cam_child_of.use_scale_y = False
    cam_child_of.use_scale_z = False

    # Lock camera transform
    camera.lock_location[0] = True
    camera.lock_location[1] = True
    camera.lock_location[2] = True
    camera.lock_rotation[0] = True
    camera.lock_rotation[1] = True
    camera.lock_rotation[2] = True
    camera.lock_scale[0] = True
    camera.lock_scale[1] = True
    camera.lock_scale[2] = True

    # Add to collection
    collection = bpy.data.collections.new("Camera Controller")
    collection.objects.link(camera)
    collection.objects.link(camera_pivot)

    # Return controller
    return collection, camera, camera_pivot


def vector_mean(vectors):
    total = Vector()
    for vector in vectors:
        total += vector
    return total / len(vectors)


def get_selection_center(context):
    selected_objects = context.selected_objects
    if selected_objects:
        return vector_mean([obj.location for obj in selected_objects])
    else:
        return context.scene.cursor.location.copy()


def get_selection_diameter(context, center):
    selected_objects = context.selected_objects

    if not selected_objects:
        return 1

    if len(selected_objects) == 1:
        if hasattr(selected_objects[0], "dimensions"):
            max_dimension = max(selected_objects[0].dimensions)
            return max(1, max_dimension)
        return 1

    distances = [(obj.location - center).magnitude for obj in selected_objects]
    max_distance = max(distances)
    return max_distance * 2


class RADIALRENDERER_OT_add_camera_controller(bpy.types.Operator):
    """Add a pre-built camera controller"""

    bl_label = "Create Camera Controller"
    bl_idname = "radialrenderer.add_camera_controller"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        # Calculate spawn location
        spawn_location = get_selection_center(context)
        # Calculate diamater
        radius = get_selection_diameter(context, spawn_location)

        # Add camera controller
        coll, _, camera_pivot = create_camera_controller(
            spawn_location, radius)
        scene.collection.children.link(coll)  # Add to scene

        # Select controller
        for obj in context.selected_objects:
            obj.select_set(False)
        context.view_layer.objects.active = camera_pivot
        camera_pivot.select_set(True)

        # Prefill user inputs
        mytool.controller = camera_pivot
        mytool.from_obj = camera_pivot
        mytool.key_obj = camera_pivot

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_add_camera_controller,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
