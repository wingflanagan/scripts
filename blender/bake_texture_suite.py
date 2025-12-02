bl_info = {
    "name": "Bake Texture Suite",
    "author": "Codex",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Bake Suite",
    "description": "One-click texture baking with selective passes, UV creation, packing, and emissive option.",
    "category": "Material",
}

import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)


def ensure_cycles(scene):
    """Switch to Cycles if needed and return previous engine name."""
    prev_engine = scene.render.engine
    if prev_engine != "CYCLES":
        scene.render.engine = "CYCLES"
    return prev_engine


def ensure_uv_map(obj, uv_name, auto_create=True):
    """Ensure a UV map exists and is active for baking."""
    uv_layers = obj.data.uv_layers
    uv = uv_layers.get(uv_name)
    if uv is None and auto_create:
        uv = uv_layers.new(name=uv_name)
        prev_mode = obj.mode
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02, area_weight=0.0, correct_aspect=True)
        bpy.ops.object.mode_set(mode=prev_mode)
    if uv is None:
        raise RuntimeError(f"No UV map named '{uv_name}' and auto-create disabled")
    uv_layers.active = uv
    uv_layers.active_index = uv_layers.find(uv.name)
    return uv


def create_bake_image(obj, pass_key, width, height):
    name = f"{obj.name}_{pass_key}_BAKED"
    image = bpy.data.images.new(name=name, width=width, height=height, alpha=False, float_buffer=False)
    image.alpha_mode = "STRAIGHT"
    try:
        image.colorspace_settings.name = "Non-Color" if pass_key == "NORMAL" else "sRGB"
    except Exception:
        pass
    return image


def find_principled(mat):
    if not mat or not mat.use_nodes:
        return None
    for node in mat.node_tree.nodes:
        if node.type == "BSDF_PRINCIPLED":
            return node
    return None


def ensure_principled(mat):
    """Ensure a Principled BSDF exists and return it."""
    p = find_principled(mat)
    if p:
        return p
    nt = mat.node_tree
    p = nt.nodes.new("ShaderNodeBsdfPrincipled")
    p.location = (0, 0)
    # Reasonable defaults.
    p.inputs["Roughness"].default_value = 0.5
    p.inputs["Metallic"].default_value = 0.0
    return p


def replace_input(nt, input_socket, output_socket):
    if input_socket is None or output_socket is None:
        return
    for link in list(input_socket.links):
        nt.links.remove(link)
    nt.links.new(output_socket, input_socket)


def ensure_bake_nodes(obj, pass_key, image):
    """Create/assign image texture nodes for baking; return images that were replaced."""
    replaced = []
    colorspace = "Non-Color" if pass_key == "NORMAL" else "sRGB"
    for slot in obj.material_slots:
        mat = slot.material
        if not mat or not mat.use_nodes:
            continue
        nt = mat.node_tree
        image_node = nt.nodes.get(f"{pass_key}_BAKE_NODE")
        if image_node is None:
            image_node = nt.nodes.new("ShaderNodeTexImage")
            image_node.name = f"{pass_key}_BAKE_NODE"
            image_node.label = f"{pass_key} Bake"
            image_node.location = (-400, 400)
        if image_node.image and image_node.image != image:
            replaced.append(image_node.image)
        image_node.image = image
        image_node.interpolation = "Smart"
        image_node.select = True
        try:
            image_node.image.colorspace_settings.name = colorspace
        except Exception:
            pass
        nt.nodes.active = image_node
    return replaced


def get_bake_node(mat, pass_key):
    if not mat or not mat.use_nodes:
        return None
    return mat.node_tree.nodes.get(f"{pass_key}_BAKE_NODE")


def choose_primary_pass(baked_images, settings):
    if settings.make_emissive and settings.emissive_source in baked_images:
        return settings.emissive_source
    for candidate in ("COMBINED", "DIFFUSE"):
        if candidate in baked_images:
            return candidate
    for candidate in ("AO", "SHADOW", "GLOSSY", "TRANSMISSION", "EMIT"):
        if candidate in baked_images:
            return candidate
    return None


def ensure_output_node(nt):
    for node in nt.nodes:
        if node.type == "OUTPUT_MATERIAL" and node.is_active_output:
            return node
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.is_active_output = True
    out.location = (400, 0)
    return out


def connect_normal(nt, principled, normal_node, image_node):
    if not principled or not normal_node or not image_node:
        return
    replace_input(nt, normal_node.inputs.get("Color"), image_node.outputs.get("Color"))
    replace_input(nt, principled.inputs.get("Normal"), normal_node.outputs.get("Normal"))


