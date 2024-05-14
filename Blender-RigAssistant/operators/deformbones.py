import bpy
from mathutils import Vector
# Handles everything related to deform bones parenting and naming

class OBJECT_OT_disconnect_bones(bpy.types.Operator):
    bl_idname = 'object.disconnect_bones'
    bl_label = "Disconnect Bones"
    #Simple operator disconnects bones from eachother

    def execute (self, context):
        bpy.ops.armature.parent_clear(type='DISCONNECT')        

        return{'FINISHED'} 

class OBJECT_OT_create_armature(bpy.types.Operator):
    bl_idname = 'object.create_armature'
    bl_label = "Create An Armature"
    # Creates a starting armature with a zero-ed out bone the is called root

    def execute (self, context):

        if bpy.context.selected_objects:
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.active_bone.name = "root"
        bpy.ops.transform.translate(value=(0, 1, -1), orient_type='GLOBAL')
        bpy.context.object.data.collections.new('Deform')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.context.object.data.collections['Deform'].assign(bpy.context.object.pose.bones['root'])
        bpy.context.object.data.collections.remove(bpy.context.object.data.collections['Bones'])
        bpy.context.object.data.collections.new('CNSTR')
        bpy.context.object.data.collections.new('CTRL')
        bpy.context.object.data.collections.new('LocOff')
        bpy.ops.object.mode_set(mode='EDIT')
        
        

        return{'FINISHED'} 
    
class OBJECT_OT_chain_parent(bpy.types.Operator):
    """Select a bones to parent them"""
    bl_idname = 'object.chain_parent'
    bl_label = "Chain Parent"
    # Activates a mode where every new bone you select is parented to the previous one

    #enters this mode
    def execute(self,context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        self.report({'INFO'}, "Shift click bones in the 3D view to Chain parent/Use control in the outliner")   

    
    def modal(self, context, event):
        if event.type == 'LEFTMOUSE':
            return {'PASS_THROUGH'}  

        elif event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}     
                 
        if event.type == 'MOUSEMOVE':
            selected_bones = bpy.context.selected_bones
            if len(selected_bones)==2:
                bpy.ops.armature.parent_set(type='OFFSET')
                active_bone = bpy.context.object.data.edit_bones.active
                bpy.ops.armature.select_all(action='DESELECT')
                bpy.context.object.data.edit_bones[active_bone.name].select = True
                bpy.context.object.data.edit_bones[active_bone.name].select_head = True
                bpy.context.object.data.edit_bones[active_bone.name].select_tail = True
                bpy.context.object.data.edit_bones.active =  bpy.context.object.data.edit_bones[active_bone.name]
                self.report({'INFO'}, "Bones Happily Parented! Press ENTER to stop")
                
        # right mouse buttons stops the chain parent action
        elif event.type in {'RIGHTMOUSE', 'RET'}:
            bpy.ops.armature.select_all(action='DESELECT')
            self.report({'INFO'}, "chain bone mode deactivated...")
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.object:
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}

class OBJECT_OT_chain_rename(bpy.types.Operator):
    """Rename bones to chains"""
    bl_idname = 'object.chain_rename'
    bl_label = "Chain Rename"
    
    text : bpy.props.StringProperty(name = "Enter Text", default="")
    startat : bpy.props.IntProperty(name = "Start at", default = 1)

    def execute(self, context):
        number = self.startat
        digits = len(str(len(bpy.context.selected_bones) + self.startat - 1))  # Determine the number of digits needed
        for bone in bpy.context.selected_bones:
            bone.name = f"{self.text}_{number:0{digits}d}"  # Use format specifier for padding with leading zeros
            number += 1
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        

class OBJECT_OT_remove_roll(bpy.types.Operator):
    bl_idname = 'object.remove_roll'
    bl_label = "Remove Roll"
    #Removes roll from the bone. 

    def execute (self, context):
        current_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='EDIT')
        for b in bpy.context.selected_bones:
            b.roll = 0
        bpy.ops.object.mode_set(mode= current_mode)
        return{'FINISHED'} 