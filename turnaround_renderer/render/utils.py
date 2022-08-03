import bpy
import os

render_started_msg = "360 RENDERER: render started\n"
render_finished_msg = "360 RENDERER: render finished\n"
frames_renderer_msg = "360 RENDERER: %s/%s frames rendered\n"


def setup_transparent_background(context, enable):
    scene = context.scene
    render = scene.render

    if enable:
        # Save for restore
        scene['previous_file_format'] = render.image_settings.file_format
        scene['previous_color_mode'] = render.image_settings.color_mode
        scene['previous_film_transparent'] = render.film_transparent
        # Change
        render.image_settings.file_format = 'PNG'
        render.image_settings.color_mode = 'RGBA'
        render.film_transparent = True
    else:
        # Restore unedited properties
        if render.image_settings.file_format == 'PNG':
            render.image_settings.file_format = scene.get(
                'previous_file_format', render.image_settings.file_format)
        if render.image_settings.color_mode == 'RGBA':
            render.image_settings.color_mode = scene.get(
                'previous_color_mode', render.image_settings.color_mode)
        if render.film_transparent:
            render.film_transparent = scene.get(
                'previous_film_transparent', render.film_transparent)


def isolate_selection(context, isolate):
    renderable_types = ("MESH", "CURVE", "SURFACE", "HAIR")

    if isolate:  # Hide renderable unselected objects

        # unselected_objects = all_objects - selected_objects
        all_objects = context.scene.objects
        selected_objects = context.selected_objects.copy()
        unselected_objects = [
            x for x in all_objects if x not in selected_objects]

        for obj in unselected_objects:
            if obj.type in renderable_types:
                obj["hidden_by_isolation"] = True
                obj.hide_render = obj.hide_viewport = True

    else:  # Unhide isolated objects

        for obj in context.scene.objects:
            if obj.get("hidden_by_isolation", False):
                obj.hide_render = obj.hide_viewport = False


def export_marker_names(context):
    scene = context.scene
    wm = context.window_manager

    # Save project
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

    # Set variables
    frame_start = scene.frame_start
    frame_end = scene.frame_end

    frames_rendered = 0
    frames_total = 1 + frame_end - frame_start

    dir_path = scene.render.filepath

    markername = ""

    # Render started
    print(render_started_msg)
    print(frames_renderer_msg % ("0", frames_total))
    wm.progress_begin(frame_start, frame_end)

    # Iterate through animation keyframes
    for step in range(frame_start, frame_end + 1):

        # Set current frame
        scene.frame_set(step)

        # Get frame's marker name
        for marker in scene.timeline_markers:
            if marker.frame == step:
                markername = marker.name

        # Set output filepath
        scene.render.filepath = os.path.join(dir_path, markername)

        # Render
        bpy.ops.render.render(write_still=True)
        frames_rendered += 1
        print(frames_renderer_msg % (frames_rendered, frames_total))
        wm.progress_update(step)

    # Reset filepath
    scene.render.filepath = dir_path

    # Render finished
    print(render_finished_msg)
    wm.progress_end()
