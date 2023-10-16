import bpy
import numpy as np
import os
from . import utils

class Opr_auto_execute(bpy.types.Operator):
    bl_idname = "opr.auto_execute"
    bl_label = "Generate Images"

    def execute(self, context):
        object = bpy.context.active_object
        if object:
            bpy.data.objects.remove(object, do_unlink=True)
        self.auto_import(context)
        return {"FINISHED"}
    
    def auto_import(self, context):
        object_path = context.scene.import_dir
        
        for file in os.listdir(object_path):
            if file.endswith(".stl") or file.endswith(".STL"):
                filepath = os.path.join(object_path, file)
                bpy.ops.import_mesh.stl(filepath=filepath)

                self.select_object(context)
                self.select_object(context)
                self.auto_set_object(context)
                self.camera_follow_object(context)
                self.light_follow_object(context)
                bpy.ops.opr.start_render()
                object = bpy.context.active_object
                bpy.data.objects.remove(object, do_unlink=True)


 #-------------------------------------------------------------------------#   

# Operador para aplicar as configuracoes iniciais no objeto
class Opr_import_object(bpy.types.Operator):
    bl_idname = "opr.import_object"
    bl_label = "Import Object"

    def execute(self, context):
        object = bpy.context.active_object
        if object:
            bpy.data.objects.remove(object, do_unlink=True)
        self.manual_import(context)
        self.select_object(context)
        self.auto_set_object(context)
        self.camera_follow_object(context)
        self.light_follow_object(context)

        return {"FINISHED"}
    
    def manual_import(self, context):
        file = context.scene.file_dir
        
        if file.endswith(".stl") or file.endswith(".STL"):
            bpy.ops.import_mesh.stl(filepath=file)


#-------------------------------------------------------------------------#

# Operador para aplicar as configuracoes iniciais no objeto
class Opr_default_rotation(bpy.types.Operator):
    bl_idname = "opr.default_rotation"
    bl_label = "Default Rotation"

    def execute(self, context):
        self.select_object(context)
        self.auto_rotate(context)

        return {"FINISHED"}


#-------------------------------------------------------------------------#

# Operador para o usuario definir uma rotacao customizada
class Opr_custom_rotate(bpy.types.Operator):
    bl_idname = "opr.custom_rotate"
    bl_label = "Custom rotate object"

    axis_items = [('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")]
    
    axis: bpy.props.EnumProperty(
        name="Axis",
        description="Axis to Rotate",
        items=axis_items,
        default='X'
    )

    angle: bpy.props.FloatProperty(name="Angle", default=0)

    def execute(self, context):
        self.select_object(context)
        self.custom_rotate(context, self.axis, self.angle)

        return {"FINISHED"}

    def custom_rotate(self, context, axis, angle):
        object = context.object
        if axis == 'X':
            object.rotation_euler.x += angle
        elif axis == 'Y':
            object.rotation_euler.y += angle
        elif axis == 'Z':
            object.rotation_euler.z += angle


#-------------------------------------------------------------------------#

# Operador para iniciar a renderização
class Opr_start_render(bpy.types.Operator):
    bl_idname = "opr.start_render"
    bl_label = "Generate Images"
        
    def execute(self, context):
        self.select_object(context)
        self.set_render(context)
        self.start_render(context)
        return {"FINISHED"}

    def set_render(self, context):
        context.scene.render.image_settings.file_format = 'PNG'

    def rotateTo(self, planet, moon, angle):
        angle = np.deg2rad(angle)
        posX = moon[0] - planet[0]
        posY = moon[1] - planet[1]
        newX = posX * np.cos(angle) - posY * np.sin(angle)
        newY = posX * np.sin(angle) + posY * np.cos(angle)
        newPos = (newX + planet[0], newY + planet[1], moon[2])
        return newPos

    def start_render(self, context):
        object = context.object
        camera = context.scene.camera
        obj_location = object.location
        cam_location = camera.location
        light = bpy.data.objects.get('Light')
        rotation_steps = context.scene.rotation_steps
        pic_qnt = round(360 / rotation_steps)

        image_path = context.scene.image_dir

        for pic in range(pic_qnt):
            context.scene.render.filepath = f'{image_path}/{object.name}/{pic + 1}'
            bpy.ops.render.render(write_still=1)
            camera.location = self.rotateTo(obj_location, cam_location, rotation_steps)
            light.location = camera.location