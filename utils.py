import bpy
import mathutils
import numpy as np

class ObjectManager:
    def select_object(self, context):
        fixed_object_names = ['Camera', 'Light']

        for object in bpy.data.objects:
            object.select_set(False)

        for object in bpy.data.objects:
            if object.name not in fixed_object_names:
                object.select_set(True)
                context.view_layer.objects.active = object
        return context.view_layer.objects.active
    
    def set_camera_tracking(self, context):
        object = self.select_object()
        camera = context.scene.camera
        constraint = camera.constraints.new(type='TRACK_TO')
        constraint.target = object

    def set_light_tracking(self, context):
        object = self.select_object()
        light = bpy.data.objects.get('Light')
        constraint = light.constraints.new(type='TRACK_TO')
        constraint.target = object

    def reset_object_origin(self, context):
        object = self.select_object()
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        object.location = mathutils.Vector((0, 0, 0))
        object.rotation_euler = mathutils.Vector((0, 0, 0))
    
    def adjust_light(self):
        light = bpy.data.objects.get('Light')
        light.data.type = 'SUN'
        light.data.energy = 2
        light.data.use_shadow = False

    def adjust_camera_distance(self, context):
        object = self.select_object()
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')

        camera.location = mathutils.Vector((1,1,1))
        light.location = camera.location + mathutils.Vector((1,1,1))
        
        bounding_box = object.bound_box
        min_coords = mathutils.Vector(bounding_box[0])
        max_coords = mathutils.Vector(bounding_box[6])
        
        scaled_min_coords = min_coords * object.scale
        scaled_max_coords = max_coords * object.scale

        diagonal = (scaled_max_coords - scaled_min_coords).length
        
        aspect_ratio = context.scene.render.resolution_x / context.scene.render.resolution_y
        camera_angle = camera.data.angle
        
        if aspect_ratio > 1:
            camera_angle /= aspect_ratio
        
        distance_camera = (diagonal / 2) / np.tan(camera_angle / 2)
        
        camera_direction = (camera.location - object.location).normalized()
        camera.location = object.location + camera_direction * distance_camera
        light.location = camera.location

        clip_start = 0.1
        clip_end = camera.location[0] * 4
        camera.data.clip_start = clip_start
        camera.data.clip_end = clip_end
    
    def auto_orient_object(self, context):
        object = self.select_object()
        rotation_angle = np.deg2rad(90)
        default_angle = mathutils.Vector((0, 0, 0))
        
        object.rotation_euler = default_angle

        dimensions = {
            "x": object.dimensions.x,
            "y": object.dimensions.y,
            "z": object.dimensions.z
        }
        
        sorted_dims = sorted(dimensions.items(), key=lambda x: x[1], reverse=True)
        max_dim = sorted_dims[0][0]
        second_max_dim = sorted_dims[1][0]

        if max_dim == "x":
            if second_max_dim == "y":
                pass
            elif second_max_dim == "z":
                object.rotation_euler.x = rotation_angle

        elif max_dim == "y":
            if second_max_dim == "x":
                object.rotation_euler.z = rotation_angle
            elif second_max_dim == "z":
                object.rotation_euler.y = -rotation_angle
                object.rotation_euler.z = rotation_angle

        elif max_dim == "z":
            if second_max_dim == "x":
                object.rotation_euler.x = rotation_angle
                object.rotation_euler.z = rotation_angle
            elif second_max_dim == "y":
                object.rotation_euler.x= rotation_angle
                object.rotation_euler.z = rotation_angle


def register_utils():
    bpy.utils.register_class(ObjectManager)

def unregister_utils():
    bpy.utils.unregister_class(ObjectManager)
    