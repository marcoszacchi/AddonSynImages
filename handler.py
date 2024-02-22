import bpy
import numpy as np
from . import utils

def update_object_rotation(scene, context):
    scene = context.scene.custom_properties
    set_object = utils.SetObject()
    object = set_object.selector(context)
   
    if object:
        if scene.manual_exec_set:
            object.rotation_euler.x = np.deg2rad(scene.object_rotation_x)
            object.rotation_euler.y = np.deg2rad(scene.object_rotation_y)
            object.rotation_euler.z = np.deg2rad(scene.object_rotation_z)

def update_camera_position(scene, context):
    scene = context.scene.custom_properties
    camera = context.scene.camera

    r = np.sqrt((camera.location.x**2) + (camera.location.y**2) + (camera.location.z**2))
    phi = np.deg2rad(scene.camera_height_angle)
    theta = np.deg2rad(90 + scene.camera_position_angle)

    camera.location.x = r * np.sin(phi) * np.cos(theta)
    camera.location.y = r * np.sin(phi) * np.sin(theta)
    camera.location.z = r * np.cos(phi)

def update_light(scene, context):
    scene = context.scene.custom_properties
    set_light = utils.SetLight()
    camera = context.scene.camera
    light = bpy.data.objects.get('Light')
    light.location = camera.location
    intensity = scene.light_intensity
    set_light.set_light_intensity(light, intensity)

def update_camera_clip(scene, context):
    camera = context.scene.camera
    if camera is not None:
        camera.data.clip_start = 0.1
        camera.data.clip_end = camera.location.length * 1.5

    
def register_handler():
    bpy.app.handlers.depsgraph_update_post.append(update_object_rotation)
    bpy.app.handlers.depsgraph_update_post.append(update_camera_position)
    bpy.app.handlers.depsgraph_update_post.append(update_light)
    bpy.app.handlers.depsgraph_update_post.append(update_camera_clip)

def unregister_handler():
    for handler in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.remove(update_object_rotation)
        bpy.app.handlers.render_complete.remove(update_camera_position)
        bpy.app.handlers.render_complete.remove(update_light)
        bpy.app.handlers.render_complete.remove(update_camera_clip)