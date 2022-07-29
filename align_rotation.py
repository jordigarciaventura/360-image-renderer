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

        if not prop.is_in_view_layer(self, mytool.controller):
            self.report({"ERROR"}, prop.not_in_view_layer_error % "Controller")
            return {"FINISHED"}

        if not prop.is_in_view_layer(self, mytool.obj):
            self.report({"ERROR"}, prop.not_in_view_layer_error % "Object")
            return {"FINISHED"}

        # Align rotation

        if mytool.controller_to_obj:
            align_rotation(mytool.controller, mytool.obj)
        else:
            align_rotation(mytool.obj, mytool.controller)

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_align_rotation,)

def register():
  for cls in classes:
    bpy.utils.register_class(cls)

def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)