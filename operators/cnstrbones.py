import bpy
from mathutils import Vector
# Does everything with the CNSTR bones and creating constraints

class OBJECT_OT_create_cnstr(bpy.types.Operator):
    """creates a cnstr bone for selected bones"""
    bl_idname = 'object.create_cnstr'
    bl_label = "Create Constraint Bones"
    #Creates a duplicate of the selected bone(s) with the prefix CNSTR_ and
    #constraints the original bone to the newly created bone. The type of constraint is picked in the UI

    def execute (self, context):
        boneCollections = bpy.context.object.data.collections_all;

        visibilityCache = []
        for i in boneCollections:
            visibilityCache.append(i.is_visible)
            
        for b in range(0,len(visibilityCache)):
            boneCollections[b].is_visible = True
            
        if bpy.context.selected_pose_bones is None and bpy.context.selected_bones is None :
            for i in range(0,len(visibilityCache)):
                boneCollections[i].is_visible = visibilityCache[i]
            visibilityCache.clear
            
            self.report({"WARNING"}, "No Bones selected Check if they are visible")
            return {'CANCELLED'} 

        current_mode = bpy.context.object.mode
        if current_mode == 'EDIT' or current_mode == 'POSE':
            bpy.ops.object.mode_set(mode='EDIT')
            armanm = bpy.context.active_object
            armature = bpy.context.object.data
            bpy.ops.object.mode_set(mode='POSE')
            pbones = bpy.context.selected_pose_bones
            bpy.ops.object.mode_set(mode='EDIT')
            current_bone = 0

            # Collection stuff: Check if there's a collection CNSTR if it's not, make it
            if boneCollections.get('CNSTR') is None:
                bcoll = bpy.context.object.data.collections.new('CNSTR')

            # this part duplicates the bone. If the duplicate already exists it deletes the old one and creates a new one
            # Also checks if there is a CTRL_ prefixed bone to parent under. 
            for b in bpy.context.selected_bones:
                if  bpy.context.object.data.edit_bones.get("CNSTR_" + b.name):
                    bpy.context.object.data.edit_bones.remove(bpy.context.object.data.edit_bones.get("CNSTR_" + b.name))

                cb = armature.edit_bones.new("CNSTR_" + b.name)
                cb.head = b.head
                cb.tail = b.tail
                cb.matrix = b.matrix
                bpy.context.object.data.edit_bones.get("CNSTR_" + b.name).use_deform = False
                if  bpy.context.object.data.edit_bones.get("CTRL_" + b.name):
                    bpy.context.object.data.edit_bones["CNSTR_" + b.name].parent = bpy.context.object.data.edit_bones["CTRL_" + b.name]

                
            #This part sets up the constraint
            bpy.ops.object.mode_set(mode='POSE')
             

            for pb in pbones:    
                for c in pb.constraints:
                    pb.constraints.remove(c)
                #first put the bone into the right collection
                bpy.context.object.data.collections['CNSTR'].assign(bpy.context.object.pose.bones["CNSTR_" + pbones[current_bone].name])  
                bpy.ops.pose.select_all(action='DESELECT')
                bpy.context.object.data.bones[pbones[current_bone].name].select = True
                bpy.context.object.data.bones["CNSTR_" + pbones[current_bone].name].select = True
                bpy.context.object.data.bones.active = bpy.context.object.pose.bones[pbones[current_bone].name].bone
                if context.scene.type_constrain.constraint_enum == 'OP1':
                    bpy.ops.pose.constraint_add_with_targets(type = 'COPY_TRANSFORMS')
                if context.scene.type_constrain.constraint_enum == 'OP2':
                    bpy.ops.pose.constraint_add_with_targets(type = 'COPY_LOCATION')
                if context.scene.type_constrain.constraint_enum == 'OP3':
                    bpy.ops.pose.constraint_add_with_targets(type = 'COPY_ROTATION')
                if context.scene.type_constrain.constraint_enum == 'OP4':
                    bpy.ops.pose.constraint_add_with_targets(type = 'COPY_SCALE')
                if context.scene.type_constrain.constraint_enum == 'OP5':
                    bpy.ops.pose.constraint_add_with_targets(type = 'IK')
                    constraint_count = 1-len(bpy.context.selected_pose_bones[0].constraints)
                    bpy.context.selected_pose_bones[0].constraints[constraint_count].use_tail = False
                    bpy.context.selected_pose_bones[0].constraints[constraint_count].chain_count= 2
                bpy.ops.pose.select_all(action='DESELECT')
                current_bone += 1
            
                
            current_bone=0
            for pb in pbones:
                bpy.context.object.data.bones[pbones[current_bone].name].select = True
                current_bone += 1
        
            
            for i in range(0,len(visibilityCache)):
                boneCollections[i].is_visible = visibilityCache[i]
            visibilityCache.clear

            bpy.ops.object.mode_set(mode= current_mode)
            return{'FINISHED'}
        else:
            self.report({"WARNING"}, "You gotta be in edit or pose mode")
            return {'CANCELLED'}
        
