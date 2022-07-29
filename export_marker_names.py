import bpy
import os

import properties as prop


def export_marker_names(self, context, path):

    scene = context.scene

    # Check dependencies

    if not bpy.data.filepath:
        self.report({"ERROR"}, prop.project_not_saved_error)
        return {"FINISHED"}

    if not path:
        self.report({"ERROR"}, prop.path_empty_error)
        return {"FINISHED"}

    if not scene.camera:
        self.report({"ERROR"}, prop.no_active_camera_error)
        return {"FINISHED"}

    markers_names = set()

    # Get markers names inside render range
    for frame in range(scene.frame_start, scene.frame_end + 1):
        for marker in scene.timeline_markers:
            if marker.frame == frame and marker.name:
                markers_names.add(marker.name)

    # Check if all frames have a marker
    if len(markers_names) < scene.frame_end + 1 - scene.frame_start:
        self.report({"ERROR"}, prop.markers_names_named_error)
        return {"FINISHED"}

    # Check if all markers have a valid name
    for name in markers_names:
        if not prop.validate_file_name(name):
            self.report({"ERROR"}, prop.marker_name_error)
            return {"FINISHED"}

    # Save project
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

    # Set variables
    frame_start = scene.frame_start
    frame_end = scene.frame_end

    frames_rendered = 0
    frames_total = frame_end + 1 - frame_start

    markername = ""

    # Render started
    print(prop.render_started_msg)
    print(prop.frames_renderer_msg % ("0", frames_total))

    # Iterate through animation keyframes
    for step in range(frame_start, frame_end + 1):

        # Set current frame
        scene.frame_set(step)

        # Get frame's marker name
        for marker in scene.timeline_markers:
            if marker.frame == step:
                markername = marker.name

        # Set output filepath
        scene.render.filepath = os.path.join(path, markername)

        # Render
        bpy.ops.render.render(write_still=True)
        frames_rendered += 1

        print(prop.frames_renderer_msg % (frames_rendered, frames_total))

    # Render finished
    print(prop.render_finished_msg)


class RADIALRENDERER_OT_export(bpy.types.Operator):
    """Render animation using markers as filename"""

    bl_label = "Export Keyframes"
    bl_idname = "radialrenderer.export"

    def execute(self, context):

        scene = context.scene
        mytool = scene.my_tool

        export_marker_names(self, context, mytool.path)

        return {"FINISHED"}


classes = (RADIALRENDERER_OT_export,)

def register():
  for cls in classes:
    bpy.utils.register_class(cls)

def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)