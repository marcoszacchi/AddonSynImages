import bpy
import numpy as np
from . import operators

class VIEW3D_PT_synthetic_image_generator(bpy.types.Panel):
    bl_label = 'Synthetic Image Generator'
    bl_idname = 'VIEW3D_PT_synthetic_image_generator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Image Generator'
 
    def draw(self, context):
        layout = self.layout
        object = context.object
        scene = context.scene.custom_properties


        box1 = layout.box()
        icon = 'TRIA_DOWN' if scene.auto_exec else 'TRIA_RIGHT'
        row = box1.row()
        row.prop(scene, "auto_exec", text="Multiple Synthesis", icon=icon, emboss=False)

        if scene.auto_exec:
            row = box1.row()
            col1 = row.column()
            col1.scale_x = 1.4
            col1.label(text="STL Directory", icon='FOLDER_REDIRECT')
            col2 = row.column()
            col2.prop(scene, "import_dir")
            row = box1.row()
        

        box2 = layout.box()
        icon = 'TRIA_DOWN' if scene.manual_exec else 'TRIA_RIGHT'
        row = box2.row()
        row.prop(scene, "manual_exec", text="Single Synthesis", icon=icon, emboss=False)

        if scene.manual_exec:
            row = box2.row()
            col1 = row.column()
            col1.scale_x = 1.4
            col1.label(text="STL File", icon='FOLDER_REDIRECT')
            col2 = row.column()
            col2.prop(scene, "file_dir")
            
            row = box2.row()
            row.operator(operators.Opr_import_object.bl_idname)

            icon = 'TRIA_DOWN' if scene.manual_exec_set else 'TRIA_RIGHT'
            row = box2.row()
            row.prop(scene, "manual_exec_set", text="Custom STL Settings", icon=icon, emboss=False)
            
            if scene.manual_exec_set:
                row = box2.row()
                col1 = row.column(align=True)
                col1.scale_x = 0.9
                op_xp = col1.operator(operators.Opr_custom_rotate.bl_idname, text="X+", icon='FILE_REFRESH')
                op_xp.axis = 'X'
                op_xp.angle = np.deg2rad(5)
                op_yp = col1.operator(operators.Opr_custom_rotate.bl_idname, text="Y+", icon='FILE_REFRESH')
                op_yp.axis = 'Y'
                op_yp.angle = np.deg2rad(5)
                op_zp = col1.operator(operators.Opr_custom_rotate.bl_idname, text="Z+", icon='FILE_REFRESH')
                op_zp.axis = 'Z'
                op_zp.angle = np.deg2rad(5)
                
                col2 = row.column(align=True)
                col2.scale_x = 0.9
                op_xn = col2.operator(operators.Opr_custom_rotate.bl_idname, text="X-", icon='FILE_REFRESH')
                op_xn.axis = 'X'
                op_xn.angle = np.deg2rad(-5)
                op_yn = col2.operator(operators.Opr_custom_rotate.bl_idname, text="Y-", icon='FILE_REFRESH')
                op_yn.axis = 'Y'
                op_yn.angle = np.deg2rad(-5)
                op_zn = col2.operator(operators.Opr_custom_rotate.bl_idname, text="Z-", icon='FILE_REFRESH')
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
                row.operator(operators.Opr_default_rotation.bl_idname, icon='DRIVER_ROTATIONAL_DIFFERENCE')
                row = box2.row()


        box3 = layout.box()
        icon = 'TRIA_DOWN' if scene.transformations else 'TRIA_RIGHT'
        row = box3.row()
        row.prop(scene, "transformations", text="Transformations", icon=icon, emboss=False)

        if scene.transformations:
            
            row = box3.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Steps", icon='SPHERE')
            col2 = row.column()
            col2.prop(scene, "rotation_steps", text="")
            
            row = box3.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Scaling", icon='VIEWZOOM')
            col2 = row.column()
            col2.prop(scene, "scaling_percentage", text="%")

            row = box3.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Translation", icon='ORIENTATION_VIEW')
            col2 = row.column()
            col2.prop(scene, "translation_percentage", text="%")
        

        box4 = layout.box()
        icon = 'TRIA_DOWN' if scene.export else 'TRIA_RIGHT'
        row = box4.row()
        row.prop(scene, "export", text="Export", icon=icon, emboss=False)

        if scene.export:
            row = box4.row()
            row.label(text="Image Path", icon='FILEBROWSER')
            row = box4.row()
            row.prop(scene, "image_dir")

            row = box4.row()
            row.operator(operators.Opr_auto_execute.bl_idname, icon='RESTRICT_RENDER_OFF')
            
            row = box4.row()
            row.operator(operators.Opr_start_render.bl_idname, icon='RESTRICT_RENDER_OFF')
            
            row = box4.row()
        

def register_panels():
    bpy.utils.register_class(VIEW3D_PT_synthetic_image_generator)

def unregister_panels():
    bpy.utils.unregister_class(VIEW3D_PT_synthetic_image_generator)