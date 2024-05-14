import bpy
from mathutils import Vector
# Create different shapes that can be used as bone shapes

class OBJECT_OT_create_circle(bpy.types.Operator):
    bl_idname = 'object.create_circle'
    bl_label = "Circle"

    def execute (self, context):
        if bpy.context.selected_objects:
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.mesh.primitive_circle_add()
        bpy.context.object.name = "circle_shpctrl"

        return{'FINISHED'} 

class OBJECT_OT_create_cube(bpy.types.Operator):
    bl_idname = 'object.create_cube'
    bl_label = "Cube"

    def execute (self, context):
        if bpy.context.selected_objects:
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.object.name = "cube_shpctrl"
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.object.show_wire = True

        return{'FINISHED'} 

class OBJECT_OT_create_piramid(bpy.types.Operator):
    bl_idname = 'object.create_piramid'
    bl_label = "Piramid"

    def execute (self, context):
        if bpy.context.selected_objects:
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.mesh.primitive_cone_add(vertices=4)
        bpy.context.object.name = "piramid_shpctrl"
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.transform.rotate(value=0.785398, orient_axis='Z', orient_type='GLOBAL')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.object.show_wire = True


        return{'FINISHED'} 

class OBJECT_OT_create_sphere(bpy.types.Operator):
    bl_idname = 'object.create_sphere'
    bl_label = "Sphere"

    def execute (self, context):
        if bpy.context.selected_objects:
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.mesh.primitive_circle_add(enter_editmode=True)
        bpy.ops.mesh.primitive_circle_add(rotation = (1.5707963267948966, 0, 0))
        bpy.ops.mesh.primitive_circle_add(rotation = (0, 1.5707963267948966, 0))
        bpy.ops.object.mode_set(mode = 'OBJECT')

        return{'FINISHED'} 

class OBJECT_OT_create_square(bpy.types.Operator):
    bl_idname = 'object.create_square'
    bl_label = "Square"

    def execute (self, context):
        if bpy.context.selected_objects:
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.context.object.name = "square_shpctrl"
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.object.show_wire = True

        return{'FINISHED'} 
