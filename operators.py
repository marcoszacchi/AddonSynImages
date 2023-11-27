import bpy
import os
import numpy as np
import random
from . import utils

class Opr_import_object(bpy.types.Operator):
    bl_idname = "opr.import_object"
    bl_label = "Import STL"

    set_object = utils.SetObject()
    set_camera = utils.SetCamera()
    set_tracking = utils.SetTracking()
    set_light = utils.SetLight()

    def execute(self, context):
        scene = context.scene.custom_properties
        object = self.set_object.selector(context)
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')
        file = scene.file_dir

        if object:
            bpy.data.objects.remove(object, do_unlink=True)
        
        scene.camera_height = 0        
        self.manual_import(file)
        object = self.set_object.selector(context)
        
        if object:
            scene.object_rotation_x = np.rad2deg(object.rotation_euler.x)
            scene.object_rotation_y = np.rad2deg(object.rotation_euler.y)
            scene.object_rotation_z = np.rad2deg(object.rotation_euler.z)
            self.set_object.set_origin(object)
            bpy.ops.opr.default_rotation()
            self.set_camera.fit_distance(context, object, camera, light)
            self.set_light.set_light(light)
            self.set_tracking.set_camera_tracking(object, camera)
            self.set_tracking.set_light_tracking(object, light)

        return {"FINISHED"}
    
    def manual_import(self, file):
        if file.endswith(".stl") or file.endswith(".STL"):
            bpy.ops.import_mesh.stl(filepath=file)


class Opr_default_rotation(bpy.types.Operator):
    bl_idname = "opr.default_rotation"
    bl_label = "Default Rotation"

    set_object = utils.SetObject()

    def execute(self, context):
        scene = context.scene.custom_properties
        object = self.set_object.selector(context)
        self.set_object.auto_rotate(object)
        scene.camera_position_angle = 0
        scene.object_rotation_x = np.rad2deg(object.rotation_euler.x)
        scene.object_rotation_y = np.rad2deg(object.rotation_euler.y)
        scene.object_rotation_z = np.rad2deg(object.rotation_euler.z)

        return {"FINISHED"}

class Opr_start_render(bpy.types.Operator):
    bl_idname = "opr.start_render"
    bl_label = "Synthesize from File"

    set_object = utils.SetObject()
    set_camera = utils.SetCamera()
        
    def execute(self, context):
        
        object = self.set_object.selector(context)
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')
        context.scene.render.image_settings.file_format = 'PNG'
        self.start_render(context, object, camera, light)
        
        return {"FINISHED"}

    def start_render(self, context, object, camera, light):
        scene = context.scene.custom_properties
        trajectory = scene.cam_trajectory
        h_angle = scene.horizontal_rotation_steps
        v_angle = scene.vertical_rotation_steps
        
        if trajectory == 'circular_trajectory':
            h_qnt = round(360/h_angle)
            
            for h_pic in range(h_qnt):
                    scene.camera_position_angle = h_pic * h_angle
                    light.location = camera.location
                    context.scene.render.filepath = f'{scene.image_dir}/{object.name}/{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}'    
                    bpy.ops.render.render(write_still=1)
            scene.camera_position_angle = 0
        
        if trajectory == 'spherical_trajectory':
            h_qnt = round(360/h_angle)
            v_qnt = round(180/v_angle)

            for v_pic in range(v_qnt + 1):
                scene.camera_height_angle = v_pic * v_angle
                
                for h_pic in range(h_qnt):
                    scene.camera_position_angle = h_pic * h_angle
                    light.location = camera.location
                    context.scene.render.filepath = f'{scene.image_dir}/{object.name}/{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}'    
                    bpy.ops.render.render(write_still=1)

            scene.camera_position_angle = 0
            scene.camera_height_angle = 90

class Opr_auto_execute(bpy.types.Operator):
    bl_idname = "opr.auto_execute"
    bl_label = "Synthesize from Directory"

    set_object = utils.SetObject()
    set_camera = utils.SetCamera()
    set_tracking = utils.SetTracking()
    set_light = utils.SetLight()

    def execute(self, context):
        object = self.set_object.selector(context)
        
        if object:
            bpy.data.objects.remove(object, do_unlink=True)
        self.auto_import(context)
        return {"FINISHED"}
    
    def auto_import(self, context):
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')
        
        object_path = context.scene.custom_properties.import_dir
        
        for file in os.listdir(object_path):
            if file.endswith(".stl") or file.endswith(".STL"):
                filepath = os.path.join(object_path, file)
                bpy.ops.import_mesh.stl(filepath=filepath)
                
                object = self.set_object.selector(context)
                self.set_object.set_origin(object)
                self.set_light.set_light(light)
                self.set_camera.fit_camera_distance(context, object, camera, light)
                self.set_object.auto_rotate(object)
                self.set_tracking.set_camera_tracking(object, camera)
                self.set_tracking.set_light_tracking(object, light)
                bpy.ops.opr.start_render()
                bpy.data.objects.remove(object, do_unlink=True)
    


def register_operators():
    bpy.utils.register_class(Opr_import_object)
    bpy.utils.register_class(Opr_default_rotation)
    bpy.utils.register_class(Opr_start_render)
    bpy.utils.register_class(Opr_auto_execute)

def unregister_operators():
    bpy.utils.unregister_class(Opr_import_object)
    bpy.utils.unregister_class(Opr_default_rotation)
    bpy.utils.unregister_class(Opr_start_render)
    bpy.utils.unregister_class(Opr_auto_execute)