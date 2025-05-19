from bpy.types import Menu, Context

def open_copy_project(self: Menu, context: Context):
  self.layout.separator()
  self.layout.operator("he_rig.open_copy_project", icon='COPYDOWN')