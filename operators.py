import bpy, os
from bpy.types import Operator

import tempfile, shutil, datetime

from . import rig_data

# Operators #

# Add button in file menu #
class HE_RIG_File_Menu_Operator(Operator):
  bl_idname = "he_rig.open_copy_project"
  bl_label = "[HE Rig] Open copy project"

  temp_dir = ""

  def execute(self, context):
    dir = os.path.dirname(__file__)

    # Source files #
    blend = os.path.join(dir, "assets", rig_data.project)
    skin = os.path.join(dir, "assets", "skin.png")
    # ------------ #

    source_files = [
      blend,
      skin
    ]

    try:
      for file in source_files:
        if not os.path.isfile(file):
          self.report({'ERROR'}, f"Ops. Im not found original [{file}] file. Maybe this plugin - is broken, or other...")

      # Generate ID #
      now = datetime.datetime.now()

      year = int(now.year)
      mouth = int(now.month)
      day = int(now.day)
      hour = int(now.hour)
      minute = int(now.minute)
      second = int(now.second)

      id = year + mouth + day + hour + minute + second
      # ----------- #

      # Generate temp location #
      temp = tempfile.gettempdir()

      temp_dir = self.temp_dir
      temp_dir = os.path.join(temp, f"prm-copy-{id}")

      os.makedirs(temp_dir, exist_ok=True)

      blend_copy = os.path.join(temp_dir, "project.blend")
      skin_copy = os.path.join(temp_dir, "skin_copy.png")
      # ---------------------- #

      # Copy to temp #
      shutil.copy2(blend, blend_copy)
      shutil.copy2(skin, skin_copy)
      # ------------ #

      # Open copy project #
      if os.path.isfile(blend_copy):
        bpy.ops.wm.open_mainfile(filepath=blend_copy)
        self.report({'WARNING'}, f"File [{blend_copy}] opened. Dont forget save project in other path!")
      else:
        self.report({'ERROR'}, f"Ops... Im not found file in [{blend_copy}] :(. Maybe, error in create copy to TEMP in system, or other error...")
        return {'CANCELLED'}
      # ----------------- #

      # Apply copy skin #
      for img in bpy.data.images:
        for item in rig_data.textures:
          if img.name == item:
            img.filepath = skin_copy
            img.reload()
            self.report({'DEBUG'}, f"Texture [{img.name}] update path.")
      # --------------- #

      return {'FINISHED'}
    except Exception as e:
      self.report({'ERROR'}, f"Error open copy project!\n> {e}")

      return {'CANCELLED'}

# Export button #
class Export_Button_Operator(Operator):
  bl_idname = "he_rig.export"
  bl_label = "Export model"

  def execute(self, context):
    scene = context.scene

    name = scene.he_rig_export_name
    path = scene.he_rig_export_path
    format = scene.he_rig_export_format

    # Check selected path #
    if not path:
      path = bpy.path.abspath("//")
      self.report({'WARNING'}, f"Export path not selected. Using project directory: [{path}]")
    # ------------------- #

    # Map format string to extension and exporter constant #
    extension = ""
    export_format = ""
    if format == "GLTF":
      extension = "gltf"
      export_format = "GLTF_SEPARATE"
    elif format == "GLB":
      extension = "glb"
      export_format = "GLB"
    else:
      self.report({'ERROR'}, f"Unknown export format: {format}")
      return {'CANCELLED'}
    # ----------------------------------------------------- #

    filepath = os.path.join(path, f"{name}.{extension}")
    try:
      # Export scene #
      bpy.ops.export_scene.gltf(
        filepath=filepath,
        use_renderable=True,
        export_format=export_format,
        export_animations=True,
        export_normals=True,
        export_tangents=True,
        export_apply=True,
        export_materials='EXPORT',
        export_draco_mesh_compression_enable=False,
        export_morph=True,
        export_morph_normal=True,
        export_morph_tangent=True
      )
      self.report({'INFO'}, f"Model exported to: {filepath}")
      return {'FINISHED'}
    except Exception as e:
      self.report({'ERROR'}, f"Export failed: {e}")
      return {'CANCELLED'}

# ----

list = [
  HE_RIG_File_Menu_Operator,
  Export_Button_Operator
]