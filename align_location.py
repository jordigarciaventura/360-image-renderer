import bpy

import properties as prop


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

        if not prop.is_in_view_layer(self, mytool.from_obj):
            self.report({"ERROR"}, prop.not_in_view_layer_error % "From")
            return {"FINISHED"}

        if not prop.is_in_view_layer(self, mytool.to_obj):
            self.report({"ERROR"}, prop.not_in_view_layer_error % "To")
            return {"FINISHED"}

        # Align location

        align_location(mytool.from_obj, mytool.to_obj)

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_align_location,)

def register():
  for cls in classes:
    bpy.utils.register_class(cls)

def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)