import bpy

from math import (
    radians,
    degrees,
)

from mathutils import Vector

from add_light_controller import add_light_controller

# Creates a Camera Controller and 3 Light Controllers. Returns the object
def add_camera_controller(context, location, radius):
    scene = context.scene

    # Create collection
    coll_name = "360 Viewer"
    coll = bpy.data.collections.new(coll_name)
    scene.collection.children.link(coll)

    # Select collection
    layer_coll = bpy.context.view_layer.layer_collection.children[coll.name]
    context.view_layer.active_layer_collection = layer_coll

    # CAMERA CONTROLLER

    # Create controller
    cam_controller = bpy.data.objects.new("Camera Controller", None)
    cam_controller.empty_display_type = "SPHERE"
    cam_controller.location = location
    cam_controller.scale = Vector((radius, radius, radius))
    coll.objects.link(cam_controller)

    # Create camera
    cam_data = bpy.data.cameras.new(name="Camera")
    cam = bpy.data.objects.new("Camera", cam_data)
    cam.location = location
    cam.rotation_euler = (radians(90), 0, 0)
    coll.objects.link(cam)

    # Add 'Transform' constraint
    light_transform = cam.constraints.new('TRANSFORM')
    light_transform.target = cam_controller
    light_transform.target_space = 'LOCAL'
    light_transform.owner_space = 'LOCAL'
    light_transform.map_from = 'SCALE'
    light_transform.from_min_y_scale = 0
    light_transform.from_max_y_scale = 100000
    light_transform.map_to = 'LOCATION'
    light_transform.map_to_z_from = 'Y'
    light_transform.to_max_z = 100000

    # Add 'Child of' constraint
    cam_child_of = cam.constraints.new('CHILD_OF')
    cam_child_of.target = cam_controller
    cam_child_of.use_scale_x = False
    cam_child_of.use_scale_y = False
    cam_child_of.use_scale_z = False

    # Lock camera transform
    cam.lock_location[0] = True
    cam.lock_location[1] = True
    cam.lock_location[2] = True
    cam.lock_rotation[0] = True
    cam.lock_rotation[1] = True
    cam.lock_rotation[2] = True
    cam.lock_scale[0] = True
    cam.lock_scale[1] = True
    cam.lock_scale[2] = True

    # LIGHT CONTROLLERS
    
    # Select controller
    for obj in context.selected_objects:
        obj.select_set(False)

    context.view_layer.objects.active = cam_controller
    cam_controller.select_set(True)

    # Return controller
    return cam_controller


class RADIALRENDERER_OT_add_camera_controller(bpy.types.Operator):
    """Add a pre-built camera controller"""

    bl_label = "Create Camera Controller"
    bl_idname = "radialrenderer.add_camera_controller"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        selected_objects = context.selected_objects

        # Calculate spawn location        
        spawn_location = Vector()
        if selected_objects:
            # Center point of all selected objects
            for obj in selected_objects:
                spawn_location += obj.location
            spawn_location /= len(selected_objects)
        else:
            spawn_location = context.scene.cursor.location.copy()

        # Calculate radius
        radius = 1
        if selected_objects:
          max_distance = max([(obj.location - spawn_location).magnitude for obj in selected_objects])
          radius = max(radius, max_distance)

        mytool.controller = mytool.from_obj = add_camera_controller(context, spawn_location, radius)

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_add_camera_controller,)

def register():
  for cls in classes:
    bpy.utils.register_class(cls)

def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)