class OBJECT_OT_remove_cnstr_bone(bpy.types.Operator):
    bl_idname = 'object.remove_cnstr_bone'
    bl_label = "Remove Constraint Bone" 

    #This cleanly removes a CNSTR_ bone also deleting the contraint on the deform bone  
    def execute (self, context):
        boneCollections = bpy.context.object.data.collections_all;

        visibilityCache = []
        for i in boneCollections:
            visibilityCache.append(i.is_visible)
            
        for b in range(0,len(visibilityCache)):
            boneCollections[b].is_visible = True

        if bpy.context.selected_pose_bones is None and bpy.context.selected_bones is None :
            for i in range(0,len(visibilityCache)):
                boneCollections[i].is_visible = visibilityCache[i]
            visibilityCache.clear
            
            self.report({"WARNING"}, "No Bones selected Check if they are visible")
            return {'CANCELLED'}
        
        current_mode = bpy.context.object.mode

        bpy.ops.object.mode_set(mode='POSE')
        pbones = bpy.context.selected_pose_bones

        bpy.ops.object.mode_set(mode='EDIT')

        for b in bpy.context.selected_bones:
            if  bpy.context.object.data.edit_bones.get("CNSTR_" + b.name):
                bpy.context.object.data.edit_bones.remove(bpy.context.object.data.edit_bones.get("CNSTR_" + b.name))

        for bone in pbones:
            for c in bone.constraints:
                bone.constraints.remove(c)  # Remove constraint 
        
        for i in range(0,len(visibilityCache)):
                boneCollections[i].is_visible = visibilityCache[i]
        visibilityCache.clear
        
        bpy.ops.object.mode_set(mode= current_mode)

        return{'FINISHED'} 

class OBJECT_OT_remove_selected_bone(bpy.types.Operator):
    bl_idname = 'object.remove_selected_bone'
    bl_label = "Remove Selected Bones"  
    #This just deletes bones
     
    def execute (self, context):
        boneCollections = bpy.context.object.data.collections_all;

        visibilityCache = []
        for i in boneCollections:
            visibilityCache.append(i.is_visible)
            
        for b in range(0,len(visibilityCache)):
            boneCollections[b].is_visible = True

        if bpy.context.selected_pose_bones is None and bpy.context.selected_bones is None :
            for i in range(0,len(visibilityCache)):
                boneCollections[i].is_visible = visibilityCache[i]
            visibilityCache.clear
            
            self.report({"WARNING"}, "No Bones selected Check if they are visible")
            return {'CANCELLED'}

        current_mode = bpy.context.object.mode

        bpy.ops.object.mode_set(mode='EDIT')

        for b in bpy.context.selected_bones:
            bpy.context.object.data.edit_bones.remove(b)
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.object.mode_set(mode= current_mode)

        for i in range(0,len(visibilityCache)):
            boneCollections[i].is_visible = visibilityCache[i]
        visibilityCache.clear

        return{'FINISHED'} 

class OBJECT_OT_remove_all_cnstr(bpy.types.Operator):
    bl_idname = 'object.remove_all_cnstr'
    bl_label = "Remove all constraints"
    # removes all the constraints from a selected bone
    # goes to pose mode, clocks the selected bones, clocks the constraints and deletes them all
    # goes back to the previous selected mode

    def execute (self, context):
        boneCollections = bpy.context.object.data.collections_all;

        visibilityCache = []
        for i in boneCollections:
            visibilityCache.append(i.is_visible)
            
        for b in range(0,len(visibilityCache)):
            boneCollections[b].is_visible = True

        if bpy.context.selected_pose_bones is None and bpy.context.selected_bones is None :
            for i in range(0,len(visibilityCache)):
                boneCollections[i].is_visible = visibilityCache[i]
            visibilityCache.clear
            
            self.report({"WARNING"}, "No Bones selected Check if they are visible")
            return {'CANCELLED'}

        current_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='POSE')
        for bone in bpy.context.selected_pose_bones:
            for c in bone.constraints:
                bone.constraints.remove(c)  # Remove constraint 
        
        for i in range(0,len(visibilityCache)):
            boneCollections[i].is_visible = visibilityCache[i]
        visibilityCache.clear

        bpy.ops.object.mode_set(mode= current_mode)
        return{'FINISHED'} 

