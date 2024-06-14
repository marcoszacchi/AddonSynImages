import bpy
import os
import numpy as np
from . import utils

class Opr_change_viewport(bpy.types.Operator):
    bl_idname = "opr.change_viewport"
    bl_label = "Change Viewport"

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'
        return {'FINISHED'}


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
        scene = context.scene.custom_properties
        object = self.set_object.selector(context)
        camera = context.scene.camera
        light = bpy.data.objects.get('Light')
        object_path = scene.import_dir
        self.set_scene.delete_trace()
        
        if object:
            bpy.data.objects.remove(object, do_unlink=True)
        
        self.select_file(context, scene, camera, light, object_path)

        return {"FINISHED"}
    
    def select_file(self, context, scene, camera, light, object_path):
        for file in os.listdir(object_path):
            if file.endswith(".stl") or file.endswith(".STL"):
                filepath = os.path.join(object_path, file)
                bpy.ops.import_mesh.stl(filepath=filepath)
                object = self.set_object.selector(context)
                scene.object_name = object.name
                self.set_object.set_origin(object)
                self.set_light.set_light(light)
                self.set_camera.fit_distance(context, object, camera, light)
                bpy.ops.opr.default_rotation()
                self.set_tracking.set_camera_tracking(camera)
                self.set_tracking.set_light_tracking(light)
                self.set_camera.camera_view()  
                bpy.ops.opr.change_viewport()
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
        
        self.manual_import(context, scene, camera, light, file)
        
        return {"FINISHED"}
    
    def manual_import(self, context, scene, camera, light, file):
        if file.endswith(".stl") or file.endswith(".STL"):
            bpy.ops.import_mesh.stl(filepath=file)
            object = self.set_object.selector(context)
            scene.object_name = object.name
            self.set_scene.delete_trace()
            scene.object_rotation_x = np.rad2deg(object.rotation_euler.x)
            scene.object_rotation_y = np.rad2deg(object.rotation_euler.y)
            scene.object_rotation_z = np.rad2deg(object.rotation_euler.z)
            self.set_object.set_origin(object)
            bpy.ops.opr.default_rotation()
            self.set_camera.fit_distance(context, object, camera, light)
            self.set_light.set_light(light)
            self.set_tracking.set_camera_tracking(camera)
            self.set_tracking.set_light_tracking(light)
            self.set_camera.camera_view()
            bpy.ops.opr.default_background_color()
            bpy.ops.opr.change_viewport()


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
        self.set_data = utils.SetData()
        
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
       
        path = scene.image_dir + "/data.txt"
        self.set_data.generate_data(context, path)
        
        return {"FINISHED"}

    def start_render(self, context, scene, object, camera, light, trajectory, h_angle, v_angle):
        if trajectory == 'circular_trajectory':
            h_qnt = round(360/h_angle)
            
            for h_pic in range(h_qnt):
                    scene.camera_position_angle = h_pic * h_angle
                    light.location = camera.location
                    self.set_light.set_light(light)
                    if scene.custom_image:
                        context.scene.render.filepath = f'{scene.image_dir}/{object.name}/{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{"custom-image"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'    
                    else:
                        context.scene.render.filepath = f'{scene.image_dir}/{object.name}/{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{scene.r_color}{"r"}_{scene.g_color}{"g"}_{scene.b_color}{"b"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'
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
                    if scene.custom_image:
                        context.scene.render.filepath = f'{scene.image_dir}/{object.name}/{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{"custom-image"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'    
                    else:
                        context.scene.render.filepath = f'{scene.image_dir}/{object.name}/{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{scene.r_color}{"r"}_{scene.g_color}{"g"}_{scene.b_color}{"b"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'    
                    bpy.ops.render.render(write_still=1)
                    self.set_scene.set_trace(camera.location)

        scene.camera_position_angle = 0
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
        object_path = scene.import_dir

        self.auto_import(context, scene, object, camera, light, object_path)

        return {"FINISHED"}
    
    def auto_import(self, context, scene, object, camera, light, object_path):
        for file in os.listdir(object_path):
            if file.endswith(".stl") or file.endswith(".STL"):
                if object:
                    bpy.data.objects.remove(object, do_unlink=True)
                    self.set_scene.delete_trace()

                filepath = os.path.join(object_path, file)
                bpy.ops.import_mesh.stl(filepath=filepath)
                object = self.set_object.selector(context)
                scene.object_name = object.name
                self.set_object.set_origin(object)
                self.set_light.set_light(light)
                self.set_camera.fit_distance(context, object, camera, light)
                bpy.ops.opr.default_rotation()
                self.set_tracking.set_camera_tracking(camera)
                self.set_tracking.set_light_tracking(light)
                bpy.ops.opr.noise_filter()
                bpy.ops.opr.start_render()


