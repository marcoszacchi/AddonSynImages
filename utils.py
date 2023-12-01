import bpy
import mathutils
import numpy as np

class SetObject:
    def selector(self, context):
        fixed_object_names = ['Camera', 'Light']

        for object in bpy.data.objects:
            object.select_set(False)

        for object in bpy.data.objects:
            if object.name not in fixed_object_names:
                object.select_set(True)
                context.view_layer.objects.active = object
        return context.view_layer.objects.active
    
    def auto_rotate(self, object):
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
    
    def set_origin(self, object):
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        object.location = mathutils.Vector((0, 0, 0))
        object.rotation_euler = mathutils.Vector((0, 0, 0))

    def scaling(self, object, scaling_percentage):
        scaling_factor = 1.0 + (scaling_percentage / 100)
        scaling_tuple = (scaling_factor, scaling_factor, scaling_factor)
        object.scale = scaling_tuple

class SetCamera:
    def fit_distance(self, context, object, camera, light):
        distance = 2
        camera.location = mathutils.Vector((0,distance,0))
        light.location = camera.location
        
        bounding_box = object.bound_box
        min_coords = mathutils.Vector(bounding_box[0])
        max_coords = mathutils.Vector(bounding_box[6])

        diagonal = (max_coords - min_coords).length
        
        aspect_ratio = context.scene.render.resolution_x / context.scene.render.resolution_y
        camera_angle = camera.data.angle
        
        if aspect_ratio > 1:
            camera_angle /= aspect_ratio
        
        distance_camera = (diagonal / 2) / np.tan(camera_angle / 2)
        
        camera_direction = (camera.location - object.location).normalized()
        camera.location = object.location + camera_direction * distance_camera
        light.location = camera.location

class SetTracking:
    def set_camera_tracking(self, object, camera):
        constraint = camera.constraints.new(type='TRACK_TO')
        constraint.target = object

    def set_light_tracking(self, object, light):
        constraint = light.constraints.new(type='TRACK_TO')
        constraint.target = object

class SetLight:
    def set_light(self, light):
        light.data.type = 'SUN'
        light.data.energy = 2
        light.data.use_shadow = False