from bpy.props import StringProperty, EnumProperty

# Properties #

# Export path/format - Operator #
export_path = (
  "he_rig_export_path",
  StringProperty(
    name="Export path",
    description="Folder to export the model",
    subtype="DIR_PATH",
    default= None
  )
)
export_format = (
  "he_rig_export_format",
  EnumProperty(
    name="Export format",
    description="Choose export format",
    items=[
      ("GLTF", "gltf", "Export as glTF"),
      ("GLB", "glb", "Export to GLB")
    ],
    default="GLTF"
  )
)

list = [
  export_path,
  export_format
]