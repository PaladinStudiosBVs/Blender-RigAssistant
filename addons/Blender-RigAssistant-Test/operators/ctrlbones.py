import bpy
from mathutils import Vector
#Handles everything related to CTRL_, offset and location bones

class OBJECT_OT_create_control_bone(bpy.types.Operator):
    """creates a cnstr bone for selected bones"""
    bl_idname = 'object.create_control_bone'
    bl_label = "Create Control Bones"
    # Creates a control bone and searches for the CNSTR_ bone to become it's parent
    # Depending which space is selected CTRL_ bone is either created in world or local space

    def execute (self, context):
        current_mode = bpy.context.object.mode
        if current_mode == 'EDIT' or current_mode == 'POSE':
            bpy.ops.object.mode_set(mode='EDIT')
            armanm = bpy.context.active_object
            armature = bpy.context.object.data
            bpy.ops.object.mode_set(mode='POSE')
            pbones = bpy.context.selected_pose_bones
            bpy.ops.object.mode_set(mode='EDIT')
            current_bone = 0
        
            if context.scene.local_world_switch.world_local_enum == 'OP1':
                for b in bpy.context.selected_bones:
                    if  bpy.context.object.data.edit_bones.get("CTRL_" + b.name):
                        bpy.context.object.data.edit_bones.remove(bpy.context.object.data.edit_bones.get("CTRL_" + b.name))
                    
                    cb = bpy.context.object.data.edit_bones.new("CTRL_" + b.name)
                    cb.head = b.head
                    cb.tail = b.tail
                    cb.matrix = b.matrix
                    bpy.context.object.data.edit_bones.get("CTRL_" + b.name).use_deform = False
                    if  bpy.context.object.data.edit_bones.get("CNSTR_" + b.name):
                        bpy.context.object.data.edit_bones["CNSTR_" + b.name].parent = bpy.context.object.data.edit_bones[cb.name]
                
            if context.scene.local_world_switch.world_local_enum == 'OP2':
                for b in bpy.context.selected_bones:
                    if  bpy.context.object.data.edit_bones.get("CTRL_" + b.name):
                        bpy.context.object.data.edit_bones.remove(bpy.context.object.data.edit_bones.get("CTRL_" + b.name))
                    
                    cb = bpy.context.object.data.edit_bones.new("CTRL_" + b.name)
                    world_vector=Vector((0,b.length,0))
                    cb.head = b.head
                    cb.tail = cb.head + world_vector
                    bpy.context.object.data.edit_bones.get("CTRL_" + b.name).use_deform = False
                    if  bpy.context.object.data.edit_bones.get("CNSTR_" + b.name):
                        bpy.context.object.data.edit_bones["CNSTR_" + b.name].parent = bpy.context.object.data.edit_bones[cb.name]



            bpy.ops.object.mode_set(mode= current_mode)
            return{'FINISHED'}
        else:
            self.report({"WARNING"}, "You gotta be in edit or pose mode")
            return {'CANCELLED'}

