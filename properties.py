import bpy

class CustomSceneProperties(bpy.types.PropertyGroup):

    import_dir: bpy.props.StringProperty(
        name="Diretório de Importação",
        description="Diretório para importar objetos",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    file_dir: bpy.props.StringProperty(
        name="Diretório de Arquivo",
        description="Diretório para importar um único objeto",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )

    image_dir: bpy.props.StringProperty(
        name="Diretório de Imagens",
        description="Diretório para salvar imagens",
        default="SynImages",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    rotation_steps: bpy.props.IntProperty(
        name="Passos de Rotação",
        min=1,
        max=360,
        default=36,
    )

    auto_exec: bpy.props.BoolProperty(
        default=False
        )

    manual_exec: bpy.props.BoolProperty(
        default=False
        )


def register_properties():
    bpy.utils.register_class(CustomSceneProperties)
    bpy.types.Scene.custom_properties = bpy.props.PointerProperty(type=CustomSceneProperties)

def unregister_properties():
    del bpy.types.Scene.custom_properties
    bpy.utils.unregister_class(CustomSceneProperties)