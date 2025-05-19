import bpy, os

from . import preference, file_menu, operators

dir = os.path.dirname(__file__)
version = os.path.join(dir, "VERSION")

with open(version, "r", encoding="utf-8") as f:
  verion_str = f.read().strip()

version_tuple = tuple(map(str, verion_str.split(".")))

bl_info = {
  "name": "HollowEngine - Special Rig | Plugin | v.1.0",
  "description": "Special plugin for HollowEngine Rig",
  "author": "_BENDY659_",
  "version": version_tuple,
  "blender": (4, 3, 0),
  "location": "View3D",
  "warning": "",
  "wiki_url": "",
  "category": "Rigging"
}

# (Un)Registrations #
def register():
  bpy.utils.register_class(preference.HE_Rig_Preference)

  for op in operators.list:
    bpy.utils.register_class(op)

  bpy.types.TOPBAR_MT_file_new.append(file_menu.open_copy_project)

def unregister():
  bpy.utils.unregister_class(preference.HE_Rig_Preference)

  for op in operators.list:
    bpy.utils.unregister_class(op)

  bpy.types.TOPBAR_MT_file_new.remove(file_menu.open_copy_project)

# Init #
if __name__ == "__main__":
  register()