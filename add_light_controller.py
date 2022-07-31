import bpy

from math import (
    radians,
    degrees,
)

from mathutils import Vector

import properties as prop

# Creates a Light Controller
def add_light_controller(context, parent, rotation = (0, 0, 0), name = ""):

    # Create light controller
    controller_name = " ".join([name, "Light Controller"]).strip()
    light_controller = bpy.data.objects.new(controller_name, None)
    light_controller.empty_display_type = 'SPHERE'
    light_controller.rotation_euler = rotation

    # Add 'Child of' constraint
    light_child_of = light_controller.constraints.new('CHILD_OF')
    light_child_of.target = parent
    light_child_of.use_scale_x = False
    light_child_of.use_scale_y = False
    light_child_of.use_scale_z = False

    # Create light
    light_name = " ".join([name,"Light"]).strip()
    light_data = bpy.data.lights.new(light_name, type="AREA")
    light = bpy.data.objects.new(light_name, light_data)
    light.location = (0, -1, 0)
    light.rotation_euler = (radians(90), 0, 0)

    # Add 'Transform' constraint
    light_transform = light.constraints.new('TRANSFORM')
    light_transform.target = light_controller
    light_transform.target_space = 'LOCAL'
    light_transform.owner_space = 'LOCAL'
    light_transform.map_from = 'SCALE'
    light_transform.from_min_y_scale = 0
    light_transform.from_max_y_scale = 100000
    light_transform.map_to = 'LOCATION'
    light_transform.map_to_z_from = 'Y'
    light_transform.to_max_z = 100000
    light_transform.mix_mode = 'REPLACE'
    
    # Add 'Child of' constraint
    light_child_of = light.constraints.new('CHILD_OF')
    light_child_of.target = light_controller
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
  
    # Add objects to scene
    context.collection.objects.link(light_controller)
    context.collection.objects.link(light)
    
    return light_controller

class RADIALRENDERER_OT_add_light_controller(bpy.types.Operator):
    """Add a pre-built light controller"""

    bl_label = "Create Light Controller"
    bl_idname = "radialrenderer.add_light_controller"

    @classmethod
    def poll(self, context):
        scene = context.scene
        mytool = scene.my_tool
        return bool(mytool.controller)

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        if not prop.is_in_view_layer(self, mytool.controller):
            self.report({"ERROR"}, prop.not_in_view_layer_error % "Controller")
            return {"FINISHED"}

        add_light_controller(context, mytool.controller)

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_add_light_controller,)

def register():
  for cls in classes:
    bpy.utils.register_class(cls)

def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)