import bpy

from math import (
    radians,
    degrees,
)

from mathutils import Vector

# Creates a Camera Controller and 3 Light Controllers. Returns the object
def create_controller(self, context, controller_location):
    def add_light_controller(name, rotation, parent):

        # Create controller
        controller = bpy.data.objects.new(name + " Light Controller", None)
        controller.empty_display_type = "CIRCLE"
        controller.empty_display_size = 0.3
        controller.rotation_euler = rotation
        context.collection.objects.link(controller)

        # Create light
        light_data = bpy.data.lights.new(name + " Light", type="AREA")
        light = bpy.data.objects.new(name + " Light", light_data)
        light.location = (0, -0.000001, 0)
        light.rotation_euler = (radians(90), 0, 0)
        context.collection.objects.link(light)

        # Set constraints

        controller_limitscale = controller.constraints.new("LIMIT_SCALE")
        controller_limitscale.use_min_x = True
        controller_limitscale.min_x = 1
        controller_limitscale.use_max_x = True
        controller_limitscale.max_x = 1
        controller_limitscale.use_min_y = True
        controller_limitscale.min_y = 1
        controller_limitscale.use_max_y = True
        controller_limitscale.max_y = 1
        controller_limitscale.use_min_z = True
        controller_limitscale.min_z = 1
        controller_limitscale.use_max_z = True
        controller_limitscale.max_z = 1

        # Set custom properties

        if not controller.get("_RNA_UI"):
            controller["_RNA_UI"] = {}

        controller["Light distance"] = 1.0

        controller["_RNA_UI"]["Light distance"] = {
            "description": "Distance to light",
            "default": 1,
            "min": 0.0,
            "max": 1000000000,
        }

        # Set driver

        location_driver = light.driver_add("location", 1)
        self.drivers.add(location_driver)

        var = location_driver.driver.variables.new()
        var.name = "distCtrl"

        target = var.targets[0]
        target.data_path = '["Light distance"]'
        target.id = controller

        location_driver.driver.expression = "-distCtrl"

        # Lock transform

        light.lock_location[0] = True
        light.lock_location[1] = True
        light.lock_location[2] = True
        light.lock_rotation[0] = True
        light.lock_rotation[1] = True
        light.lock_rotation[2] = True

        controller.lock_scale[0] = True
        controller.lock_scale[1] = True
        controller.lock_scale[2] = True

        # Set parents

        light.parent = controller
        controller.parent = parent

    def update_dependencies():
        for drv in self.drivers:
            drv.driver.expression = drv.driver.expression[:]

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
    cam_controller.location = controller_location
    coll.objects.link(cam_controller)

    # Create camera

    cam_data = bpy.data.cameras.new(name="Camera")
    cam = bpy.data.objects.new("Camera", cam_data)
    cam.location = (0, -1, 0)
    cam.rotation_euler = (radians(90), 0, 0)
    coll.objects.link(cam)

    # Set constraints

    cam_limitscale = cam.constraints.new("LIMIT_SCALE")
    cam_limitscale.use_min_x = True
    cam_limitscale.min_x = 1
    cam_limitscale.use_max_x = True
    cam_limitscale.max_x = 1
    cam_limitscale.use_min_y = True
    cam_limitscale.min_y = 1
    cam_limitscale.use_max_y = True
    cam_limitscale.max_y = 1
    cam_limitscale.use_min_z = True
    cam_limitscale.min_z = 1
    cam_limitscale.use_max_z = True
    cam_limitscale.max_z = 1

    # Lock camera transform

    cam.lock_location[0] = True
    cam.lock_location[1] = True
    cam.lock_location[2] = True
    cam.lock_rotation[0] = True
    cam.lock_rotation[1] = True
    cam.lock_rotation[2] = True

    # Set parent

    cam.parent = cam_controller
    cam.matrix_parent_inverse = cam_controller.matrix_world.inverted()

    # LIGHT CONTROLLERS

    self.drivers = set()

    # Key Light Controller
    add_light_controller("Key", (radians(-15), 0, radians(-45)), cam_controller)

    # Fill Light Controller
    add_light_controller("Fill", (radians(-15), 0, radians(45)), cam_controller)

    # Rim Light Controller
    add_light_controller("Rim", (radians(-30), 0, radians(-135)), cam_controller)

    # Update dependencies
    update_dependencies()

    # Select controller

    for obj in context.selected_objects:
        obj.select_set(False)

    context.view_layer.objects.active = cam_controller
    cam_controller.select_set(True)

    # Return referencies
    return cam_controller


class RADIALRENDERER_OT_create_preset(bpy.types.Operator):
    """Add a pre-built controller"""

    bl_label = "Create Preset"
    bl_idname = "radialrenderer.create_preset"

    def execute(self, context):

        scene = context.scene
        mytool = scene.my_tool

        # Calculate controller spawn location
        spawn_location = Vector()

        selected_objects = context.selected_objects
        if len(selected_objects):
            for obj in selected_objects:
                spawn_location += obj.location
            spawn_location /= len(selected_objects)
        else:
            spawn_location = context.scene.cursor.location.copy()

        # Set object reference
        if len(selected_objects) == 1:
            mytool.obj = context.selected_objects[0]

        mytool.controller = create_controller(self, context, spawn_location)

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_create_preset,)

def register():
  for cls in classes:
    bpy.utils.register_class(cls)

def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)