def isolate_selection(context, isolate):
  renderable_types = ("MESH", "CURVE", "SURFACE", "HAIR")      

  if isolate: # Hide renderable unselected objects
    
    # unselected_objects = all_objects - selected_objects
    all_objects = context.scene.objects
    selected_objects = context.selected_objects.copy()
    unselected_objects = [x for x in all_objects if x not in selected_objects]

    for obj in unselected_objects:
        if obj.type in renderable_types:
            obj["hidden_by_isolation"] = True
            obj.hide_render = obj.hide_viewport = True
  
  else: # Unhide isolated objects
    
    for obj in context.scene.objects:
      if obj.get("hidden_by_isolation", False):
        obj.hide_render = obj.hide_viewport = False