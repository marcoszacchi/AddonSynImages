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
            row.prop(scene, "manual_exec_set", text="Rotate Object", icon=icon, emboss=False)
            
            if scene.manual_exec_set:

                row = box2.row()
                col1 = row.column()
                col1.scale_x = 1.2
                col1.label(text="X axis", icon='FILE_REFRESH')
                col2 = row.column()
                col2.prop(scene, "object_rotation_x", text="")

                row = box2.row()
                col1 = row.column()
                col1.scale_x = 1.2
                col1.label(text="Y axis", icon='FILE_REFRESH')
                col2 = row.column()
                col2.prop(scene, "object_rotation_y", text="")

                row = box2.row()
                col1 = row.column()
                col1.scale_x = 1.2
                col1.label(text="Z axis", icon='FILE_REFRESH')
                col2 = row.column()
                col2.prop(scene, "object_rotation_z", text="")

                row = box2.row()
                row.operator(operators.Opr_default_rotation.bl_idname, icon='DRIVER_ROTATIONAL_DIFFERENCE')
                row = box2.row()
        
        box3 = layout.box()
        icon = 'TRIA_DOWN' if scene.trajectory else 'TRIA_RIGHT'
        row = box3.row()
        row.prop(scene, "trajectory", text="Trajectory", icon=icon, emboss=False)

        if scene.trajectory:
            row = box3.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Camera Trajectory", icon='OUTLINER_DATA_CURVE')
            col2 = row.column()
            col2.prop(scene, "cam_trajectory")
            
            if scene.cam_trajectory == 'circular_trajectory':
                row = box3.row()
                col1 = row.column()
                col1.scale_x = 1.2
                col1.label(text="Horizontal Steps", icon='SPHERE')
                col2 = row.column()
                col2.prop(scene, "horizontal_rotation_steps", text="")

                row = box3.row()
                col1 = row.column()
                col1.scale_x = 1.2
                col1.label(text="Phi", icon='ORIENTATION_GLOBAL')
                col2 = row.column()
                col2.prop(scene, "camera_height_angle", text="")

            elif scene.cam_trajectory == 'spherical_trajectory':
                row = box3.row()
                col1 = row.column()
                col1.scale_x = 1.2
                col1.label(text="Horizontal Steps", icon='SPHERE')
                col2 = row.column()
                col2.prop(scene, "horizontal_rotation_steps", text="")

                row = box3.row()
                col1 = row.column()
                col1.scale_x = 1.2
                col1.label(text="Vertical Steps", icon='SPHERE')
                col2 = row.column()
                col2.prop(scene, "vertical_rotation_steps", text="")


        box4 = layout.box()
        icon = 'TRIA_DOWN' if scene.transformations else 'TRIA_RIGHT'
        row = box4.row()
        row.prop(scene, "transformations", text="Transformations", icon=icon, emboss=False)

        if scene.transformations:
            row = box4.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Scaling", icon='VIEWZOOM')
            col2 = row.column()
            col2.prop(scene, "scaling_percentage", text="%")

            row = box4.row()
            col1 = row.column()
            col1.scale_x = 1.2
            col1.label(text="Translation", icon='ORIENTATION_VIEW')
            col2 = row.column()
            col2.prop(scene, "translation_percentage", text="%")
        

        box5 = layout.box()
        icon = 'TRIA_DOWN' if scene.export else 'TRIA_RIGHT'
        row = box5.row()
        row.prop(scene, "export", text="Export", icon=icon, emboss=False)

        if scene.export:
            row = box5.row()
            row.label(text="Image Path", icon='FILEBROWSER')
            row = box5.row()
            row.prop(scene, "image_dir")

            row = box5.row()
            row.operator(operators.Opr_auto_execute.bl_idname, icon='RESTRICT_RENDER_OFF')
            
            row = box5.row()
            row.operator(operators.Opr_start_render.bl_idname, icon='RESTRICT_RENDER_OFF')
            
            row = box5.row()
        

def register_panels():
    bpy.utils.register_class(VIEW3D_PT_synthetic_image_generator)

def unregister_panels():
    bpy.utils.unregister_class(VIEW3D_PT_synthetic_image_generator)