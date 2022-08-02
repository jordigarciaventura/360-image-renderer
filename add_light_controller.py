import bpy

import properties as prop

from math import radians
from mathutils import Vector


# Creates a Light Controller
def create_light_controller(parent):
    parent_rotation = Vector(
        (parent.rotation_euler.x, parent.rotation_euler.y, parent.rotation_euler.z))

    # Create light pivot
    light_pivot = bpy.data.objects.new("Light Pivot", None)
    light_pivot.empty_display_type = 'SPHERE'
    light_pivot.location = parent.location
    light_pivot.rotation_euler = parent_rotation
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
    light.rotation_euler = parent_rotation + Vector((radians(90), 0, 0))
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

        # Add light controller
        coll, _, light_pivot = create_light_controller(mytool.controller) # Create light controller
        mytool.controller.users_collection[0].children.link(coll) # Add inside camera controller 

        # Select controller
        for obj in context.selected_objects:
            obj.select_set(False)
        context.view_layer.objects.active = light_pivot
        light_pivot.select_set(True)

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_add_light_controller,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
