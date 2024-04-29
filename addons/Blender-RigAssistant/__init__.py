# Addon info
bl_info = {
    "name": "Blender Rig Assistant",
    "description":"Rig anything with ease",
    "author": "Thomas Breuker",
    "blender": (3, 4, 1),
    "version": (0, 0, 2),
    "category": "Rigging",
    "location": "View3D > Sidebar > RigAssistant",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
}

import bpy
from mathutils import Vector
from .operators.rigshapes import OBJECT_OT_create_circle, OBJECT_OT_create_cube, OBJECT_OT_create_piramid, OBJECT_OT_create_sphere, OBJECT_OT_create_square
from .operators.ctrlbones import OBJECT_OT_suffix_l, OBJECT_OT_suffix_r, OBJECT_OT_create_control_bone, OBJECT_OT_create_local_offset_bone, OBJECT_OT_add_controls, OBJECT_OT_remove_controls
from .operators.cnstrbones import OBJECT_OT_remove_all_cnstr, OBJECT_OT_create_cnstr, OBJECT_OT_add_cnstr, OBJECT_OT_remove_cnstr_bone, OBJECT_OT_remove_selected_bone, OBJECT_OT_append_cnstr, OBJECT_OT_create_cnstr_ctrl
from .operators.deformbones import OBJECT_OT_create_armature, OBJECT_OT_disconnect_bones, OBJECT_OT_remove_roll, OBJECT_OT_chain_parent,OBJECT_OT_chain_rename

# Tells the which constraint to pick when using create constraint add constraint or append constraint.
class constraint_properties(bpy.types.PropertyGroup):
    constraint_enum : bpy.props.EnumProperty(
        name = "type",
        description = "choose the type of constraint",
        items = [('OP1',"TRANSFORMS",""),
                ('OP2',"LOCATION",""),
                ('OP3',"ROTATION",""),
                ('OP4',"SCALE",""),
                ('OP5',"IK",""),
                ('OP6',"NONE",""),

        ]

    )
#switches between local or world space for control bones
class world_local_properties(bpy.types.PropertyGroup):
    world_local_enum : bpy.props.EnumProperty(
        name = "space",
        description = "choose between world or local",
        items = [('OP1',"LOCAL",""),
                ('OP2',"WORLD",""),

        ]

    )
#UI window
class VIEW3D_PT_blender_rig_assistant(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rig Assistant"
    bl_label = "Rig Assistant"  

  
    def draw(self, context):
        coltop = self.layout.column(heading="Armature Creator")
        coltop.label(text="Armature")
        coltop.operator('object.create_armature',icon = 'ARMATURE_DATA')
        coltop.operator('object.disconnect_bones', icon = 'BONE_DATA')
        coltop.operator('object.remove_roll', icon ='OUTLINER_DATA_GREASEPENCIL')
        coltop.operator('object.chain_parent',icon ='DECORATE_LINKED')
        coltop.operator('object.chain_rename',icon ='DECORATE_LINKED')
        self.layout.separator()
        
        rowa=self.layout.row(align=True)
        rowa.operator('object.prefix_l', icon ='EVENT_L')
        rowa.operator('object.prefix_r', icon ='EVENT_R')
        self.layout.separator()

        col= self.layout.column()
        col.label(text="Constraints")
        col.prop(context.scene.type_constrain, "constraint_enum")
        col.operator('object.create_cnstr', icon = 'CONSTRAINT_BONE')
        col.operator('object.append_cnstr', icon = 'CONSTRAINT')
        col.operator('object.add_cnstr', icon = 'GROUP_BONE')
        self.layout.separator()

        colb=self.layout.column()
        colb.label(text="Removing Bones and Constraints")
        colb.operator('object.remove_all_cnstr', icon = 'CANCEL')
        colb.operator('object.remove_cnstr_bone', icon = 'CONSTRAINT_BONE')
        colb.operator('object.remove_selected_bone', icon = 'BONE_DATA')
        
        self.layout.separator()

        colc= self.layout.column()
        colc.label(text="Controls and Offsets")
        colc.prop(context.scene.local_world_switch, "world_local_enum")
        colc.operator('object.create_control_bone', icon = 'OUTLINER_DATA_ARMATURE')
        colc.operator('object.create_local_offset_bone' , icon = 'OUTLINER_DATA_ARMATURE')
        colc.operator('object.create_cnstr_ctrl',icon ='BONE_DATA')
        self.layout.separator()
        
        cold=self.layout.column()
        cold.label(text="Control Shapes")
        cold.operator('object.add_controls', icon = 'MOD_SKIN')
        cold.operator('object.remove_controls', icon ='MOD_PHYSICS')
        self.layout.separator()
 
        colf=self.layout.grid_flow(row_major=True, columns=2, align=True)
        colf.operator('object.create_circle', icon ='MESH_CIRCLE')
        colf.operator('object.create_cube', icon ='CUBE')
        colf.operator('object.create_piramid', icon ='CONE')
        colf.operator('object.create_sphere', icon ='SPHERE')
        colf.operator('object.create_square', icon = 'MESH_PLANE')

blender_classes = [
    constraint_properties,
    world_local_properties,
    OBJECT_OT_remove_all_cnstr,
    OBJECT_OT_create_cnstr,
    OBJECT_OT_add_cnstr,
    OBJECT_OT_chain_parent,
    OBJECT_OT_chain_rename,
    OBJECT_OT_create_cnstr_ctrl,
    VIEW3D_PT_blender_rig_assistant,
    OBJECT_OT_remove_cnstr_bone,
    OBJECT_OT_remove_selected_bone,
    OBJECT_OT_create_control_bone,
    OBJECT_OT_create_local_offset_bone,
    OBJECT_OT_add_controls,
    OBJECT_OT_remove_controls,
    OBJECT_OT_remove_roll,
    OBJECT_OT_append_cnstr,
    OBJECT_OT_create_armature,
    OBJECT_OT_disconnect_bones,
    OBJECT_OT_suffix_l,
    OBJECT_OT_suffix_r,
    OBJECT_OT_create_circle,
    OBJECT_OT_create_cube,
    OBJECT_OT_create_piramid,
    OBJECT_OT_create_sphere,
    OBJECT_OT_create_square,
    ]


def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)

    bpy.types.Scene.type_constrain = bpy.props.PointerProperty(type = constraint_properties)
    bpy.types.Scene.local_world_switch = bpy.props.PointerProperty(type = world_local_properties)
def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class) 
    del bpy.types.Scene.type_constrain
    del bpy.types.Scene.local_world_switch 