class OBJECT_OT_add_cnstr(bpy.types.Operator):
    bl_idname = 'object.add_cnstr'
    bl_label = "Constraint Between Selected Bones"   
    #Adds a constrain between selected bones
    #Constrain type gets picked in the UI in __init__
    #IK has already been set to most used config

    def execute(self,context):
        boneCollections = bpy.context.object.data.collections_all;

        visibilityCache = []
        for i in boneCollections:
            visibilityCache.append(i.is_visible)
            
        for b in range(0,len(visibilityCache)):
            boneCollections[b].is_visible = True

        if bpy.context.selected_pose_bones is None and bpy.context.selected_bones is None :
            for i in range(0,len(visibilityCache)):
                boneCollections[i].is_visible = visibilityCache[i]
            visibilityCache.clear
            
            self.report({"WARNING"}, "No Bones selected Check if they are visible")
            return {'CANCELLED'}

        current_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='POSE')
        if context.scene.type_constrain.constraint_enum == 'OP1':
            bpy.ops.pose.constraint_add_with_targets(type = 'COPY_TRANSFORMS')
        if context.scene.type_constrain.constraint_enum == 'OP2':
            bpy.ops.pose.constraint_add_with_targets(type = 'COPY_LOCATION')
        if context.scene.type_constrain.constraint_enum == 'OP3':
            bpy.ops.pose.constraint_add_with_targets(type = 'COPY_ROTATION')
        if context.scene.type_constrain.constraint_enum == 'OP4':
            bpy.ops.pose.constraint_add_with_targets(type = 'COPY_SCALE')
        if context.scene.type_constrain.constraint_enum == 'OP5':
            bpy.ops.pose.constraint_add_with_targets(type = 'IK')
            constraint_count = 1-len(bpy.context.selected_pose_bones[0].constraints)
            bpy.context.selected_pose_bones[0].constraints[constraint_count].use_tail = False
            bpy.context.selected_pose_bones[0].constraints[constraint_count].chain_count= 2
        
        for i in range(0,len(visibilityCache)):
            boneCollections[i].is_visible = visibilityCache[i]
        visibilityCache.clear

        bpy.ops.object.mode_set(mode= current_mode)

        return{'FINISHED'} 

class OBJECT_OT_append_cnstr(bpy.types.Operator):
    bl_idname = 'object.append_cnstr'
    bl_label = "Append Constraint To Bones"
    #Will append a constraint to a bone that already has a CNSTR bone.
    #Constrain type gets picked in the UI in __init__
    #IK has already been set to most used config  
    
    def execute(self,context):
        boneCollections = bpy.context.object.data.collections_all;

        visibilityCache = []
        for i in boneCollections:
            visibilityCache.append(i.is_visible)
            
        for b in range(0,len(visibilityCache)):
            boneCollections[b].is_visible = True

        if bpy.context.selected_pose_bones is None and bpy.context.selected_bones is None :
            for i in range(0,len(visibilityCache)):
                boneCollections[i].is_visible = visibilityCache[i]
            visibilityCache.clear
            
            self.report({"WARNING"}, "No Bones selected Check if they are visible")
            return {'CANCELLED'}

        current_mode = bpy.context.object.mode
        current_bone = 0
        bpy.ops.object.mode_set(mode='POSE')
        pbones = bpy.context.selected_pose_bones
        for pb in pbones:
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.data.bones[pbones[current_bone].name].select = True
            bpy.context.object.data.bones["CNSTR_" + pbones[current_bone].name].select = True
            bpy.context.object.data.bones.active = bpy.context.object.pose.bones[pbones[current_bone].name].bone
            if context.scene.type_constrain.constraint_enum == 'OP1':
                bpy.ops.pose.constraint_add_with_targets(type = 'COPY_TRANSFORMS')
            if context.scene.type_constrain.constraint_enum == 'OP2':
                bpy.ops.pose.constraint_add_with_targets(type = 'COPY_LOCATION')
            if context.scene.type_constrain.constraint_enum == 'OP3':
                bpy.ops.pose.constraint_add_with_targets(type = 'COPY_ROTATION')
            if context.scene.type_constrain.constraint_enum == 'OP4':
                bpy.ops.pose.constraint_add_with_targets(type = 'COPY_SCALE')
            if context.scene.type_constrain.constraint_enum == 'OP5':
                bpy.ops.pose.constraint_add_with_targets(type = 'IK')
                constraint_count = 1-len(bpy.context.selected_pose_bones[0].constraints)
                bpy.context.selected_pose_bones[0].constraints[constraint_count].use_tail = False
                bpy.context.selected_pose_bones[0].constraints[constraint_count].chain_count= 2
           
            bpy.ops.pose.select_all(action='DESELECT')
            current_bone += 1
            
        current_bone=0
        for pb in pbones:
            bpy.context.object.data.bones[pbones[current_bone].name].select = True
            current_bone += 1

        
        for i in range(0,len(visibilityCache)):
            boneCollections[i].is_visible = visibilityCache[i]
        visibilityCache.clear

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode= current_mode)

        return{'FINISHED'} 
    
