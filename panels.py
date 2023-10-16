import bpy
import numpy as np
from . import utils
from . import properties

class VIEW3D_PT_synthetic_image_generator(bpy.types.Panel):
    bl_label = 'Synthetic Image Generator'
    bl_idname = 'VIEW3D_PT_synthetic_image_generator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Image Generator'
 
    def draw(self, context):
        layout = self.layout
        self.manager = utils.ObjectManager()
        object = self.manager.select_object
        scene = context.scene
       
        box1 = layout.box()

        icon = 'TRIA_DOWN' if scene.auto_exec else 'TRIA_RIGHT'
        row1 = box1.row()
        row1.prop(context.scene.my_custom_properties, "auto_exec", text="Generate from Directory", icon=icon, emboss=False)

        if context.scene.my_custom_properties.auto_exec:

            row = box1.row()
            row.label(text="Files Path", icon='FOLDER_REDIRECT')
            row = box1.row()
            row.prop(context.scene.my_custom_properties, "import_dir")

            row = box1.row()
        
        box2 = layout.box()

        icon = 'TRIA_DOWN' if context.scene.my_custom_properties.manual_exec else 'TRIA_RIGHT'
        row2 = box2.row()
        row2.prop(context.scene.my_custom_properties, "manual_exec", text="Generate from File", icon=icon, emboss=False)

        if context.scene.my_custom_properties.manual_exec:

            row = box2.row()
            row.label(text="File Path", icon='FOLDER_REDIRECT')
            row = box2.row()
            row.prop(context.scene.my_custom_properties, "file_dir")
            
            row = box2.row()
            row.operator("opr.import_object")

            row = box2.row()
            col1 = row.column(align=True)
            col1.scale_x = 0.9
            op_xp = col1.operator("opr.custom_rotate", text="X+", icon='FILE_REFRESH')
            op_xp.axis = 'X'
            op_xp.angle = np.deg2rad(5)
            op_yp = col1.operator("opr.custom_rotate", text="Y+", icon='FILE_REFRESH')
            op_yp.axis = 'Y'
            op_yp.angle = np.deg2rad(5)
            op_zp = col1.operator("opr.custom_rotate", text="Z+", icon='FILE_REFRESH')
            op_zp.axis = 'Z'
            op_zp.angle = np.deg2rad(5)
            
            col2 = row.column(align=True)
            col2.scale_x = 0.9
            op_xn = col2.operator("opr.custom_rotate", text="X-", icon='FILE_REFRESH')
            op_xn.axis = 'X'
            op_xn.angle = np.deg2rad(-5)
            op_yn = col2.operator("opr.custom_rotate", text="Y-", icon='FILE_REFRESH')
            op_yn.axis = 'Y'
            op_yn.angle = np.deg2rad(-5)
            op_zn = col2.operator("opr.custom_rotate", text="Z-", icon='FILE_REFRESH')
            op_zn.axis = 'Z'
            op_zn.angle = np.deg2rad(-5)

            col3 = row.column(align=True)
            row1 = col3.row()
            row1.prop(object, "rotation_euler", text="", index=0,)
            row2 = col3.row()
            row2.prop(object, "rotation_euler", text="", index=1)
            row3 = col3.row()
            row3.prop(object, "rotation_euler", text="", index=2)

            row = box2.row()
            row.operator("opr.default_rotation", icon='DRIVER_ROTATIONAL_DIFFERENCE')
            row = box2.row()
        
        box_out = layout.box()

        row = box_out.row()
        row.label(text="Save images to", icon='FOLDER_REDIRECT')
        row = box_out.row()
        row.prop(context.scene.my_custom_properties, "image_dir")

        row = box_out.row()
        col1 = row.column()
        col2 = row.column()
        col1.label(text="Steps", icon='SPHERE')
        col2.prop(context.scene.my_custom_properties, "rotation_steps", text="")

        row = box_out.row()
        if scene.auto_exec:
            row = box_out.row()
            row.operator("opr.auto_execute", icon='RESTRICT_RENDER_OFF')
            row = box_out.row()

        if scene.manual_exec:
            row = box_out.row()
            row.operator("opr.start_render", icon='RESTRICT_RENDER_OFF')
            row = box_out.row()

def register_panels():
    bpy.utils.register_class(VIEW3D_PT_synthetic_image_generator)

def unregister_panels():
    bpy.utils.unregister_class(VIEW3D_PT_synthetic_image_generator)