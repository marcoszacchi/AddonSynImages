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
                bpy.ops.wm.stl_import(filepath=filepath)
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
            bpy.ops.wm.stl_import(filepath=file)
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

    
class Opr_import_texture(bpy.types.Operator):
    bl_idname = "opr.import_texture"
    bl_label = "Import Texture"
    
    def __init__(self):
        self.set_object = utils.SetObject()
        self.set_camera = utils.SetCamera()
        self.set_tracking = utils.SetTracking()
        self.set_light = utils.SetLight()
        self.set_scene = utils.SetScene()
        self.set_render = utils.SetRender()

    def execute(self, context):
        scene = context.scene.custom_properties
        obj = self.set_object.selector(context)
        directory = scene.texture_dir
        texture_name = os.path.basename(os.path.normpath(directory))
        scene.texture_name = texture_name
        scene.texture_scale = 100
        scene.texture_location_x = 0
        scene.texture_location_y = 0
        scene.texture_location_z = 0
        scene.texture_rotation_x = 0
        scene.texture_rotation_y = 0
        scene.texture_rotation_z = 0
        scene.texture_scale_x = 100
        scene.texture_scale_y = 100
        scene.texture_scale_z = 100

        if not directory or not os.path.isdir(directory):
            return {"CANCELLED"}

        texture_files = self.check_texture_files(directory)
        self.setup_material(context, texture_files)
        self.apply_smart_uv_unwrap(obj)

        return {"FINISHED"}

    def check_texture_files(self, directory):
        texture_files = {
            "Color": None,
            "Roughness": None,
            "Metalness": None,
            "NormalDX": None,
            "Displacement": None
        }
        
        for file in os.listdir(directory):
            file_lower = file.lower()
            if "color" in file_lower:
                texture_files["Color"] = os.path.join(directory, file)
            elif "roughness" in file_lower:
                texture_files["Roughness"] = os.path.join(directory, file)
            elif "metalness" in file_lower:
                texture_files["Metalness"] = os.path.join(directory, file)
            elif "normaldx" in file_lower:
                texture_files["NormalDX"] = os.path.join(directory, file)
            elif "displacement" in file_lower:
                texture_files["Displacement"] = os.path.join(directory, file)

        return texture_files

    def create_texture_node(self, nodes, label, location, filepath, color_space='COLOR'):
        tex_node = nodes.new(type='ShaderNodeTexImage')
        tex_node.location = location
        tex_node.label = label
        tex_node.image = bpy.data.images.load(filepath)
        if color_space == 'Non-Color':
            tex_node.image.colorspace_settings.name = 'Non-Color'
        return tex_node

    def setup_material(self, context, texture_files):
        obj = context.active_object
        material = None

        if not obj.data.materials:
            material = bpy.data.materials.new(name="Material")
            obj.data.materials.append(material)
        else:
            material = obj.active_material

        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        tex_coord = nodes.new(type='ShaderNodeTexCoord')
        tex_coord.location = (-1200, 0)

        mapping = nodes.new(type='ShaderNodeMapping')
        mapping.location = (-1000, 0)
        links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

        principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled_bsdf.location = (400, 0)

        material_output = nodes.new(type='ShaderNodeOutputMaterial')
        material_output.location = (800, 0)
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

        if texture_files["Color"]:
            tex_base_color = self.create_texture_node(nodes, "Base Color", (-600, 300), texture_files["Color"])
            links.new(mapping.outputs['Vector'], tex_base_color.inputs['Vector'])
            links.new(tex_base_color.outputs['Color'], principled_bsdf.inputs['Base Color'])

        if texture_files["Roughness"]:
            tex_roughness = self.create_texture_node(nodes, "Roughness", (-600, 150), texture_files["Roughness"], color_space='Non-Color')
            links.new(mapping.outputs['Vector'], tex_roughness.inputs['Vector'])
            links.new(tex_roughness.outputs['Color'], principled_bsdf.inputs['Roughness'])

        if texture_files["Metalness"]:
            tex_metallic = self.create_texture_node(nodes, "Metallic", (-600, 0), texture_files["Metalness"], color_space='Non-Color')
            links.new(mapping.outputs['Vector'], tex_metallic.inputs['Vector'])
            links.new(tex_metallic.outputs['Color'], principled_bsdf.inputs['Metallic'])

        if texture_files["NormalDX"]:
            tex_normal = self.create_texture_node(nodes, "Normal", (-600, -150), texture_files["NormalDX"], color_space='Non-Color')
            normal_map = nodes.new(type='ShaderNodeNormalMap')
            normal_map.location = (-200, -150)
            links.new(mapping.outputs['Vector'], tex_normal.inputs['Vector'])
            links.new(tex_normal.outputs['Color'], normal_map.inputs['Color'])
            links.new(normal_map.outputs['Normal'], principled_bsdf.inputs['Normal'])

        if texture_files["Displacement"]:
            tex_displacement = self.create_texture_node(nodes, "Displacement", (-600, -300), texture_files["Displacement"], color_space='Non-Color')
            displacement = nodes.new(type='ShaderNodeDisplacement')
            displacement.location = (400, -300)
            links.new(mapping.outputs['Vector'], tex_displacement.inputs['Vector'])
            links.new(tex_displacement.outputs['Color'], displacement.inputs['Height'])
            links.new(displacement.outputs['Displacement'], material_output.inputs['Displacement'])

    def apply_smart_uv_unwrap(self, obj):
        if obj.type == 'MESH':
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.smart_project()
            bpy.ops.object.mode_set(mode='OBJECT')

    
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
                        if scene.texture:
                            context.scene.render.filepath = f'{scene.image_dir}/{object.name}_{scene.texture_name}/{object.name}_{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{"custom-image"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'    
                        else:
                            context.scene.render.filepath = f'{scene.image_dir}/{object.name}/{object.name}_{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{"custom-image"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'
                    else:
                        if scene.texture:
                            context.scene.render.filepath = f'{scene.image_dir}/{object.name}_{scene.texture_name}/{object.name}_{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{scene.r_color}{"r"}_{scene.g_color}{"g"}_{scene.b_color}{"b"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'
                        else:
                            context.scene.render.filepath = f'{scene.image_dir}/{object.name}/{object.name}_{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{scene.r_color}{"r"}_{scene.g_color}{"g"}_{scene.b_color}{"b"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'
                    
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
                        if scene.texture:
                            context.scene.render.filepath = f'{scene.image_dir}/{object.name}_{scene.texture_name}/{object.name}_{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{"custom-image"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'    
                        else:
                            context.scene.render.filepath = f'{scene.image_dir}/{object.name}/{object.name}_{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{"custom-image"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'
                    else:
                        if scene.texture:
                            context.scene.render.filepath = f'{scene.image_dir}/{object.name}_{scene.texture_name}/{object.name}_{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{scene.r_color}{"r"}_{scene.g_color}{"g"}_{scene.b_color}{"b"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'
                        else:
                            context.scene.render.filepath = f'{scene.image_dir}/{object.name}/{object.name}_{scene.camera_position_angle:.2f}{"d"}_{scene.camera_height_angle:.2f}{"d"}_{scene.r_color}{"r"}_{scene.g_color}{"g"}_{scene.b_color}{"b"}_{scene.smoothing}{"px"}_{scene.noise}{"%"}'    
                    
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
                bpy.ops.wm.stl_import(filepath=filepath)
                object = self.set_object.selector(context)
                scene.object_name = object.name
                self.set_object.set_origin(object)
                self.set_light.set_light(light)
                self.set_camera.fit_distance(context, object, camera, light)
                bpy.ops.opr.default_rotation()
                self.set_tracking.set_camera_tracking(camera)
                self.set_tracking.set_light_tracking(light)
                bpy.ops.opr.import_texture()
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


