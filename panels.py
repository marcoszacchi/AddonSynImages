import bpy
from . import operators

class VIEW3D_PT_synthetic_image_generator(bpy.types.Panel):
    bl_label = 'Synthetic Image Generator'
    bl_idname = 'VIEW3D_PT_synthetic_image_generator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SynImages'
 
    def draw(self, context):
        layout = self.layout
        scene = context.scene.custom_properties

        box1 = layout.box()
        icon = 'TRIA_DOWN' if scene.auto_exec else 'TRIA_RIGHT'
        row = box1.row()
        row.prop(scene, "auto_exec", text="Multiple Synthesizes", icon=icon, emboss=False)

        if scene.auto_exec:
            row = box1.row()
            col1 = row.column()
            col1.scale_x = 0.9
            col1.label(text="Source", icon='FOLDER_REDIRECT')
            col2 = row.column()
            col2.prop(scene, "import_dir")
            
            row = box1.row()
            row.operator(operators.Opr_select_directory.bl_idname)
        

        box2 = layout.box()
        icon = 'TRIA_DOWN' if scene.manual_exec else 'TRIA_RIGHT'
        row = box2.row()
        row.prop(scene, "manual_exec", text="Single Synthesizes", icon=icon, emboss=False)

        if scene.manual_exec:
            row = box2.row()
            col1 = row.column()
            col1.scale_x = 0.9
            col1.label(text="File", icon='FOLDER_REDIRECT')
            col2 = row.column()
            col2.prop(scene, "file_dir")
            
            row = box2.row()
            row.operator(operators.Opr_import_object.bl_idname)
        
        box3 = layout.box()
        icon = 'TRIA_DOWN' if scene.manual_exec_set else 'TRIA_RIGHT'
        row = box3.row()
        row.prop(scene, "manual_exec_set", text="Object Rotation", icon=icon, emboss=False)
        
        if scene.manual_exec_set:

            row = box3.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="X axis", icon='FILE_REFRESH')
            col2 = row.column()
            col2.prop(scene, "object_rotation_x", text="")

            row = box3.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Y axis", icon='FILE_REFRESH')
            col2 = row.column()
            col2.prop(scene, "object_rotation_y", text="")

            row = box3.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Z axis", icon='FILE_REFRESH')
            col2 = row.column()
            col2.prop(scene, "object_rotation_z", text="")

            row = box3.row()
            row.operator(operators.Opr_default_rotation.bl_idname, icon='DRIVER_ROTATIONAL_DIFFERENCE')
            row = box3.row()
        
        box4 = layout.box()
        icon = 'TRIA_DOWN' if scene.trajectory else 'TRIA_RIGHT'
        row = box4.row()
        row.prop(scene, "trajectory", text="Trajectory", icon=icon, emboss=False)

        if scene.trajectory:
            row = box4.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Camera Trajectory", icon='OUTLINER_DATA_CURVE')
            col2 = row.column()
            col2.prop(scene, "cam_trajectory")
            
            if scene.cam_trajectory == 'circular_trajectory':
                row = box4.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="H. Steps", icon='SPHERE')
                col2 = row.column()
                col2.prop(scene, "horizontal_rotation_steps", text="")

                row = box4.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="Phi", icon='ORIENTATION_GLOBAL')
                col2 = row.column()
                col2.prop(scene, "camera_height_angle", text="")

            elif scene.cam_trajectory == 'spherical_trajectory':
                row = box4.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="Horizontal Steps", icon='SPHERE')
                col2 = row.column()
                col2.prop(scene, "horizontal_rotation_steps", text="")

                row = box4.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="V. Steps", icon='SPHERE')
                col2 = row.column()
                col2.prop(scene, "vertical_rotation_steps", text="")


        box5 = layout.box()
        icon = 'TRIA_DOWN' if scene.transformations else 'TRIA_RIGHT'
        row = box5.row()
        row.prop(scene, "transformations", text="Transformations", icon=icon, emboss=False)

        if scene.transformations:
            row = box5.row()
            col1 = row.column()
            col1.scale_x = 1.1
            col1.label(text="Scaling", icon='VIEWZOOM')
            col2 = row.column()
            col2.prop(scene, "scaling_percentage", text="%")

            row = box5.row()
            col1 = row.column()
            col1.scale_x = 1.1
            col1.label(text="Hor. Translation", icon='ORIENTATION_VIEW')
            col2 = row.column()
            col2.prop(scene, "horizontal_translation", text="")

            row = box5.row()
            col1 = row.column()
            col1.scale_x = 1.1
            col1.label(text="Ver. Translation", icon='ORIENTATION_VIEW')
            col2 = row.column()
            col2.prop(scene, "vertical_translation", text="")

            row = box5.row()
            col1 = row.column()
            col1.scale_x = 1.1
            col1.label(text="Light Intensity", icon='LIGHT_DATA')
            col2 = row.column()
            col2.prop(scene, "light_intensity", text="%")


        box6 = layout.box()
        icon = 'TRIA_DOWN' if scene.background else 'TRIA_RIGHT'
        row = box6.row()
        row.prop(scene, "background", text="Background", icon=icon, emboss=False)

        if scene.background:
            row = box6.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Background Type", icon='OUTLINER_DATA_CURVE')
            col2 = row.column()
            col2.prop(scene, "background_type")

            if scene.background_type == 'solid_color':
                row = box6.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="Red", icon='SEQUENCE_COLOR_01')
                col2 = row.column()
                col2.prop(scene, "r_color", text="")
                
                row = box6.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="Green", icon='SEQUENCE_COLOR_04')
                col2 = row.column()
                col2.prop(scene, "g_color", text="")
                
                row = box6.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="Blue", icon='SEQUENCE_COLOR_05')
                col2 = row.column()
                col2.prop(scene, "b_color", text="")

                row = box6.row()
                row.operator(operators.Opr_select_background_color.bl_idname, text="Apply")

                row = box6.row()
                row.operator(operators.Opr_default_background_color.bl_idname, text="Default")

            if scene.background_type == 'image':
                row = box6.row()
                col1 = row.column()
                col1.scale_x = 0.9
                col1.label(text="Source", icon='IMAGE_RGB')
                col2 = row.column()
                col2.prop(scene, "background_dir")

                row = box6.row()
                row.operator(operators.Opr_select_background_image.bl_idname, text="Apply")

        box7 = layout.box()
        icon = 'TRIA_DOWN' if scene.export else 'TRIA_RIGHT'
        row = box7.row()
        row.prop(scene, "export", text="Export", icon=icon, emboss=False)

        if scene.export:
            row = box7.row()
            row.label(text="Image Path", icon='FILEBROWSER')
            row = box7.row()
            row.prop(scene, "image_dir")

            row = box7.row()
            row.operator(operators.Opr_auto_execute.bl_idname, icon='RESTRICT_RENDER_OFF')
            
            row = box7.row()
            row.operator(operators.Opr_start_render.bl_idname, icon='RESTRICT_RENDER_OFF')
            
            row = box7.row()
        

def register_panels():
    bpy.utils.register_class(VIEW3D_PT_synthetic_image_generator)

def unregister_panels():
    bpy.utils.unregister_class(VIEW3D_PT_synthetic_image_generator)