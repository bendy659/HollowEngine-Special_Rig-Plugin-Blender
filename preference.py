from bpy.types import AddonPreferences

from . import rig_data

class HE_Rig_Preference(AddonPreferences):
  bl_idname = __package__
  
  def draw(self, context):
    layout = self.layout

    layout.label(text="License")
    layout.separator()

    for line in rig_data.license.splitlines():
      layout.label(text=line)