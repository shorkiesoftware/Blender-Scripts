import bpy
import array
import math
import mathutils
from os import system

system('cls')

outputFile = "C:/Users/Dave/Desktop/marc_ride_slow.pose"
armatureName = 'Armature'

arm = bpy.data.objects[armatureName]
bones = arm.pose.bones
position = []
boneArray = []

class Counter:
    ctr = 0

def parseBone(bone, parent, pid, counter):
    index = counter.ctr
    counter.ctr += 1
    
    mat = 0
    if parent is not None:
        mat = parent.matrix.inverted() @ bone.matrix
    else:
        mat = bone.matrix
        
    rot = mat.to_quaternion()
    boneArray.append(-rot.x)
    boneArray.append(-rot.y)
    boneArray.append(rot.z)
    boneArray.append(rot.w)
    
    for c in bone.children:
        parseBone(c, bone, index, counter)
        
bpy.ops.object.select_all(action='DESELECT')
arm.select_set(True)
arm.rotation_euler = mathutils.Euler((-1.5707963, 0, 0), 'XYZ')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

count = Counter()
position.append(bones[0].matrix[0][3])
position.append(bones[0].matrix[1][3])
position.append(-bones[0].matrix[2][3])
parseBone(bones[0], None, 0, count)

arm.rotation_euler = mathutils.Euler((1.5707963, 0, 0), 'XYZ')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

print(position)

file = open(outputFile, "wb")
array.array("I", [count.ctr]).tofile(file)
array.array("f", position).tofile(file)
array.array("f", boneArray).tofile(file)
file.close()
    
print("DONE")