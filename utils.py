import bpy
import mathutils
import numpy as np

class SetRender:
    def set_viewport(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'

class SetObject:
    def selector(self, context):
        fixed_object_names = ['Camera', 'Light', 'Origin']

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
    
    def camera_view(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                            space.region_3d.view_perspective = 'CAMERA'
                            space.overlay.show_floor = False
                            space.overlay.show_axis_x = False
                            space.overlay.show_axis_y = False
                            return
    
    def space_view(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                            space.region_3d.view_perspective = 'PERSP'
                            space.overlay.show_floor = False
                            space.overlay.show_axis_x = False
                            space.overlay.show_axis_y = False
                            return

class SetTracking:
    def create_empty(self):
        empty_name="Origin"
        if empty_name in bpy.data.objects:
            empty = bpy.data.objects[empty_name]
        else:
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
            empty = bpy.context.view_layer.objects.active
            empty.name = empty_name
        return empty
    
    def set_camera_tracking(self, camera):
        empty = self.create_empty()

        track_to_constraint = False

        for constraint in camera.constraints:
            if constraint.type == 'TRACK_TO':
                constraint.target = empty
                track_to_constraint = True
                break

        if not track_to_constraint:
            constraint = camera.constraints.new(type='TRACK_TO')
            constraint.target = empty

    def set_light_tracking(self, light):
        empty = self.create_empty()

        track_to_constraint = False

        for constraint in light.constraints:
            if constraint.type == 'TRACK_TO':
                constraint.target = empty
                track_to_constraint = True
                break
        
        if not track_to_constraint:
            constraint = light.constraints.new(type='TRACK_TO')
            constraint.target = empty

class SetLight:
    def set_light(self, light):
        light.data.type = 'SUN'
        light.data.use_shadow = False
    
    def set_light_intensity(self, light, intensity):
        value = (2 * intensity) / 100
        light.data.energy = value

class SetScene:
    def set_trace(self, location):
        bpy.ops.object.empty_add(type='SPHERE', location=location)
    
    def delete_trace(self):
        traces = bpy.context.scene.objects
        traces_to_delete = [obj for obj in traces if obj.type == 'EMPTY' and obj.empty_display_type == 'SPHERE']
        for trace in traces_to_delete:
            bpy.data.objects.remove(trace, do_unlink=True)

class SetWorld:
    def set_background_color(self, r, g, b):
        a = 255
        r, g, b, a = [x / 255.0 for x in (r, g, b, a)]
        world = bpy.context.scene.world
        world.use_nodes = True
        node_tree = world.node_tree
        nodes = node_tree.nodes
        nodes.clear()
        node_background = nodes.new(type='ShaderNodeBackground')
        node_output = nodes.new(type='ShaderNodeOutputWorld')
        node_background.inputs['Color'].default_value = (r, g, b, a)
        node_tree.links.new(node_background.outputs['Background'], node_output.inputs['Surface'])

    def set_background_image(self, image_path):
        image = bpy.data.images.load(image_path)

        world = bpy.context.scene.world
        world.use_nodes = True
        node_tree = world.node_tree
        nodes = node_tree.nodes
        nodes.clear()

        node_background = nodes.new('ShaderNodeBackground')
        env_texture = nodes.new('ShaderNodeTexEnvironment')
        world_output = nodes.new('ShaderNodeOutputWorld')

        env_texture.image = image

        links = node_tree.links
        link_env_bg = None
        for link in links:
            if link.from_node == env_texture and link.to_node == node_background:
                link_env_bg = link
                break

        if not link_env_bg:
            links.new(env_texture.outputs["Color"], node_background.inputs["Color"])
        
        link_bg_output = None
        for link in links:
            if link.from_node == node_background and link.to_node == world_output:
                link_bg_output = link
                break

        if not link_bg_output:
            links.new(node_background.outputs["Background"], world_output.inputs["Surface"])
        