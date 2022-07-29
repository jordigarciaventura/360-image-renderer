import bpy

import properties as prop


def align_rotation(obj_from, obj_to):
    obj_from.rotation_euler = obj_to.rotation_euler


class RADIALRENDERER_OT_align_rotation(bpy.types.Operator):
    """Align objects rotation"""

    bl_label = "Orientate"
    bl_idname = "radialrenderer.align_rotation"

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

        # Align rotation

        align_rotation(mytool.from_obj, mytool.to_obj)

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_align_rotation,)

def register():
  for cls in classes:
    bpy.utils.register_class(cls)

def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)