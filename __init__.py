import bpy, os
from bpy.types import Scene

from . import preference, file_menu, operators, properties, panel

bl_info = {
  "name": "HollowEngine - Special Rig | Plugin | v.1.0",
  "description": "Special plugin for HollowEngine Rig",
  "author": "_BENDY659_",
  "version": (1, 0, 0),
  "blender": (4, 3, 0),
  "location": "File > New",
  "warning": "",
  "wiki_url": "",
  "category": "Rigging"
}

# (Un)Registrations #
def register():
  bpy.utils.register_class(preference.HE_Rig_Preference)

  for name, prop in properties.list:
    setattr(Scene, name, prop)

  for op in operators.list:
    bpy.utils.register_class(op)

  bpy.types.TOPBAR_MT_file_new.append(file_menu.open_copy_project)

  bpy.utils.register_class(panel.RigPanel)

def unregister():
  bpy.utils.unregister_class(preference.HE_Rig_Preference)

  for name, _ in properties.list:
    delattr(Scene, name)

  for op in operators.list:
    bpy.utils.unregister_class(op)

  bpy.types.TOPBAR_MT_file_new.remove(file_menu.open_copy_project)

  bpy.utils.unregister_class(panel.RigPanel)

# Init #
if __name__ == "__main__":
  register()