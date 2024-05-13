import bpy

class CustomProperties(bpy.types.PropertyGroup):
    auto_exec: bpy.props.BoolProperty(default=False)#type: ignore
    manual_exec: bpy.props.BoolProperty(default=False)#type: ignore
    manual_exec_set: bpy.props.BoolProperty(default=False)#type: ignore
    trajectory: bpy.props.BoolProperty(default=False)#type: ignore
    transformations: bpy.props.BoolProperty(default=False)#type: ignore
    background: bpy.props.BoolProperty(default=False)#type: ignore
    background_color: bpy.props.BoolProperty(default=False)#type: ignore
    background_image: bpy.props.BoolProperty(default=False)#type: ignore
    export: bpy.props.BoolProperty(default=False)#type: ignore
    multiple: bpy.props.BoolProperty(default=False)#type: ignore
    single: bpy.props.BoolProperty(default=False)#type: ignore

    object_name : bpy.props.StringProperty(
        name="Object Name",
        description="Name of the object",
        default="",
        maxlen=1024  # Opcional: limita o comprimento máximo da string
    )#type: ignore

    cam_trajectory : bpy.props.EnumProperty(
        items=[
            ('circular_trajectory', "Circular", "Circular Trajectory"),
            ('spherical_trajectory', "Spherical", "Spherical Trajectory")
        ],
        name="",
        description=""
    )#type: ignore

    import_dir : bpy.props.StringProperty(
        name="",
        description="Directory to import objects",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )#type: ignore

    file_dir : bpy.props.StringProperty(
        name="",
        description="Directory to import single object",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )#type: ignore

    object_rotation_x : bpy.props.FloatProperty(
        name="Object Rotation X",
    )#type: ignore

    object_rotation_y : bpy.props.FloatProperty(
        name="Object Rotation Y",
    )#type: ignore

    object_rotation_z : bpy.props.FloatProperty(
        name="Object Rotation Z",
    )#type: ignore

    image_dir : bpy.props.StringProperty(
        name="",
        description="Directory to save images",
        default="C:/SynImages",
        maxlen=1024,
        subtype='DIR_PATH'
    )#type: ignore

    background_dir : bpy.props.StringProperty(
        name="",
        description="Directory to import background",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )#type: ignore

    horizontal_rotation_steps : bpy.props.IntProperty(
        name="Rotation Steps",
        min=1,
        max=360,
        default=36,
    )#type: ignore

    vertical_rotation_steps : bpy.props.IntProperty(
        name="Rotation Steps",
        min=1,
        max=180,
        default=18,
    )#type: ignore

    camera_position_angle : bpy.props.FloatProperty(
        name="Camera Height",
        min = 0,
        max = 360,
        default=0,
    )#type: ignore

    camera_height_angle : bpy.props.FloatProperty(
        name="Camera Height",
        min = 0.0001,
        max = 180,
        default=90,
    )#type: ignore

    scaling_percentage : bpy.props.IntProperty(
        name="Scaling",
        min=0,
        max=500,
        default=100,
    )#type: ignore

    horizontal_translation : bpy.props.FloatProperty(
        name="Horizontal Translation",
        min=-50,
        max=50,
        default=0,
    )#type: ignore

    vertical_translation : bpy.props.FloatProperty(
        name="Vertical Translation",
        min=-50,
        max=50,
        default=0,
    )#type: ignore

    light_intensity : bpy.props.IntProperty(
        name="Light Intensity",
        min=0,
        max=200,
        default=100,
    )#type: ignore

    background_type : bpy.props.EnumProperty(
        items=[
            ('solid_color', "Solid Color", "RGB Solid Color"),
            ('image', "Image", "Fixed Image")
        ],
        name="",
        description=""
    )#type: ignore

    r_color : bpy.props.IntProperty(
        name="R",
        min=0,
        max=255,
        default=13,
    )#type: ignore

    g_color : bpy.props.IntProperty(
        name="G",
        min=0,
        max=255,
        default=13,
    )#type: ignore

    b_color : bpy.props.IntProperty(
        name="B",
        min=0,
        max=255,
        default=13,
    )#type: ignore

def register_properties():
    bpy.utils.register_class(CustomProperties)
    bpy.types.Scene.custom_properties = bpy.props.PointerProperty(type=CustomProperties)

def unregister_properties():
    del bpy.types.Scene.custom_properties
    bpy.utils.unregister_class(CustomProperties)