def apply_bake_to_material(mat, baked_images, settings):
    """Wire baked outputs to the material (Base Color + optional camera-only emission + normal)."""
    if not mat or not mat.use_nodes:
        return
    nt = mat.node_tree
    principled = ensure_principled(mat)

    primary_pass = choose_primary_pass(baked_images, settings)
    image_node = get_bake_node(mat, primary_pass) if primary_pass else None
    if image_node and image_node.outputs.get("Color"):
        replace_input(nt, principled.inputs.get("Base Color"), image_node.outputs.get("Color"))

    # Normal map hookup.
    if "NORMAL" in baked_images:
        normal_image_node = get_bake_node(mat, "NORMAL")
        normal_map_node = None
        for node in nt.nodes:
            if node.type == "NORMAL_MAP":
                normal_map_node = node
                break
        if normal_map_node is None:
            normal_map_node = nt.nodes.new("ShaderNodeNormalMap")
            normal_map_node.location = principled.location.x - 250, principled.location.y - 250
        connect_normal(nt, principled, normal_map_node, normal_image_node)

    # Emission without lighting the scene: only for camera rays.
    output_node = ensure_output_node(nt)
    if settings.make_emissive and settings.emissive_source in baked_images and image_node:
        emission_node = nt.nodes.get("BAKE_EMISSION_NODE")
        if emission_node is None:
            emission_node = nt.nodes.new("ShaderNodeEmission")
            emission_node.name = "BAKE_EMISSION_NODE"
            emission_node.label = "Bake Emission"
            emission_node.location = principled.location.x + 250, principled.location.y + 250
        replace_input(nt, emission_node.inputs.get("Color"), image_node.outputs.get("Color"))
        emission_node.inputs["Strength"].default_value = 1.0

        light_path = nt.nodes.get("BAKE_LIGHTPATH_NODE")
        if light_path is None:
            light_path = nt.nodes.new("ShaderNodeLightPath")
            light_path.name = "BAKE_LIGHTPATH_NODE"
            light_path.label = "Bake Light Path"
            light_path.location = emission_node.location.x - 250, emission_node.location.y - 150

        mix_shader = nt.nodes.get("BAKE_MIX_NODE")
        if mix_shader is None:
            mix_shader = nt.nodes.new("ShaderNodeMixShader")
            mix_shader.name = "BAKE_MIX_NODE"
            mix_shader.label = "Camera Emission Mix"
            mix_shader.location = emission_node.location.x + 250, emission_node.location.y

        replace_input(nt, mix_shader.inputs.get("Fac"), light_path.outputs.get("Is Camera Ray"))
        # mix: Shader1 used when Fac=0, Shader2 when Fac=1. We want emission for camera rays.
        replace_input(nt, mix_shader.inputs[1], principled.outputs.get("BSDF"))
        replace_input(nt, mix_shader.inputs[2], emission_node.outputs.get("Emission"))
        replace_input(nt, output_node.inputs.get("Surface"), mix_shader.outputs.get("Shader"))
    else:
        # Default: drive base color, keep standard Principled output.
        replace_input(nt, output_node.inputs.get("Surface"), principled.outputs.get("BSDF"))


def purge_images(images):
    for img in images:
        if img and img.users == 0:
            try:
                bpy.data.images.remove(img)
            except RuntimeError:
                # Image may still be packed or referenced elsewhere.
                pass


def bake_pass(context, bake_type, margin):
    scene = context.scene
    bake_settings = scene.render.bake
    bake_settings.use_clear = True
    bake_settings.target = "IMAGE_TEXTURES"
    bake_settings.margin = margin
    kwargs = {"type": bake_type}

    def supported_filters():
        try:
            enum_items = bpy.types.BakeSettings.bl_rna.properties["pass_filter"].enum_items.keys()
            return set(enum_items)
        except Exception:
            return set()

    if bake_type in {"DIFFUSE", "GLOSSY", "TRANSMISSION"}:
        kwargs["pass_filter"] = {"DIRECT", "INDIRECT", "COLOR"}
    # For COMBINED, leave pass_filter unset to let Blender include all supported contributions by default.
    if bake_type == "NORMAL":
        bake_settings.normal_space = "TANGENT"

    def run_bake(kw):
        return bpy.ops.object.bake(**kw)

    try:
        result = run_bake(kwargs)
    except Exception as exc:
        # Handle pass_filter incompatibility by stripping it and retrying once.
        msg = str(exc)
        if "pass_filter" in kwargs and "not found" in msg:
            kw2 = dict(kwargs)
            kw2.pop("pass_filter", None)
            result = run_bake(kw2)
        else:
            raise

    if isinstance(result, set) and "FINISHED" not in result:
        raise RuntimeError(f"Baking {bake_type} failed with status: {result}")


