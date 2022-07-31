import bpy


renderable_types = ("MESH", "CURVE", "SURFACE", "HAIR")


def isolate_selection(self, context):
    mytool = context.scene.my_tool
    
    if mytool.only_selected:
      hide_selection(context)
    else:
      unhide_objects(context)
      
      
def hide_selection(context):
        
    # unselected_objects = all_objects - selected_objects
    all_objects = context.scene.objects
    selected_objects = context.selected_objects.copy()
    unselected_objects = [x for x in all_objects if x not in selected_objects]

    for obj in unselected_objects:
        if obj.type in renderable_types:
            obj["hidden_by_isolation"] = True
            obj.hide_render = obj.hide_viewport = True
  

def unhide_objects(context):
    for obj in context.scene.objects:
      if obj.get("hidden_by_isolation", False):
        obj.hide_render = obj.hide_viewport = False