class Opr_set_background_color(bpy.types.Operator):
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
        scene.custom_image = False

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
        scene.custom_image = True
        
        return {'FINISHED'}

class Opr_smoothing_filter(bpy.types.Operator):
    bl_idname = "opr.smoothing_filter"
    bl_label = "Apply Smoothing"

    def __init__(self):
        self.set_object = utils.SetObject()
        self.set_camera = utils.SetCamera()
        self.set_tracking = utils.SetTracking()
        self.set_light = utils.SetLight()
        self.set_scene = utils.SetScene()

    def execute(self, context):
        scene = context.scene
        custom_props = scene.custom_properties
        smoothing = custom_props.get('smoothing', None)

        scene.render.filter_size = smoothing

        return {'FINISHED'}
    

class Opr_noise_filter(bpy.types.Operator):
    bl_idname = "opr.noise_filter"
    bl_label = "Apply Material Noise"

    def __init__(self):
        self.set_object = utils.SetObject()
        self.set_camera = utils.SetCamera()
        self.set_tracking = utils.SetTracking()
        self.set_light = utils.SetLight()
        self.set_scene = utils.SetScene()

    def execute(self, context):
        scene = context.scene.custom_properties
        object = self.set_object.selector(context)
        noise = scene.noise
        
        if object.active_material is None:
            mat = bpy.data.materials.new(name="BlurMaterial")
            object.active_material = mat
        else:
            mat = object.active_material

        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        for node in nodes:
            nodes.remove(node)

        output_node = nodes.new(type="ShaderNodeOutputMaterial")
        principled_node = nodes.new(type="ShaderNodeBsdfPrincipled")
        tex_coord_node = nodes.new(type="ShaderNodeTexCoord")
        mapping_node = nodes.new(type="ShaderNodeMapping")
        noise_node = nodes.new(type="ShaderNodeTexNoise")

        noise_node.inputs['Scale'].default_value = noise

        links.new(tex_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])
        links.new(mapping_node.outputs['Vector'], noise_node.inputs['Vector'])
        links.new(noise_node.outputs['Fac'], principled_node.inputs['Base Color'])
        links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

        return {'FINISHED'}
        

def register_operators():
    bpy.utils.register_class(Opr_change_viewport)
    bpy.utils.register_class(Opr_import_object)
    bpy.utils.register_class(Opr_default_rotation)
    bpy.utils.register_class(Opr_start_render)
    bpy.utils.register_class(Opr_select_directory)
    bpy.utils.register_class(Opr_auto_execute)
    bpy.utils.register_class(Opr_default_background_color)
    bpy.utils.register_class(Opr_set_background_color)
    bpy.utils.register_class(Opr_select_background_image)
    bpy.utils.register_class(Opr_smoothing_filter)
    bpy.utils.register_class(Opr_noise_filter)

def unregister_operators():
    bpy.utils.unregister_class(Opr_change_viewport)
    bpy.utils.unregister_class(Opr_import_object)
    bpy.utils.unregister_class(Opr_default_rotation)
    bpy.utils.unregister_class(Opr_start_render)
    bpy.utils.unregister_class(Opr_select_directory)
    bpy.utils.unregister_class(Opr_auto_execute)
    bpy.utils.unregister_class(Opr_default_background_color)
    bpy.utils.unregister_class(Opr_set_background_color)
    bpy.utils.unregister_class(Opr_select_background_image)
    bpy.utils.unregister_class(Opr_smoothing_filter)
    bpy.utils.unregister_class(Opr_noise_filter)