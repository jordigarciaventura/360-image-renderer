def isolate_selection_func(self, context, value):
    isolate = bool(getattr(self, value))
    coll = context.scene.my_tool.hidden_objects
    isolate_selection(context, isolate, coll)


def isolate_selection(context, isolate, coll):

    renderable_types = ("MESH", "CURVE", "SURFACE", "HAIR")

    # Hide
    if isolate:

        # unselected_objects = all_objects - selected_objects
        all_objects = context.scene.objects
        selected_objects = context.selected_objects.copy()
        unselected_objects = [x for x in all_objects if x not in selected_objects]

        for obj in unselected_objects:
            if obj.type in renderable_types:
                item = coll.add()
                item.object = obj

        for obj in coll:
            obj.object.hide_render = obj.object.hide_viewport = True

    # Unhide
    else:
        for obj in coll:
            obj.object.hide_render = obj.object.hide_viewport = False

        coll.clear()