def register_operators():
    bpy.utils.register_class(Opr_change_viewport)
    bpy.utils.register_class(Opr_import_object)
    bpy.utils.register_class(Opr_import_texture)
    bpy.utils.register_class(Opr_default_rotation)
    bpy.utils.register_class(Opr_start_render)
    bpy.utils.register_class(Opr_select_directory)
    bpy.utils.register_class(Opr_auto_execute)
    bpy.utils.register_class(Opr_default_background_color)
    bpy.utils.register_class(Opr_set_background_color)
    bpy.utils.register_class(Opr_select_background_image)
    bpy.utils.register_class(Opr_smoothing_filter)

def unregister_operators():
    bpy.utils.unregister_class(Opr_change_viewport)
    bpy.utils.unregister_class(Opr_import_object)
    bpy.utils.unregister_class(Opr_import_texture)
    bpy.utils.unregister_class(Opr_default_rotation)
    bpy.utils.unregister_class(Opr_start_render)
    bpy.utils.unregister_class(Opr_select_directory)
    bpy.utils.unregister_class(Opr_auto_execute)
    bpy.utils.unregister_class(Opr_default_background_color)
    bpy.utils.unregister_class(Opr_set_background_color)
    bpy.utils.unregister_class(Opr_select_background_image)
    bpy.utils.unregister_class(Opr_smoothing_filter)