class OBJECT_OT_create_local_offset_bone(bpy.types.Operator):
    """creates a local offset bone to the last selected parents the first selected under it"""
    bl_idname = 'object.create_local_offset_bone'
    bl_label = "Create Local Offset Bones"
    # Creates a duplicate of the selected bone and parents the original bone under it
    # When 2 bones are selected it duplicates the first selected bone and parents it under the active bone.

    def execute (self, context):
        current_mode = bpy.context.object.mode
        if current_mode == 'EDIT' or current_mode == 'POSE':
            bpy.ops.object.mode_set(mode='EDIT')
            armanm = bpy.context.active_object
            armature = bpy.context.object.data
            selected_bones = bpy.context.selected_bones
            selected_active_bone = bpy.context.object.data.edit_bones.active
        

            if len(selected_bones) == 2:
                if selected_bones[0] == selected_active_bone:
                    active=1
                else:
                    active=0

                    
                cb = bpy.context.object.data.edit_bones.new("LOC_" + selected_bones[active].name)
                cb.head = selected_bones[active].head
                cb.tail = selected_bones[active].tail
                cb.matrix = selected_bones[active].matrix
                bpy.context.object.data.edit_bones.get("LOC_" + selected_bones[active].name).use_deform = False
                bpy.context.object.data.edit_bones[cb.name].parent = bpy.context.object.data.edit_bones[selected_active_bone.name]

            if len(selected_bones) == 1:
                cb = bpy.context.object.data.edit_bones.new("OFF_" + selected_bones[0].name)
                cb.head = selected_bones[0].head
                cb.tail = selected_bones[0].tail
                cb.matrix = selected_bones[0].matrix
                bpy.context.object.data.edit_bones.get("OFF_" + selected_bones[0].name).use_deform = False
                bpy.context.object.data.edit_bones[selected_active_bone.name].parent = bpy.context.object.data.edit_bones[cb.name]
             
            bpy.ops.object.mode_set(mode= current_mode)
            return{'FINISHED'}
        else:
            self.report({"WARNING"}, "You gotta be in edit or pose mode")
            return {'CANCELLED'}

class OBJECT_OT_add_controls(bpy.types.Operator):
    """creates custom shapes on selected pose bones"""
    bl_idname = 'object.add_controls'
    bl_label = "Add Control Shapes"
    # Checks selected bones, checks if there's an object selected
    # Makes the object the shape of the selected bones

    def execute (self, context):
        selected_objects = bpy.context.selected_objects
        bpy.ops.object.mode_set(mode='POSE')
        selected_pose_bones = bpy.context.selected_pose_bones
        bpy.ops.object.mode_set(mode= 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        for meshes in selected_objects:
            if meshes.type == 'MESH':
                bpy.data.objects[meshes.name].select_set(state = True)
                
        

        mesh_count = len(bpy.context.selected_objects)

        if mesh_count > 1:
            print ("Too many meshes selected, Im going to take the first one") 

            bpy.ops.object.mode_set(mode= 'POSE')
            selected_mesh = bpy.context.selected_objects[0]

            for bone in selected_pose_bones:
                bpy.context.object.pose.bones[bone.name].custom_shape = bpy.data.objects[selected_mesh.name]

        if mesh_count == 1:
            bpy.ops.object.mode_set(mode= 'POSE')
            selected_mesh = bpy.context.selected_objects[0]

            for bone in selected_pose_bones:
                bpy.context.object.pose.bones[bone.name].custom_shape = bpy.data.objects[selected_mesh.name]
        

        if mesh_count == 0:
            print ("No mesh selected, I can't work with that")
        return{'FINISHED'}
    
class OBJECT_OT_remove_controls(bpy.types.Operator):
    """creates custom shapes on selected pose bones"""
    bl_idname = 'object.remove_controls'
    bl_label = "Remove Control Shapes"
    # Removes any object shapes that the bones have currently on them

    def execute (self, context):
        selected_pose_bones = bpy.context.selected_pose_bones

        for shapes in selected_pose_bones:
            bpy.context.object.pose.bones[shapes.name].custom_shape = None

        return{'FINISHED'}
    
class OBJECT_OT_suffix_l(bpy.types.Operator):
    bl_idname = 'object.prefix_l'
    bl_label = "Suffix .l"
    # ends a bone name with .l making it suitable for mirroring and symetrization

    def execute (self, context):
        current_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='EDIT')
        for b in bpy.context.selected_bones:
            b.name = b.name + ".l"
        bpy.ops.object.mode_set(mode= current_mode)
        return{'FINISHED'} 

class OBJECT_OT_suffix_r(bpy.types.Operator):
    bl_idname = 'object.prefix_r'
    bl_label = "Suffix .r"
    # ends a bone name with .r making it suitable for mirroring and symetrization

    def execute (self, context):
        current_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='EDIT')
        for b in bpy.context.selected_bones:
            b.name = b.name + ".r"
        bpy.ops.object.mode_set(mode= current_mode)
        return{'FINISHED'} 
