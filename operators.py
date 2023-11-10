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
        object = self.set_object.selector(context)
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')
        file = context.scene.custom_properties.file_dir
        
        if object:
            bpy.data.objects.remove(object, do_unlink=True)
        
        self.manual_import(file)
        object = self.set_object.selector(context)
        
        if object:
            self.set_object.set_origin(object)
            self.set_object.auto_rotate(object)
            self.set_camera.fit_camera_distance(context, object, camera, light)
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
        object = self.set_object.selector(context)
        self.set_object.auto_rotate(object)

        return {"FINISHED"}


class Opr_custom_rotate(bpy.types.Operator):
    bl_idname = "opr.custom_rotate"
    bl_label = "Custom rotate object"

    set_object = utils.SetObject()

    axis: bpy.props.EnumProperty(
        name="Axis",
        description="Axis to Rotate",
        items=[('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")],
        default='X'
    )

    angle: bpy.props.FloatProperty(name="Angle", default=0)

    def execute(self, context):
        object = self.set_object.selector(context)
        self.custom_rotate(object, self.axis, self.angle)

        return {"FINISHED"}

    def custom_rotate(self, object, axis, angle):
        if axis == 'X':
            object.rotation_euler.x += angle
        elif axis == 'Y':
            object.rotation_euler.y += angle
        elif axis == 'Z':
            object.rotation_euler.z += angle


class Opr_start_render(bpy.types.Operator):
    bl_idname = "opr.start_render"
    bl_label = "Synthesize from File"

    set_object = utils.SetObject()
    set_camera = utils.SetCamera()
        
    def execute(self, context):
        object = self.set_object.selector(context)
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')
        
        self.set_render(context)
        self.start_render(context, object, camera, light)
        return {"FINISHED"}

    def set_render(self, context):
        context.scene.render.image_settings.file_format = 'PNG'

    def start_render(self, context, object, camera, light):
        scene = context.scene.custom_properties

        obj_location = object.location
        cam_location = camera.location
        rotation_steps = scene.rotation_steps
        pic_qnt = round(360 / rotation_steps)

        image_path = scene.image_dir
        object_path = f'{image_path}/{object.name}'

        for pic in range(pic_qnt):
            context.scene.render.filepath = f'{object_path}/{pic + 1}'
            bpy.ops.render.render(write_still=1)
            camera.location = self.set_camera.rotate_pos(obj_location, cam_location, rotation_steps)
            light.location = camera.location
        

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
    bpy.utils.register_class(Opr_custom_rotate)
    bpy.utils.register_class(Opr_start_render)
    bpy.utils.register_class(Opr_auto_execute)

def unregister_operators():
    bpy.utils.unregister_class(Opr_import_object)
    bpy.utils.unregister_class(Opr_default_rotation)
    bpy.utils.unregister_class(Opr_custom_rotate)
    bpy.utils.unregister_class(Opr_start_render)
    bpy.utils.unregister_class(Opr_auto_execute)