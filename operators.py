import bpy
import os
import numpy as np
from . import utils

class Opr_select_directory(bpy.types.Operator):
    bl_idname = "opr.select_directory"
    bl_label = "Select Directory"

    def __init__(self):
        self.set_object = utils.SetObject()
        self.set_camera = utils.SetCamera()
        self.set_tracking = utils.SetTracking()
        self.set_light = utils.SetLight()
        self.set_scene = utils.SetScene()

    def execute(self, context):
        object = self.set_object.selector(context)
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')
        object_path = context.scene.custom_properties.import_dir
        self.set_scene.delete_trace()
        
        if object:
            bpy.data.objects.remove(object, do_unlink=True)
        
        self.select_file(context, camera, light, object_path)

        return {"FINISHED"}
    
    def select_file(self, context, camera, light, object_path):
        for file in os.listdir(object_path):
            if file.endswith(".stl") or file.endswith(".STL"):
                filepath = os.path.join(object_path, file)
                bpy.ops.import_mesh.stl(filepath=filepath)
                
                object = self.set_object.selector(context)
                self.set_object.set_origin(object)
                self.set_light.set_light(light)
                self.set_camera.fit_distance(context, object, camera, light)
                bpy.ops.opr.default_rotation()
                self.set_tracking.set_camera_tracking(object, camera)
                self.set_tracking.set_light_tracking(object, light)
                self.set_camera.camera_view()
                
                return


class Opr_import_object(bpy.types.Operator):
    bl_idname = "opr.import_object"
    bl_label = "Import STL"

    def __init__(self):
        self.set_object = utils.SetObject()
        self.set_camera = utils.SetCamera()
        self.set_tracking = utils.SetTracking()
        self.set_light = utils.SetLight()
        self.set_scene = utils.SetScene()
        self.set_render = utils.SetRender()

    def execute(self, context):
        scene = context.scene.custom_properties
        object = self.set_object.selector(context)
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')
        file = scene.file_dir
        self.set_scene.delete_trace()
        self.set_render.set_viewport()

        if object:
            bpy.data.objects.remove(object, do_unlink=True)
        
        scene.camera_height = 0        
        self.manual_import(file)
        object = self.set_object.selector(context)
        
        if object:
            self.set_scene.delete_trace()
            scene.object_rotation_x = np.rad2deg(object.rotation_euler.x)
            scene.object_rotation_y = np.rad2deg(object.rotation_euler.y)
            scene.object_rotation_z = np.rad2deg(object.rotation_euler.z)
            self.set_object.set_origin(object)
            bpy.ops.opr.default_rotation()
            self.set_camera.fit_distance(context, object, camera, light)
            self.set_light.set_light(light)
            self.set_tracking.set_camera_tracking(object, camera)
            self.set_tracking.set_light_tracking(object, light)
            self.set_camera.camera_view()

        return {"FINISHED"}
    
    def manual_import(self, file):
        if file.endswith(".stl") or file.endswith(".STL"):
            bpy.ops.import_mesh.stl(filepath=file)


class Opr_default_rotation(bpy.types.Operator):
    bl_idname = "opr.default_rotation"
    bl_label = "Default Rotation"

    def __init__(self):
        self.set_object = utils.SetObject()

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
    bl_label = "Single Synthesize"

    def __init__(self):
        self.set_object = utils.SetObject()
        self.set_camera = utils.SetCamera()
        self.set_scene = utils.SetScene()
        self.set_light = utils.SetLight()
        
    def execute(self, context):
        scene = context.scene.custom_properties
        object = self.set_object.selector(context)
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')
        trajectory = scene.cam_trajectory
        h_angle = scene.horizontal_rotation_steps
        v_angle = scene.vertical_rotation_steps
        context.scene.render.image_settings.file_format = 'PNG'
        self.set_scene.delete_trace()
        self.start_render(context, scene, object, camera, light, trajectory, h_angle, v_angle)
        return {"FINISHED"}

    def start_render(self, context, scene, object, camera, light, trajectory, h_angle, v_angle):
        if trajectory == 'circular_trajectory':
            h_qnt = round(360/h_angle)
            
            for h_pic in range(h_qnt):
                    scene.camera_position_angle = h_pic * h_angle
                    light.location = camera.location
                    self.set_light.set_light(light)
                    context.scene.render.filepath = f'{scene.image_dir}/{object.name}_{"circular"}/{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}'    
                    bpy.ops.render.render(write_still=1)
                    self.set_scene.set_trace(camera.location)
        
        if trajectory == 'spherical_trajectory':
            h_qnt = round(360/h_angle)
            v_qnt = round(180/v_angle)

            for v_pic in range(v_qnt + 1):
                scene.camera_height_angle = v_pic * v_angle
                
                for h_pic in range(h_qnt):
                    scene.camera_position_angle = h_pic * h_angle
                    light.location = camera.location
                    context.scene.render.filepath = f'{scene.image_dir}/{object.name}_{"spherical"}/{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}'    
                    bpy.ops.render.render(write_still=1)
                    self.set_scene.set_trace(camera.location)

        scene.camera_position_angle = 0
        scene.camera_height_angle = 90
        bpy.ops.opr.default_rotation()
        self.set_camera.space_view()