class BakeSuiteSettings(bpy.types.PropertyGroup):
    resolution: IntProperty(
        name="Resolution",
        description="Resolution for baked images",
        default=4096,
        min=64,
        max=16384,
    )
    uv_name: StringProperty(
        name="UV Map",
        description="UV map to use/create for baking",
        default="BakeUV",
    )
    auto_create_uv: BoolProperty(
        name="Auto-create UV",
        description="Create and unwrap a bake UV map if missing",
        default=True,
    )
    pack_images: BoolProperty(
        name="Pack Images",
        description="Pack baked images into the .blend file",
        default=True,
    )
    purge_originals: BoolProperty(
        name="Purge Originals",
        description="Remove replaced image datablocks after baking",
        default=False,
    )
    make_emissive: BoolProperty(
        name="Make Emissive",
        description="Drive material emission from baked map (lighting-free)",
        default=False,
    )
    bake_combined: BoolProperty(name="Combined", default=True)
    bake_diffuse: BoolProperty(name="Diffuse/Albedo", default=False)
    bake_ao: BoolProperty(name="Ambient Occlusion", default=True)
    bake_shadow: BoolProperty(name="Shadow", default=False)
    bake_normal: BoolProperty(name="Normal", default=True)
    bake_emit: BoolProperty(name="Emission", default=False)
    bake_glossy: BoolProperty(name="Glossy", default=False)
    bake_transmission: BoolProperty(name="Transmission", default=False)
    margin: IntProperty(
        name="Margin (px)",
        description="Bake margin padding in pixels",
        default=16,
        min=0,
        max=128,
    )
    emissive_source: EnumProperty(
        name="Emissive From",
        description="Which baked pass to wire into emission when enabled",
        items=[
            ("COMBINED", "Combined", "Use Combined bake for emission"),
            ("DIFFUSE", "Diffuse", "Use Diffuse/Albedo bake for emission"),
            ("EMIT", "Emission", "Use Emission bake"),
        ],
        default="COMBINED",
    )


class BAKE_OT_texture_suite(bpy.types.Operator):
    bl_idname = "object.bake_texture_suite"
    bl_label = "Bake Selected Maps"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.bake_suite
        obj = context.object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Active object must be a mesh")
            return {"CANCELLED"}

        selected_passes = [
            ("COMBINED", settings.bake_combined),
            ("DIFFUSE", settings.bake_diffuse),
            ("AO", settings.bake_ao),
            ("SHADOW", settings.bake_shadow),
            ("NORMAL", settings.bake_normal),
            ("EMIT", settings.bake_emit),
            ("GLOSSY", settings.bake_glossy),
            ("TRANSMISSION", settings.bake_transmission),
        ]
        passes_to_bake = [p for p, enabled in selected_passes if enabled]
        if not passes_to_bake:
            self.report({"ERROR"}, "Select at least one bake pass")
            return {"CANCELLED"}

        scene = context.scene
        prev_engine = ensure_cycles(scene)

        # Ensure UVs.
        try:
            ensure_uv_map(obj, settings.uv_name, settings.auto_create_uv)
        except RuntimeError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        # Prepare selection/state.
        prev_selection = [o for o in context.selected_objects]
        prev_active = context.view_layer.objects.active
        for o in prev_selection:
            o.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj

        baked_images = {}
        replaced_images = []
        try:
            for pass_key in passes_to_bake:
                image = create_bake_image(obj, pass_key, settings.resolution, settings.resolution)
                baked_images[pass_key] = image
                replaced_images.extend(ensure_bake_nodes(obj, pass_key, image))
                bake_pass(context, pass_key, settings.margin)
                if settings.pack_images:
                    try:
                        image.pack()
                    except RuntimeError:
                        pass
        except Exception as exc:
            self.report({"ERROR"}, f"Bake failed: {exc}")
            scene.render.engine = prev_engine
            for o in prev_selection:
                o.select_set(True)
            if prev_active:
                context.view_layer.objects.active = prev_active
            return {"CANCELLED"}

        # Wire baked results once all passes are done.
        for slot in obj.material_slots:
            mat = slot.material
            if not mat or not mat.use_nodes:
                continue
            apply_bake_to_material(mat, baked_images, settings)

        # Restore selection and engine.
        for o in prev_selection:
            o.select_set(True)
        if prev_active:
            context.view_layer.objects.active = prev_active
        scene.render.engine = prev_engine

        if settings.purge_originals:
            purge_images(replaced_images)

        self.report({"INFO"}, f"Baked: {', '.join(passes_to_bake)}")
        return {"FINISHED"}


class BAKE_PT_texture_suite(bpy.types.Panel):
    bl_label = "Bake Suite"
    bl_idname = "BAKE_PT_texture_suite"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Bake Suite"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None and obj.type == "MESH"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.bake_suite

        layout.label(text="Passes")
        col = layout.column(align=True)
        col.prop(settings, "bake_combined")
        col.prop(settings, "bake_diffuse")
        col.prop(settings, "bake_ao")
        col.prop(settings, "bake_shadow")
        col.prop(settings, "bake_normal")
        col.prop(settings, "bake_emit")
        col.prop(settings, "bake_glossy")
        col.prop(settings, "bake_transmission")

        layout.separator()
        layout.label(text="Target")
        row = layout.row(align=True)
        row.prop(settings, "resolution")
        row.prop(settings, "margin")
        layout.prop(settings, "uv_name")
        layout.prop(settings, "auto_create_uv")
        layout.prop(settings, "pack_images")
        layout.prop(settings, "purge_originals")

        layout.separator()
        layout.prop(settings, "make_emissive")
        sub = layout.column()
        sub.enabled = settings.make_emissive
        sub.prop(settings, "emissive_source")

        layout.operator(BAKE_OT_texture_suite.bl_idname, icon="RENDER_STILL")


classes = (
    BakeSuiteSettings,
    BAKE_OT_texture_suite,
    BAKE_PT_texture_suite,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bake_suite = PointerProperty(type=BakeSuiteSettings)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bake_suite


if __name__ == "__main__":
    register()
