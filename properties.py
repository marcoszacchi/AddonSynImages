import bpy

class CustomProperties(bpy.types.PropertyGroup):
    auto_exec: bpy.props.BoolProperty(default=False)
    manual_exec: bpy.props.BoolProperty(default=False)
    manual_exec_set: bpy.props.BoolProperty(default=False)
    transformations: bpy.props.BoolProperty(default=False)
    export: bpy.props.BoolProperty(default=False)

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

    image_dir : bpy.props.StringProperty(
        name="",
        description="Directory to save images",
        default="SynImages",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    rotation_steps : bpy.props.IntProperty(
        name="Rotation Steps",
        min=1,
        max=360,
        default=36,
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

def register_properties():
    bpy.utils.register_class(CustomProperties)
    bpy.types.Scene.custom_properties = bpy.props.PointerProperty(type=CustomProperties)

def unregister_properties():
    del bpy.types.Scene.custom_properties
    bpy.utils.unregister_class(CustomProperties)