class Opr_auto_execute(bpy.types.Operator):
    bl_idname = "opr.auto_execute"
    bl_label = "Multiple Synthesizes"

    def __init__(self):
        self.set_object = utils.SetObject()
        self.set_camera = utils.SetCamera()
        self.set_tracking = utils.SetTracking()
        self.set_light = utils.SetLight()
        self.set_scene = utils.SetScene()

    def execute(self, context):
        scene = context.scene.custom_properties
        object = self.set_object.selector(context)
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')
        object_path = scene.custom_properties.import_dir

        self.auto_import(context, object, camera, light, object_path)

        return {"FINISHED"}
    
    def auto_import(self, context, object, camera, light, object_path):
        for file in os.listdir(object_path):
            if file.endswith(".stl") or file.endswith(".STL"):
                if object:
                    bpy.data.objects.remove(object, do_unlink=True)
                    self.set_scene.delete_trace()

                filepath = os.path.join(object_path, file)
                bpy.ops.import_mesh.stl(filepath=filepath)
                object = self.set_object.selector(context)
                self.set_object.set_origin(object)
                self.set_light.set_light(light)
                self.set_camera.fit_distance(context, object, camera, light)
                bpy.ops.opr.default_rotation()
                self.set_tracking.set_camera_tracking(object, camera)
                self.set_tracking.set_light_tracking(object, light)
                bpy.ops.opr.start_render()


class Opr_select_background_color(bpy.types.Operator):
    bl_idname = "opr.set_background_color"
    bl_label = "Set Background Color"

    def __init__(self):
        self.set_world = utils.SetWorld()

    def execute(self, context):
        scene = context.scene.custom_properties
        r = scene.r_color
        g = scene.g_color
        b = scene.b_color

        self.set_world.set_background_color(r, g, b)

        return {'FINISHED'}


class Opr_default_background_color(bpy.types.Operator):
    bl_idname = "opr.default_background_color"
    bl_label = "Default Background Color"

    def __init__(self):
        self.set_world = utils.SetWorld()

    def execute(self, context):
        scene = context.scene.custom_properties
        scene.r_color = 13
        scene.g_color = 13
        scene.b_color = 13
        r = scene.r_color
        g = scene.g_color
        b = scene.b_color

        self.set_world.set_background_color(r, g, b)

        return {'FINISHED'}
 

class Opr_select_background_image(bpy.types.Operator):
    bl_idname = "opr.set_background_image"
    bl_label = "Set Background Image"

    def __init__(self):
        self.set_world = utils.SetWorld()

    def execute(self, context):
        scene = context.scene.custom_properties
        image_path = scene.background_dir

        self.set_world.set_background_image(image_path)
        
        return {'FINISHED'}


def register_operators():
    bpy.utils.register_class(Opr_import_object)
    bpy.utils.register_class(Opr_default_rotation)
    bpy.utils.register_class(Opr_start_render)
    bpy.utils.register_class(Opr_select_directory)
    bpy.utils.register_class(Opr_auto_execute)
    bpy.utils.register_class(Opr_select_background_color)
    bpy.utils.register_class(Opr_default_background_color)
    bpy.utils.register_class(Opr_select_background_image)

def unregister_operators():
    bpy.utils.unregister_class(Opr_import_object)
    bpy.utils.unregister_class(Opr_default_rotation)
    bpy.utils.unregister_class(Opr_start_render)
    bpy.utils.unregister_class(Opr_select_directory)
    bpy.utils.unregister_class(Opr_auto_execute)
    bpy.utils.unregister_class(Opr_select_background_color)
    bpy.utils.unregister_class(Opr_default_background_color)
    bpy.utils.unregister_class(Opr_select_background_image)