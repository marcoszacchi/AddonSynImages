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

        multipleBox = layout.box()
        icon = 'TRIA_DOWN' if scene.auto_exec else 'TRIA_RIGHT'
        row = multipleBox.row()
        row.prop(scene, "auto_exec", text="Multiple Synthesizes", icon=icon, emboss=False)

        if scene.auto_exec:
            row = multipleBox.row()
            col1 = row.column()
            col1.scale_x = 0.9
            col1.label(text="Source", icon='FOLDER_REDIRECT')
            col2 = row.column()
            col2.prop(scene, "import_dir")
            
            row = multipleBox.row()
            row.operator(operators.Opr_select_directory.bl_idname)
        

        singleBox = layout.box()
        icon = 'TRIA_DOWN' if scene.manual_exec else 'TRIA_RIGHT'
        row = singleBox.row()
        row.prop(scene, "manual_exec", text="Single Synthesizes", icon=icon, emboss=False)

        if scene.manual_exec:
            row = singleBox.row()
            col1 = row.column()
            col1.scale_x = 0.9
            col1.label(text="File", icon='FOLDER_REDIRECT')
            col2 = row.column()
            col2.prop(scene, "file_dir")
            
            row = singleBox.row()
            row.operator(operators.Opr_import_object.bl_idname)
        

        rotationBox = layout.box()
        icon = 'TRIA_DOWN' if scene.manual_exec_set else 'TRIA_RIGHT'
        row = rotationBox.row()
        row.prop(scene, "manual_exec_set", text="Object Rotation", icon=icon, emboss=False)
        
        if scene.manual_exec_set:

            row = rotationBox.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="X axis", icon='FILE_REFRESH')
            col2 = row.column()
            col2.prop(scene, "object_rotation_x", text="")

            row = rotationBox.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Y axis", icon='FILE_REFRESH')
            col2 = row.column()
            col2.prop(scene, "object_rotation_y", text="")

            row = rotationBox.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Z axis", icon='FILE_REFRESH')
            col2 = row.column()
            col2.prop(scene, "object_rotation_z", text="")

            row = rotationBox.row()
            row.operator(operators.Opr_default_rotation.bl_idname, icon='DRIVER_ROTATIONAL_DIFFERENCE')
            row = rotationBox.row()
        

        trajectoryBox = layout.box()
        icon = 'TRIA_DOWN' if scene.trajectory else 'TRIA_RIGHT'
        row = trajectoryBox.row()
        row.prop(scene, "trajectory", text="Trajectory", icon=icon, emboss=False)

        if scene.trajectory:
            row = trajectoryBox.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Camera Trajectory", icon='OUTLINER_DATA_CURVE')
            col2 = row.column()
            col2.prop(scene, "cam_trajectory")
            
            if scene.cam_trajectory == 'circular_trajectory':
                row = trajectoryBox.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="H. Steps", icon='SPHERE')
                col2 = row.column()
                col2.prop(scene, "horizontal_rotation_steps", text="")

                row = trajectoryBox.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="Phi", icon='ORIENTATION_GLOBAL')
                col2 = row.column()
                col2.prop(scene, "camera_height_angle", text="")

            elif scene.cam_trajectory == 'spherical_trajectory':
                row = trajectoryBox.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="H. Steps", icon='SPHERE')
                col2 = row.column()
                col2.prop(scene, "horizontal_rotation_steps", text="")

                row = trajectoryBox.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="V. Steps", icon='SPHERE')
                col2 = row.column()
                col2.prop(scene, "vertical_rotation_steps", text="")

        
        textureBox = layout.box()
        icon = 'TRIA_DOWN' if scene.texture else 'TRIA_RIGHT'
        row = textureBox.row()
        row.prop(scene, "texture", text="Texture", icon=icon, emboss=False)

        if scene.texture:
            row = textureBox.row()
            col1 = row.column()
            col1.scale_x = 0.9
            col1.label(text="Texture", icon='FOLDER_REDIRECT')
            col2 = row.column()
            col2.prop(scene, "texture_dir")
            
            row = textureBox.row()
            row.operator(operators.Opr_import_texture.bl_idname)

            row = textureBox.row()
            row = textureBox.row()
            col1 = row.column()
            col1.label(text="Depth", icon='NODE_TEXTURE')
            
            row = textureBox.row()
            col1 = row.column()
            col1.label(text="Scale")
            col2 = row.column()
            col2.prop(scene, "texture_scale", text="")

            row = textureBox.row()
            row = textureBox.row()
            col1 = row.column()
            col1.label(text="Location", icon='EMPTY_ARROWS')
            
            row = textureBox.row()
            col1 = row.column()
            col1 = col1.label(text="X axis")
            col2 = row.column()
            col2.prop(scene, "texture_location_x", text="")
            
            row = textureBox.row()
            col1 = row.column()
            col1 = col1.label(text="Y axis")
            col2 = row.column()
            col2.prop(scene, "texture_location_y", text="")

            row = textureBox.row()
            col1 = row.column()
            col1 = col1.label(text="Z axis")
            col2 = row.column()
            col2.prop(scene, "texture_location_z", text="")

            row = textureBox.row()
            row = textureBox.row()
            col1 = row.column()
            col1.label(text="Rotation", icon='FILE_REFRESH')

            row = textureBox.row()
            col1 = row.column()
            col1 = col1.label(text="X axis")
            col2 = row.column()
            col2.prop(scene, "texture_rotation_x", text="")
            
            row = textureBox.row()
            col1 = row.column()
            col1 = col1.label(text="Y axis")
            col2 = row.column()
            col2.prop(scene, "texture_rotation_y", text="")

            row = textureBox.row()
            col1 = row.column()
            col1 = col1.label(text="Z axis")
            col2 = row.column()
            col2.prop(scene, "texture_rotation_z", text="")

            row = textureBox.row()
            row = textureBox.row()
            col1 = row.column()
            col1.label(text="Scale", icon='VIEWZOOM')

            row = textureBox.row()
            col1 = row.column()
            col1 = col1.label(text="X axis")
            col2 = row.column()
            col2.prop(scene, "texture_scale_x", text="")
            
            row = textureBox.row()
            col1 = row.column()
            col1 = col1.label(text="Y axis")
            col2 = row.column()
            col2.prop(scene, "texture_scale_y", text="")

            row = textureBox.row()
            col1 = row.column()
            col1 = col1.label(text="Z axis")
            col2 = row.column()
            col2.prop(scene, "texture_scale_z", text="")
            
        
        transformationBox = layout.box()
        icon = 'TRIA_DOWN' if scene.transformations else 'TRIA_RIGHT'
        row = transformationBox.row()
        row.prop(scene, "transformations", text="Transformations", icon=icon, emboss=False)

        if scene.transformations:
            row = transformationBox.row()
            col1 = row.column()
            col1.scale_x = 1.1
            col1.label(text="Scaling", icon='VIEWZOOM')
            col2 = row.column()
            col2.prop(scene, "scaling_percentage", text="%")

            row = transformationBox.row()
            col1 = row.column()
            col1.scale_x = 1.1
            col1.label(text="Hor. Translation", icon='ORIENTATION_VIEW')
            col2 = row.column()
            col2.prop(scene, "horizontal_translation", text="")

            row = transformationBox.row()
            col1 = row.column()
            col1.scale_x = 1.1
            col1.label(text="Ver. Translation", icon='ORIENTATION_VIEW')
            col2 = row.column()
            col2.prop(scene, "vertical_translation", text="")

            row = transformationBox.row()
            col1 = row.column()
            col1.scale_x = 1.1
            col1.label(text="Light Intensity", icon='LIGHT_DATA')
            col2 = row.column()
            col2.prop(scene, "light_intensity", text="%")


        filterBox = layout.box()
        icon = 'TRIA_DOWN' if scene.filters else 'TRIA_RIGHT'
        row = filterBox.row()
        row.prop(scene, "filters", text="Filters", icon=icon, emboss=False)

        if scene.filters:
            row = filterBox.row()
            col1 = row.column()
            col1.scale_x = 0.9
            col1.label(text="Blur", icon='FOLDER_REDIRECT')
            col2 = row.column()
            col2.prop(scene, "smoothing", text="px")

            row = filterBox.row()
            row.operator(operators.Opr_smoothing_filter.bl_idname, icon='DRIVER_ROTATIONAL_DIFFERENCE')
            row = filterBox.row()


        backgroundBox = layout.box()
        icon = 'TRIA_DOWN' if scene.background else 'TRIA_RIGHT'
        row = backgroundBox.row()
        row.prop(scene, "background", text="Background", icon=icon, emboss=False)

        if scene.background:
            row = backgroundBox.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Background Type", icon='OUTLINER_DATA_CURVE')
            col2 = row.column()
            col2.prop(scene, "background_type")

            if scene.background_type == 'solid_color':
                row = backgroundBox.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="Red", icon='SEQUENCE_COLOR_01')
                col2 = row.column()
                col2.prop(scene, "r_color", text="")
                
                row = backgroundBox.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="Green", icon='SEQUENCE_COLOR_04')
                col2 = row.column()
                col2.prop(scene, "g_color", text="")
                
                row = backgroundBox.row()
                col1 = row.column()
                col1.scale_x = 1.1
                col1.label(text="Blue", icon='SEQUENCE_COLOR_05')
                col2 = row.column()
                col2.prop(scene, "b_color", text="")

                row = backgroundBox.row()
                row.operator(operators.Opr_set_background_color.bl_idname, text="Apply")

                row = backgroundBox.row()
                row.operator(operators.Opr_default_background_color.bl_idname, text="Default")

            if scene.background_type == 'image':
                row = backgroundBox.row()
                col1 = row.column()
                col1.scale_x = 0.9
                col1.label(text="Source", icon='IMAGE_RGB')
                col2 = row.column()
                col2.prop(scene, "background_dir")

                row = backgroundBox.row()
                row.operator(operators.Opr_select_background_image.bl_idname, text="Apply")


        exportBox = layout.box()
        icon = 'TRIA_DOWN' if scene.export else 'TRIA_RIGHT'
        row = exportBox.row()
        row.prop(scene, "export", text="Export", icon=icon, emboss=False)

        if scene.export:
            row = exportBox.row()
            row.label(text="Image Path", icon='FILEBROWSER')
            
            row = exportBox.row()
            row.prop(scene, "image_dir")
            

            box9 = layout.box()
            icon = 'TRIA_DOWN' if scene.multiple else 'TRIA_RIGHT'
            row = box9.row()
            row.prop(scene, "multiple", text="Multiple Synthesize", icon=icon, emboss=False)

            if scene.multiple:
                row = box9.row()
                row.operator(operators.Opr_auto_execute.bl_idname, icon='RESTRICT_RENDER_OFF')
            
            multipleBox0 = layout.box()
            icon = 'TRIA_DOWN' if scene.single else 'TRIA_RIGHT'
            row = multipleBox0.row()
            row.prop(scene, "single", text="Single Synthesize", icon=icon, emboss=False)
            
            if scene.single:
                row = multipleBox0.row()
                row.operator(operators.Opr_start_render.bl_idname, icon='RESTRICT_RENDER_OFF')
        
            row = exportBox.row()

def register_panels():
    bpy.utils.register_class(VIEW3D_PT_synthetic_image_generator)

def unregister_panels():
    bpy.utils.unregister_class(VIEW3D_PT_synthetic_image_generator)