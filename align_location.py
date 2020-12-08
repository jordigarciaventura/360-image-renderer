import bpy

from . import properties as prop


def align_location(obj_from, obj_to):
    obj_from.location = obj_to.matrix_world.to_translation()


class RADIALRENDERER_OT_align_location(bpy.types.Operator):
    """Align objects location"""

    bl_label = "Align"
    bl_idname = "radialrenderer.align_location"

    def execute(self, context):

        scene = context.scene
        mytool = scene.my_tool

        # Check dependencies

        if not prop.is_in_view_layer(self, mytool.controller):
            self.report({"ERROR"}, prop.not_in_view_layer_error % "Controller")
            return {"FINISHED"}

        if not prop.is_in_view_layer(self, mytool.obj):
            self.report({"ERROR"}, prop.not_in_view_layer_error % "Object")
            return {"FINISHED"}

        # Align location

        if mytool.controller_to_obj:
            align_location(mytool.controller, mytool.obj)
        else:
            align_location(mytool.obj, mytool.controller)

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_align_location,)
