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

# Export path #
class Export_Path_Operator(Operator):
  bl_idname = "he_rig.export_path"
  bl_label = "Select export folder"
  bl_description = "Select a folder to export to"

  directory: bpy.props.StringProperty(subtype="DIR_PATH")

  def invoke(self, context, event):
    context.window_manager.fileselect_add(self)
    self.use_folder = True

    return {'RUNNING_MODAL'}
  
  def execute(self, context):
    context.scene.he_rig_export_path = self.directory

    return {'FINISHED'}

# Export button #
class Export_Button_Operator(Operator):
  bl_idname = "he_rig.export"
  bl_label = "Export model"

  def execute(self, context):
    scene = context.scene

    path = scene.he_rig_export_path
    format = scene.he_rig_export_format

    # Check selected path #
    if not path:
      temp_dir = HE_RIG_File_Menu_Operator.temp_dir
      path = temp_dir
      self.report({'WARNING'}, f"Export path not selected. Im use [{temp_dir}]!")
    # ------------------- #

    filepath = os.path.join(path, f"model.{format[1]}")

    # Check format selected #
    export_format = ""

    if format == "GLTF":
      export_format = "GLTF_SEPARATE"
    elif format == "GLB":
      export_format = "GLB"
    else:
      self.reort({'ERROR'}, f"Idk this export format [{format}]!")
    # --------------------- #
    
    # Export scene #
    bpy.ops.export_scene.gltf(
      filepath=filepath,
      export_format=export_format,
      export_normals=True,
      export_tangents=True,
      export_apply=True,
      export_materials='PLACEHOLDER',
      export_draco_mesh_compression_enable=False,
      export_morph=True,
      export_morph_normal=True,
      export_morph_tangent=True
    )
    # ------------ #

    self.report({'INFO'}, f"Im exported to [{filepath}]")
    return ['FINISHED']

# ----

list = [
  HE_RIG_File_Menu_Operator,
  Export_Path_Operator,
  Export_Button_Operator
]