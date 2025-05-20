from bpy.types import Panel

class RigPanel(Panel):
  bl_label = "HollowEngine | Special Rig"
  bl_idname = "HE_RIG_PANEL"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"
  bl_category = "Special Rig"

  def draw(self, context):
    layout = self.layout
    scene = context.scene

    layout.separator()

    ### Export ###

    export_path = scene.he_rig_export_path
    export_format = scene.he_rig_export_format

    export = layout.box()

    export.label(text="Export rig...")
    e_col = export.column()

    e_col_row0 = e_col.row()
    e_col_row0.prop(scene, "he_rig_export_name") # File name
    e_col_row0.prop(scene, "he_rig_export_path") # Path

    e_col_row1 = e_col.row()
    e_col_row1.operator("he_rig.export", text=f"Export to [{export_format}]") # Export button
    e_col_row1.prop(scene, "he_rig_export_format") # Export format

    ### ------ ###

    layout.separator()

    ### Rig Properties ###

    props = layout.box()
    props.label(text="Rig Properties", icon="SETTINGS")

    rig = context.active_object

    if rig and rig.type == 'ARMATURE' and rig["he_special_rig"] == True:
      ## Eyes ##

      head = rig.pose.bones["Head"]

      eyes = props.box()
      eyes.label(text="Eyes", icon="HIDE_OFF")

      eyes_row = eyes.row()
      
      # Left Eye #
      left_eye = eyes_row.column()

      left_eye.label(text="Left Eye")
      left_eye.prop(head, "[\"Left_Eye_Close\"]", slider=True, text="Closing")
      left_eye.separator()
      left_eye.prop(head, "[\"Left_Eye_Top_Close\"]", slider=True, text="Closing Top")
      left_eye.prop(head, "[\"Left_Eye_Bottom_Close\"]", slider=True, text="Closing Bottom")
      # -------- #

      eyes_row.separator()

      # Right Eye #
      right_eye = eyes_row.column()
      right_eye1 = eyes_row.column()

      right_eye.label(text="Right Eye")
      right_eye.prop(head, "[\"Right_Eye_Close\"]", slider=True, text="Closing")
      right_eye.separator()
      right_eye.prop(head, "[\"Right_Eye_Top_Close\"]", slider=True, text="Closing Top")
      right_eye.prop(head, "[\"Right_Eye_Bottom_Close\"]", slider=True, text="Closing Bottom")
      # -------- #

      ## ---- ##
    else:
      props.label(text="<Select Special Rig>")
      
    ### -------------- ###