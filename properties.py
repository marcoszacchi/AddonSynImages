import bpy

class CustomProperties(bpy.types.PropertyGroup):
    auto_exec: bpy.props.BoolProperty(default=False)
    manual_exec: bpy.props.BoolProperty(default=False)
    manual_exec_set: bpy.props.BoolProperty(default=False)
    trajectory: bpy.props.BoolProperty(default=False)
    transformations: bpy.props.BoolProperty(default=False)
    background: bpy.props.BoolProperty(default=False)
    background_color: bpy.props.BoolProperty(default=False)
    background_image: bpy.props.BoolProperty(default=False)
    export: bpy.props.BoolProperty(default=False)

    cam_trajectory: bpy.props.EnumProperty(
        items=[
            ('circular_trajectory', "Circular", "Circular Trajectory"),
            ('spherical_trajectory', "Spherical", "Spherical Trajectory")
        ],
        name="",
        description=""
    )

    import_dir : bpy.props.StringProperty(
        name="",
        description="Directory to import objects",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    file_dir : bpy.props.StringProperty(
        name="",
        description="Directory to import single object",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )

    object_rotation_x : bpy.props.FloatProperty(
        name="Object Rotation X",
    )

    object_rotation_y : bpy.props.FloatProperty(
        name="Object Rotation Y",
    )

    object_rotation_z : bpy.props.FloatProperty(
        name="Object Rotation Z",
    )

    image_dir : bpy.props.StringProperty(
        name="",
        description="Directory to save images",
        default="SynImages",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    background_dir : bpy.props.StringProperty(
        name="",
        description="Directory to import background",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )

    horizontal_rotation_steps : bpy.props.IntProperty(
        name="Rotation Steps",
        min=1,
        max=360,
        default=36,
    )

    vertical_rotation_steps : bpy.props.IntProperty(
        name="Rotation Steps",
        min=1,
        max=180,
        default=18,
    )

    camera_position_angle : bpy.props.FloatProperty(
        name="Camera Height",
        min = 0,
        max = 360,
        default=0,
    )

    camera_height_angle : bpy.props.FloatProperty(
        name="Camera Height",
        min = 0.0001,
        max = 180,
        default=90,
    )

    scaling_percentage : bpy.props.IntProperty(
        name="Scaling",
        min=0,
        max=100,
        default=0,
    )

    translation_percentage : bpy.props.IntProperty(
        name="Translation",
        min=0,
        max=100,
        default=0,
    )

    light_intensity : bpy.props.IntProperty(
        name="Light Intensity",
        min=0,
        max=200,
        default=100,
    )

    background_type: bpy.props.EnumProperty(
        items=[
            ('solid_color', "Solid Color", "RGB Solid Color"),
            ('image', "Image", "Fixed Image")
        ],
        name="",
        description=""
    )

    r_color: bpy.props.IntProperty(
        name="R",
        min=0,
        max=255,
        default=13,
    )

    g_color: bpy.props.IntProperty(
        name="G",
        min=0,
        max=255,
        default=13,
    )

    b_color: bpy.props.IntProperty(
        name="B",
        min=0,
        max=255,
        default=13,
    )

def register_properties():
    bpy.utils.register_class(CustomProperties)
    bpy.types.Scene.custom_properties = bpy.props.PointerProperty(type=CustomProperties)

def unregister_properties():
    del bpy.types.Scene.custom_properties
    bpy.utils.unregister_class(CustomProperties)