import bpy

from math import radians
from mathutils import Vector


def create_light_controller(parent):
    # Create light pivot
    light_pivot = bpy.data.objects.new("Light Pivot", None)
    light_pivot.empty_display_type = 'SPHERE'
    light_pivot.location = parent.location
    light_pivot.rotation_euler = parent.rotation_euler.copy()
    light_pivot.scale = parent.scale * 0.8

    # Add 'Child of' constraint
    light_child_of = light_pivot.constraints.new('CHILD_OF')
    light_child_of.target = parent
    light_child_of.use_scale_x = False
    light_child_of.use_scale_y = False
    light_child_of.use_scale_z = False

    # Create light
    light_data = bpy.data.lights.new("Light", type="AREA")
    light = bpy.data.objects.new("Light", light_data)
    light.location = parent.location
    light.rotation_euler = parent.rotation_euler.copy()
    light.rotation_euler.rotate_axis('X', radians(90))
    light.scale = light_pivot.scale * 4

    # Add 'Transform' constraint
    light_transform = light.constraints.new('TRANSFORM')
    light_transform.target = light_pivot
    light_transform.target_space = 'LOCAL'
    light_transform.owner_space = 'LOCAL'
    light_transform.map_from = 'SCALE'
    light_transform.from_min_y_scale = 0
    light_transform.from_max_y_scale = 100000
    light_transform.map_to = 'LOCATION'
    light_transform.map_to_z_from = 'Y'
    light_transform.to_max_z = 100000

    # Add 'Child of' constraint
    light_child_of = light.constraints.new('CHILD_OF')
    light_child_of.target = light_pivot
    light_child_of.use_scale_x = False
    light_child_of.use_scale_y = False
    light_child_of.use_scale_z = False

    # Lock transforms
    light.lock_location[0] = True
    light.lock_location[1] = True
    light.lock_location[2] = True
    light.lock_rotation[0] = True
    light.lock_rotation[1] = True
    light.lock_rotation[2] = True

    # Add to collection
    collection = bpy.data.collections.new("Light Controller")
    collection.objects.link(light_pivot)
    collection.objects.link(light)

    return collection, light, light_pivot


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
