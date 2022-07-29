import bpy

class RADIALRENDERER_OT_swap_align(bpy.types.Operator):
    """Swap align items"""

    bl_label = "Swap"
    bl_idname = "radialrenderer.swap_align"

    def execute(self, context):

        scene = context.scene
        mytool = scene.my_tool

        mytool.from_obj, mytool.to_obj = mytool.to_obj, mytool.from_obj 

        return {"FINISHED"}
      

classes = (RADIALRENDERER_OT_swap_align,)

def register():
  for cls in classes:
    bpy.utils.register_class(cls)

def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)