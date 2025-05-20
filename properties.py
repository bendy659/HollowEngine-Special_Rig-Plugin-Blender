from bpy.props import StringProperty, EnumProperty

# Properties #

# Export name/path/format - Operator #
export_name = (
  "he_rig_export_name",
  StringProperty(
    name="Export",
    subtype="FILE_NAME",
    default="rig"
  )
)
export_path = (
  "he_rig_export_path",
  StringProperty(
    subtype="DIR_PATH",
    default=""
  )
)
export_format = (
  "he_rig_export_format",
  EnumProperty(
    name="Export format",
    items=[
      ("GLTF", "gltf", "Export as glTF"),
      ("GLB", "glb", "Export to GLB")
    ],
    default="GLTF"
  )
)

list = [
  export_name,
  export_path,
  export_format
]