import os

import bpy

import properties as prop


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
    print(prop.render_started_msg)
    print(prop.frames_renderer_msg % ("0", frames_total))
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
        print(prop.frames_renderer_msg % (frames_rendered, frames_total))
        wm.progress_update(step)

    # Reset filepath
    scene.render.filepath = dir_path

    # Render finished
    print(prop.render_finished_msg)
    wm.progress_end()


class RADIALRENDERER_OT_export(bpy.types.Operator):
    """Render animation using markers as filename"""

    bl_label = "Export Keyframes"
    bl_idname = "radialrenderer.export"

    def execute(self, context):
        scene = context.scene

        # Check dependencies
        if not bpy.data.filepath:
            self.report({"ERROR"}, prop.project_not_saved_error)
            return {"FINISHED"}

        if not scene.render.filepath:
            self.report({"ERROR"}, prop.path_empty_error)
            return {"FINISHED"}

        if not scene.camera:
            self.report({"ERROR"}, prop.no_active_camera_error)
            return {"FINISHED"}

        markers_names = []

        # Get markers names inside render range
        for frame in range(scene.frame_start, scene.frame_end + 1):
            for marker in scene.timeline_markers:
                if marker.frame == frame and marker.name:
                    markers_names.append(marker.name)
                    print(marker.name)

        # Check if all frames have a marker
        if len(markers_names) < 1 + scene.frame_start - scene.frame_end:
            self.report({"ERROR"}, prop.markers_names_named_error)
            return {"FINISHED"}

        # Check if all markers have a valid name
        for name in markers_names:
            if not prop.validate_file_name(name):
                self.report({"ERROR"}, prop.marker_name_error)
                return {"FINISHED"}

        export_marker_names(context)

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_export,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
